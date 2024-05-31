from dataclasses import dataclass
from urllib.request import urlretrieve
from urllib.parse import urlparse
from threading import Thread
from tempfile import TemporaryFile
from typing import Optional
import hashlib
import socket
import os
import logging
import struct
import binascii
import time
import re

from . import config
from .android.fastbootd import Fastbootd
from .tftpd import TFTPD, TFTPDClient
from .dhcpd import DHCPD, CPUArch, Firmware, BootProtocol, MacAddress
from .logger import logger
from .socketactivation import get_sockets_by_name

DEFAULT_CONFIG_PATHS = {
    'TFTP_DIR': '/boots/tftp',
}

# The IPXE binaries can get generated using "make ipxe-dut-clients"
IPXE_BASE_URL = 'https://downloads.gfx-ci.steamos.cloud/ipxe-dut-client/'
IPXE_BINARIES = {
    "IPXE_X86_64_EFI_FILENAME": '2024-01-30_20-41-29-mupuf-x86_64-snponly.efi',
    "IPXE_I386_EFI_FILENAME": '2024-01-30_20-41-29-mupuf-i386-snponly.efi',
    "IPXE_I386_MBR_FILENAME": '2024-01-30_20-41-29-mupuf-i386-undionly.kpxe',
    "IPXE_ARM32_EFI_FILENAME": '2024-01-30_20-41-29-mupuf-arm32-snponly.efi',
    "IPXE_ARM64_EFI_FILENAME": '2024-01-30_20-41-29-mupuf-arm64-snponly.efi',
}
BASE_DIR = os.path.dirname(__file__)


def provision_ipxe_dut_clients(tftp_dir):  # pragma: nocover
    os.makedirs(tftp_dir, exist_ok=True)

    logger.debug("Downloading the latest iPXE DUT clients...")
    for filename in IPXE_BINARIES.values():
        urlretrieve(f"{IPXE_BASE_URL}/{filename}", os.path.join(tftp_dir, filename))


class BootsDHCPD(DHCPD, Thread):
    def __init__(self, boots, name, interface):  # pragma: nocover
        self.boots = boots

        Thread.__init__(self, name=name)
        self.daemon = True

        DHCPD.__init__(self, interface=interface)

    @property
    def static_clients(self):
        clients = []
        for dut in self.boots.mars.known_machines:
            clients.append({'mac_addr': MacAddress(dut.mac_address),
                            'ipaddr': dut.ip_address,
                            'hostname': dut.full_name})
        return clients

    def boot_target(self, client_request):
        # Ensure MaRS is aware of this client request
        mac_addr = client_request.mac_addr
        ip_address, _ = self.get_or_assign_ip_for_client(mac_addr)
        arch = client_request.architecture.name
        fw = client_request.firmware.name
        protocol = client_request.protocol.name
        dut_data = {
            "id": mac_addr.as_str,
            "mac_address": mac_addr.as_str,
            "base_name": f"{arch}-{fw}-{protocol}".lower(),
            "ip_address": ip_address,
            "tags": []
        }
        self.boots.mars.machine_discovered(dut_data, update_if_already_exists=False)

        if client_request.architecture not in [CPUArch.X86, CPUArch.X86_64, CPUArch.ARM32, CPUArch.ARM64]:
            self.logger.error(f"Unsupported architecture '{client_request.architecture}'")
            return None

        if client_request.protocol != BootProtocol.TFTP:
            self.logger.error(f"Unsupported protocol '{client_request.protocol}'")
            return None

        if client_request.user_class == "iPXE":
            p = client_request.firmware.to_ipxe_platform if client_request.firmware else ""
            b = client_request.architecture.to_ipxe_buildarch if client_request.architecture else ""
            return f"{config.EXECUTOR_URL}/boot/{client_request.mac_addr}/boot.ipxe?platform={p}&buildarch={b}"
        elif client_request.firmware == Firmware.BIOS:
            if client_request.architecture in [CPUArch.X86, CPUArch.X86_64]:
                # NOTE: BIOS firmware means an x86-compatible CPU, and the i386 binary will work for all of them
                return IPXE_BINARIES['IPXE_I386_MBR_FILENAME']
            else:
                self.logger.error(f"Unsupported BIOS architecture '{client_request.architecture}'")
        elif client_request.firmware == Firmware.UEFI:
            if client_request.architecture == CPUArch.X86:
                return IPXE_BINARIES['IPXE_I386_EFI_FILENAME']
            elif client_request.architecture == CPUArch.X86_64:
                return IPXE_BINARIES['IPXE_X86_64_EFI_FILENAME']
            elif client_request.architecture == CPUArch.ARM32:
                return IPXE_BINARIES['IPXE_ARM32_EFI_FILENAME']
            elif client_request.architecture == CPUArch.ARM64:
                return IPXE_BINARIES['IPXE_ARM64_EFI_FILENAME']
            else:  # pragma: nocover
                self.logger.error(f"Unsupported UEFI architecture '{client_request.architecture}'")
        elif client_request.firmware == Firmware.UBOOT:
            arch = client_request.architecture.name
            return f"/dyn/bootloader/u-boot/{arch}/{client_request.mac_addr}/boot.scr"
        else:
            self.logger.error(f"Unsupported firmware type '{client_request.firmware}'")
            return None

    def run(self):  # pragma: nocover
        # Use the socket provided by our caller (systemd?), or create or own if none are found
        sock = None
        if sockets := get_sockets_by_name(config.BOOTS_DHCP_IPv4_SOCKET_NAME, socket.AF_INET, socket.SOCK_DGRAM):
            sock = sockets[0]

        self.listen(sock)


class TftpdClient(TFTPDClient):  # pragma: nocover
    def load_file(self, filename):
        if m := re.fullmatch("/?dyn/bootloader/u-boot/([^/]*)/([^/]*)/boot.scr", filename):
            buildarch = m.group(1)
            machine_id = m.group(2)
            data = self.parent.boots.uboot_boot_script(buildarch, machine_id)

            try:
                self.fh = TemporaryFile()
                self.fh.write(data)
                self.fh.seek(0)

                self.filesize = len(data)
                self.filename = 'gen://' + filename
            except Exception as e:
                self.parent.logger.warning(f"While serving {filename} caught the following exception: {e}")
                return False

            return True

        if m := re.fullmatch("/?minio(/.*)", filename):
            minio_url = config.MINIO_URL + m.group(1)
            try:
                tempfile, headers = urlretrieve(minio_url)
            except Exception as e:
                self.parent.logger.warning(f"While fetching {minio_url} caught the following exception: {e}")
                return False

            try:
                self.fh = open(tempfile, 'rb')

                self.fh.seek(0, os.SEEK_END)
                self.filesize = self.fh.tell()
                self.fh.seek(0, os.SEEK_SET)

                self.filename = "minio://" + filename
            except Exception as e:
                self.parent.logger.warning(f"While serving {minio_url} caught the following exception: {e}")
                return False
            finally:
                os.remove(tempfile)

            return True

        return TFTPDClient.load_file(self, filename)


class BootsTFTPD(TFTPD, Thread):  # pragma: nocover
    def __init__(self, boots, name, directory, interface):
        self.boots = boots

        Thread.__init__(self, name=name)
        self.daemon = True

        tftp_logger = logging.getLogger(f"{logger.name}.TFTP")
        tftp_logger.setLevel(logging.INFO)
        TFTPD.__init__(self, interface, client=TftpdClient, logger=tftp_logger, netboot_directory=directory)

    def run(self):
        # Use the socket provided by our caller (systemd?), or create or own if none are found
        sock = None
        if sockets := get_sockets_by_name(config.BOOTS_TFTP_IPv4_SOCKET_NAME, socket.AF_INET, socket.SOCK_DGRAM):
            sock = sockets[0]

        self.listen(sock)


class BootsFastbootd(Fastbootd, Thread):  # pragma: nocover
    def __init__(self, boots, name):
        self.boots = boots

        Thread.__init__(self, name=name)
        self.daemon = True

        fastbootd_logger = logging.getLogger(f"{logger.name}.Fastbootd")
        fastbootd_logger.setLevel(logging.INFO)
        Fastbootd.__init__(self, logger=fastbootd_logger)

    def gen_mac_address(self, serial):
        mac_addr = bytearray(hashlib.sha1(serial.encode()).digest()[-7:-1])

        # Ensure we generated a locally-administrated MAC address
        if (mac_addr[0] & 0x0F) not in [0x2, 0x6, 0xA, 0xE]:
            mac_addr[0] = (mac_addr[0] & 0x0F) | 0x2

        return MacAddress(bytes(mac_addr))

    def new_device_found(self, device):  # pragma: nocover
        # Ensure the bootloader is unlocked
        if device.variables.get("unlocked") != "yes":
            try:
                device.run_cmd(b"flashing:unlock")
            except Exception:
                # Ignore errors, we'll just tell users that the device is unusable
                pass

        # Ensure MaRS is aware of this client request
        serialno = device.variables["serialno"]
        mac_addr = self.gen_mac_address(serialno)
        product_name = device.variables.get("product")
        base_name = product_name or serialno
        ip_address, _ = self.boots.dhcpd.get_or_assign_ip_for_client(mac_addr)
        dut_data = {
            "id": serialno,
            "mac_address": mac_addr.as_str,
            "base_name": f"fastboot-{base_name}".lower(),
            "ip_address": ip_address,
            "tags": []
        }
        self.boots.mars.machine_discovered(dut_data, update_if_already_exists=False)

        # We got everything we wanted from the device, free our lock
        device.release()

        # Notify the DUT that we are ready to boot!
        if dut := self.boots.mars.get_machine_by_id(serialno):
            dut.boot_config_query(platform=None, buildarch=None, bootloader="fastboot")

    def run(self):
        while True:
            self.update_device_list()
            time.sleep(1)


@dataclass
class BootConfig:
    kernel: Optional[str] = None
    initrd: Optional[str] = None
    cmdline: Optional[str] = None

    dtb: Optional[str] = None

    @classmethod
    def _gen_envvar_name(cls, suffix, fields):
        # Check that all the fields are strings
        for field in fields:
            if not isinstance(field, str):
                return None

        if len(fields) > 0:
            fields_str = "_".join([f.upper() for f in fields if f]) + "_"
        else:
            fields_str = ""

        return "BOOTS_DEFAULT_" + fields_str + suffix

    @classmethod
    def _find_best_option(cls, machine, bootloader, platform, buildarch, suffix):
        # Generate all the possible names for environment variables
        prioritized_combos = [
            (bootloader, buildarch, platform),
            (buildarch, platform),
            (bootloader, buildarch),
            (buildarch, ),
            (bootloader, ),
            tuple()
        ]
        prioritized_opts = [cls._gen_envvar_name(suffix, fields) for fields in prioritized_combos]

        # Iterate through the options, in priority order, ignoring invalid entries
        for option in [o for o in prioritized_opts if o]:
            if opt := os.environ.get(option):
                return opt

    @classmethod
    def defaults(cls, machine=None, bootloader=None, platform=None, buildarch=None):
        # Possible values:
        # * bootloader: ipxe, uboot
        # * platforms: efi, pcbios, uboot
        # * buildarch: i386, x86_64, arm32, arm64

        kwargs = {"machine": machine, "bootloader": bootloader, "platform": platform, "buildarch": buildarch}
        kernel = cls._find_best_option(**kwargs, suffix="KERNEL")
        if not kernel:
            raise ValueError("No default kernel found (specified using BOOTS_DEFAULT_*KERNEL)")

        initrd = cls._find_best_option(**kwargs, suffix="INITRD")
        if not initrd:
            raise ValueError("No default initramfs found (specified using BOOTS_DEFAULT_*INITRD)")

        cmdline = cls._find_best_option(**kwargs, suffix="CMDLINE")
        if not cmdline:
            raise ValueError("No default kernel command line found (specified using BOOTS_DEFAULT_*CMDLINE)")

        # NOTE: We voluntarily do not want to use a default DTB as we want to replace this mechanism in the future
        # with something a little more flexible

        return cls(kernel=kernel, initrd=initrd, cmdline=cmdline)

    def fixup_missing_fields_with_defaults(self, machine=None, bootloader=None, platform=None, buildarch=None):
        kwargs = {"machine": machine, "bootloader": bootloader, "platform": platform, "buildarch": buildarch}

        if not self.kernel:
            self.kernel = self._find_best_option(**kwargs, suffix="KERNEL")
            if not self.kernel:
                raise ValueError("No default kernel found (specified using BOOTS_DEFAULT_*KERNEL)")

        if not self.initrd:
            self.initrd = self._find_best_option(**kwargs, suffix="INITRD")
            if not self.initrd:
                raise ValueError("No default initramfs found (specified using BOOTS_DEFAULT_*INITRD)")


class BootService:
    def __init__(self, mars,
                 private_interface=None,
                 config_paths=DEFAULT_CONFIG_PATHS):
        self.mars = mars
        self.private_interface = private_interface or config.PRIVATE_INTERFACE
        self.config_paths = config_paths

        # Do not start the servers
        if config.BOOTS_DISABLE_SERVERS:
            self.dhcpd = self.tftpd = self.fastbootd = None
            return

        # Download the iPXE binaries and store them where the DUTs can download them
        provision_ipxe_dut_clients(tftp_dir=config_paths['TFTP_DIR'])

        self.dhcpd = BootsDHCPD(self, "DHCP Server", self.private_interface)
        self.dhcpd.dns_servers = [self.dhcpd.ip]
        self.dhcpd.start()

        self.tftpd = BootsTFTPD(self, "TFTP Server", self.config_paths["TFTP_DIR"], self.private_interface)
        self.tftpd.start()

        self.fastbootd = BootsFastbootd(self, "Fastbootd Server")
        self.fastbootd.start()

    @classmethod
    def _platform_cmdline(cls, platform=None):
        return "initrd=initrd" if platform in ["efi"] else ""

    @classmethod
    def _gen_ipxe_boot_script(cls, bootconfig, platform=None):
        platform_cmdline = cls._platform_cmdline(platform=platform)

        cmdline = bootconfig.cmdline if bootconfig.cmdline is not None else ""
        cmdline = cmdline.replace(";", "${semicolon:string}")
        cmdline = cmdline.replace("&", "${ampersand:string}")
        cmdline = cmdline.replace("|", "${pipe:string}")

        return f"""#!ipxe

set semicolon:hex 3b
set ampersand:hex 26
set pipe:hex 7C

echo

echo Downloading the kernel
kernel {bootconfig.kernel} {platform_cmdline} {cmdline}

echo Downloading the initrd
initrd --name initrd {bootconfig.initrd}

echo Booting!
boot
"""

    def get_boot_config(self, machine=None, platform=None, buildarch=None, bootloader="ipxe"):
        bootconfig = None

        if machine is not None:
            bootconfig = machine.boot_config_query(platform=platform, buildarch=buildarch, bootloader=bootloader)

        if bootconfig is None:
            bootconfig = BootConfig.defaults(machine=machine, bootloader=bootloader,
                                             platform=platform, buildarch=buildarch)

        return bootconfig

    def ipxe_boot_script(self, machine=None, platform=None, buildarch=None):
        bootconfig = self.get_boot_config(machine, platform, buildarch)
        return self._gen_ipxe_boot_script(bootconfig, platform=platform)

    @classmethod
    def _gen_uboot_boot_script(cls, bootconfig, platform=None):
        platform_cmdline = cls._platform_cmdline(platform=platform)
        cmdline = bootconfig.cmdline if bootconfig.cmdline is not None else ""
        kernel = "minio" + urlparse(bootconfig.kernel).path
        initrd = "minio" + urlparse(bootconfig.initrd).path
        fdt = ("minio" + urlparse(bootconfig.dtb).path) if bootconfig.dtb else ""

        # TODO: consider adding EFI boot support?
        return f"""
echo Loading
setenv bootargs '{platform_cmdline} {cmdline}'
tftp ${{kernel_addr_r}} {kernel}
if test -n "{fdt}"
then
    tftp ${{fdt_addr}} {fdt}
elif test -n "${{fdt_file}}"
then
    tftp ${{fdt_addr}} {fdt}
else
    setenv fdt_addr ${{fdtcontroladdr}}
fi

tftp ${{ramdisk_addr_r}} {initrd}
setenv ramdisk_size ${{filesize}}
if test -z "${{kernel_comp_addr_r}}"
then
    setexpr kernel_comp_addr_r ${{ramdisk_addr_r}} + ${{ramdisk_size}}
    setenv kernel_comp_size 0x4000000 # hope for the best
fi

echo Booting!
booti ${{kernel_addr_r}} ${{ramdisk_addr_r}}:${{ramdisk_size}} ${{fdt_addr}}
bootz ${{kernel_addr_r}} ${{ramdisk_addr_r}}:${{ramdisk_size}} ${{fdt_addr}}
"""

    def uboot_boot_script(self, buildarch=None, machine_id=None):
        platform = "uboot"

        machine = self.mars.get_machine_by_id(machine_id)
        bootconfig = self.get_boot_config(machine, platform, buildarch, "uboot")

        script = bytes(self._gen_uboot_boot_script(bootconfig, platform=platform), "ascii")

        MAGIC = 0x27051956
        OS_LINUX = 5

        ARCH_INVALID = 0
        ARCH_ARM = 2
        ARCH_I386 = 3
        ARCH_ARM64 = 22
        ARCH_X86_64 = 24
        ARCH_RISCV = 26

        TYPE_SCRIPT = 6
        COMP_NONE = 0

        data = struct.pack(">II", len(script), 0) + script
        dcrc = binascii.crc32(data)

        if buildarch == CPUArch.ARM32.name:
            uboot_arch = ARCH_ARM
        elif buildarch == CPUArch.X86.name:
            uboot_arch = ARCH_I386
        elif buildarch == CPUArch.ARM64.name:
            uboot_arch = ARCH_ARM64
        elif buildarch == CPUArch.X86_64.name:
            uboot_arch = ARCH_X86_64
        elif buildarch == CPUArch.RISCV32.name or buildarch == CPUArch.RISCV64.name:
            uboot_arch = ARCH_RISCV
        else:
            uboot_arch = ARCH_INVALID

        hdr = struct.pack(">7I4b32x",
                          MAGIC, 0, int(time.time()), len(data), 0, 0, dcrc,
                          OS_LINUX, uboot_arch, TYPE_SCRIPT, COMP_NONE)
        hcrc = binascii.crc32(hdr)
        return hdr[0:4] + struct.pack(">I", hcrc) + hdr[8:] + data
