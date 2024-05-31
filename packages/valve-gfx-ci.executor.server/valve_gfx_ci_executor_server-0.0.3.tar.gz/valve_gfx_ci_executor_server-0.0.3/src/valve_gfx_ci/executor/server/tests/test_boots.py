from unittest.mock import patch, MagicMock
from server.boots import BootService, BootConfig, IPXE_BINARIES, BootsDHCPD
from server.dhcpd import CPUArch, Firmware, BootProtocol, MacAddress
import server.config as config
import pytest


@patch("server.boots.BootsTFTPD")
@patch("server.boots.BootsDHCPD")
@patch("server.boots.provision_ipxe_dut_clients")
def create_boot_service(tmp_path, mock_provisioner, mock_dhcpd, mock_tftpd):
    paths = {
        'TFTP_DIR': f'{tmp_path}/tftp',
    }
    service = BootService(MagicMock(),
                          private_interface='br0',
                          config_paths=paths)

    if not config.BOOTS_DISABLE_SERVERS:
        mock_dhcpd.assert_called_with(service, "DHCP Server", 'br0')
        mock_tftpd.assert_called_with(service, "TFTP Server", paths["TFTP_DIR"], 'br0')

    return service


def test_boot_service(tmp_path):
    create_boot_service(tmp_path)


def test_boot_service_disabled(tmp_path):
    config.BOOTS_DISABLE_SERVERS = True
    try:
        create_boot_service(tmp_path)
    finally:
        config.BOOTS_DISABLE_SERVERS = False


@patch("server.boots.DHCPD.__init__")
def test_dhcpd_static_clients(dhcpd_mock):
    boots = MagicMock()
    dhcp = BootsDHCPD(boots, name="toto", interface="br0")

    m_mac = "00-01-02-03-04-05"
    m_ipaddr = "10.42.0.42"
    m_hostname = "machine1"

    boots.mars.known_machines = [MagicMock(mac_address=m_mac, ip_address=m_ipaddr, full_name=m_hostname)]
    assert dhcp.static_clients == [{'mac_addr': MacAddress(m_mac), 'ipaddr': m_ipaddr, 'hostname': m_hostname}]


@patch("server.boots.DHCPD.__init__")
def test_dhcpd_boot_target(dhcpd_mock):
    dhcp = BootsDHCPD(MagicMock(), name="toto", interface="br0")
    dhcp.logger = MagicMock()
    dhcp.get_or_assign_ip_for_client = MagicMock(return_value=("10.0.0.42", "new client"))

    dhcpd_mock.assert_called_once_with(dhcp, interface="br0")

    # Legacy X86 boot
    request = MagicMock(architecture=CPUArch.X86, firmware=Firmware.BIOS,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == IPXE_BINARIES['IPXE_I386_MBR_FILENAME']
    dhcp.boots.mars.machine_discovered.assert_called_once_with(
        {
            "id": "00:01:02:03:04:05",
            "mac_address": "00:01:02:03:04:05",
            "base_name": "x86-bios-tftp",
            "ip_address": "10.0.0.42",
            "tags": []
        }, update_if_already_exists=False)

    # X86 UEFI boot
    request = MagicMock(architecture=CPUArch.X86, firmware=Firmware.UEFI,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == IPXE_BINARIES['IPXE_I386_EFI_FILENAME']

    # X86_64 UEFI boot
    request = MagicMock(architecture=CPUArch.X86_64, firmware=Firmware.UEFI,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == IPXE_BINARIES['IPXE_X86_64_EFI_FILENAME']

    # ARM32 UEFI boot
    request = MagicMock(architecture=CPUArch.ARM32, firmware=Firmware.UEFI,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == IPXE_BINARIES['IPXE_ARM32_EFI_FILENAME']

    # ARM64 UEFI boot
    request = MagicMock(architecture=CPUArch.ARM64, firmware=Firmware.UEFI,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == IPXE_BINARIES['IPXE_ARM64_EFI_FILENAME']

    # ARM32 U-Boot boot
    request = MagicMock(architecture=CPUArch.ARM32, firmware=Firmware.UBOOT,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == "/dyn/bootloader/u-boot/ARM32/00:01:02:03:04:05/boot.scr"

    # ARM64 U-Boot boot
    request = MagicMock(architecture=CPUArch.ARM64, firmware=Firmware.UBOOT,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) == "/dyn/bootloader/u-boot/ARM64/00:01:02:03:04:05/boot.scr"

    # Unsupported Architecture
    request = MagicMock(architecture=CPUArch.RISCV32, firmware=Firmware.BIOS,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) is None
    dhcp.logger.error.assert_called_once_with("Unsupported architecture 'RISCV32'")
    dhcp.logger.error.reset_mock()

    # Unsupported Architecture for BIOS
    request = MagicMock(architecture=CPUArch.ARM32, firmware=Firmware.BIOS,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) is None
    dhcp.logger.error.assert_called_once_with("Unsupported BIOS architecture 'ARM32'")
    dhcp.logger.error.reset_mock()

    # Unsupported Protocol
    request = MagicMock(architecture=CPUArch.X86, firmware=Firmware.UEFI,
                        protocol=BootProtocol.HTTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) is None
    dhcp.logger.error.assert_called_once_with("Unsupported protocol 'HTTP'")
    dhcp.logger.error.reset_mock()

    # Unsupported Firmware
    request = MagicMock(architecture=CPUArch.X86, firmware=Firmware.RPI,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"))
    assert dhcp.boot_target(request) is None
    dhcp.logger.error.assert_called_once_with("Unsupported firmware type 'RPI'")
    dhcp.logger.error.reset_mock()

    # iPXE request on X86/BIOS/TFTP
    request = MagicMock(architecture=CPUArch.X86, firmware=Firmware.BIOS,
                        protocol=BootProtocol.TFTP, mac_addr=MacAddress("00-01-02-03-04-05"),
                        user_class="iPXE")
    assert (dhcp.boot_target(request) ==
            "http://ci-gateway/boot/00:01:02:03:04:05/boot.ipxe?platform=pcbios&buildarch=i386")


def test_ipxe_boot_script(tmp_path, monkeypatch):
    service = create_boot_service(tmp_path)

    # Set the default boot configuration
    expected_boot_cfg = BootConfig(kernel="default_kernel",
                                   initrd="default_initrd",
                                   cmdline="default_cmdline")
    monkeypatch.setenv("BOOTS_DEFAULT_KERNEL", expected_boot_cfg.kernel)
    monkeypatch.setenv("BOOTS_DEFAULT_INITRD", expected_boot_cfg.initrd)
    monkeypatch.setenv("BOOTS_DEFAULT_CMDLINE", expected_boot_cfg.cmdline)

    # Check that when no machines are specified, we use the default boot configuration
    service._gen_ipxe_boot_script = MagicMock()
    service.ipxe_boot_script(machine=None)
    service._gen_ipxe_boot_script.assert_called_once_with(expected_boot_cfg, platform=None)

    # Check that we use the bootconfig when defined
    service._gen_ipxe_boot_script = MagicMock()
    machine = MagicMock()
    platform = MagicMock()
    buildarch = MagicMock()
    service.ipxe_boot_script(machine=machine, platform=platform, buildarch=buildarch)
    machine.boot_config_query.assert_called_with(platform=platform, buildarch=buildarch, bootloader="ipxe")


class UbootTestingMars(MagicMock):
    def get_machine_by_id(self, machine_id, raise_if_missing=False):
        if machine_id == "none":
            return None

        return self.machine_mock


def test_uboot_boot_script(tmp_path, monkeypatch):
    service = create_boot_service(tmp_path)

    service.mars = UbootTestingMars()

    # Set the default boot configuration
    expected_boot_cfg = BootConfig(kernel="default_kernel",
                                   initrd="default_initrd",
                                   cmdline="default_cmdline")
    monkeypatch.setenv("BOOTS_DEFAULT_KERNEL", expected_boot_cfg.kernel)
    monkeypatch.setenv("BOOTS_DEFAULT_INITRD", expected_boot_cfg.initrd)
    monkeypatch.setenv("BOOTS_DEFAULT_CMDLINE", expected_boot_cfg.cmdline)

    # Check that when no machines is invalid, we use the default boot configuration
    service._gen_uboot_boot_script = MagicMock(return_value="default_script")
    service.uboot_boot_script(machine_id="none")
    service._gen_uboot_boot_script.assert_called_once_with(expected_boot_cfg, platform="uboot")

    # Check that we use the bootconfig when defined
    service._gen_uboot_boot_script = MagicMock(return_value="default_script")
    machine = MagicMock()
    service.mars.machine_mock = machine
    buildarch = MagicMock()
    service.uboot_boot_script(machine_id="00-01-02-03-04-05", buildarch=buildarch)
    machine.boot_config_query.assert_called_with(platform="uboot", buildarch=buildarch, bootloader="uboot")

    for name in [CPUArch.ARM32.name, CPUArch.ARM64.name,
                 CPUArch.X86.name, CPUArch.X86_64.name,
                 CPUArch.RISCV32.name, CPUArch.RISCV64.name]:
        service.uboot_boot_script(machine_id="00-01-02-03-04-05", buildarch=name)
        machine.boot_config_query.assert_called_with(platform="uboot", buildarch=name, bootloader="uboot")


def test_platform_cmdline():
    assert BootService._platform_cmdline() == ""
    assert BootService._platform_cmdline(platform="efi") == "initrd=initrd"
    assert BootService._platform_cmdline(platform="pcbios") == ""


def test_gen_ipxe_boot_script():
    BootService._platform_cmdline = MagicMock(return_value="platform_args")

    script = BootService._gen_ipxe_boot_script(BootConfig(kernel="/kernel", initrd="/initrd", cmdline="cmdline"))
    assert "kernel /kernel platform_args cmdline\n" in script
    assert "initrd --name initrd /initrd\n" in script
    assert "boot\n" in script


def test_gen_uboot_boot_script():
    BootService._platform_cmdline = MagicMock(return_value="platform_args")

    script = BootService._gen_uboot_boot_script(BootConfig(kernel="/kernel", initrd="/initrd", cmdline="cmdline",
                                                           dtb="/dtb"))
    assert "tftp ${kernel_addr_r} minio/kernel\n" in script
    assert "tftp ${ramdisk_addr_r} minio/initrd\n" in script
    assert "tftp ${fdt_addr} minio/dtb\n" in script
    assert "booti ${kernel_addr_r} ${ramdisk_addr_r}:${ramdisk_size} ${fdt_addr}\n" in script


def test_default_boot_config(monkeypatch):
    # Check what happens without boot configs
    with pytest.raises(ValueError, match="No default kernel found.*"):
        BootConfig.defaults()
    monkeypatch.setenv("BOOTS_DEFAULT_KERNEL", "default_kernel")
    with pytest.raises(ValueError, match="No default initramfs found.*"):
        BootConfig.defaults()
    monkeypatch.setenv("BOOTS_DEFAULT_INITRD", "default_initrd")
    with pytest.raises(ValueError, match="No default kernel command line found.*"):
        BootConfig.defaults()
    monkeypatch.setenv("BOOTS_DEFAULT_CMDLINE", "default_cmdline")

    # Basic test
    b = BootConfig.defaults()
    assert b == BootConfig(kernel="default_kernel", initrd="default_initrd", cmdline="default_cmdline")

    # Test more complex configurations
    monkeypatch.setenv("BOOTS_DEFAULT_IPXE_X86_64_EFI_KERNEL", "ipxe_x86_64_efi_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_X86_64_EFI_KERNEL", "x86_64_efi_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_IPXE_X86_64_KERNEL", "ipxe_x86_64_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_X86_64_KERNEL", "x86_64_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_IPXE_KERNEL", "ipxe_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_X86_64_INITRD", "ipxe_x86_64_initrd")
    monkeypatch.setenv("BOOTS_DEFAULT_IPXE_ARM64_PCBIOS_KERNEL", "ipxe_arm64_pcbios_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_ARM64_EFI_INITRD", "arm64_efi_initrd")
    monkeypatch.setenv("BOOTS_DEFAULT_ARM64_CMDLINE", "arm64_cmdline")

    b = BootConfig.defaults(bootloader="ipxe", buildarch="x86_64", platform="efi")
    assert b == BootConfig(kernel="ipxe_x86_64_efi_kernel", initrd="ipxe_x86_64_initrd", cmdline="default_cmdline")

    b = BootConfig.defaults(buildarch="x86_64", platform="efi")
    assert b == BootConfig(kernel="x86_64_efi_kernel", initrd="ipxe_x86_64_initrd", cmdline="default_cmdline")

    b = BootConfig.defaults(buildarch="x86_64")
    assert b == BootConfig(kernel="x86_64_kernel", initrd="ipxe_x86_64_initrd", cmdline="default_cmdline")

    b = BootConfig.defaults(bootloader="ipxe")
    assert b == BootConfig(kernel="ipxe_kernel", initrd="default_initrd", cmdline="default_cmdline")

    # Check that BOOTS_DEFAULT_IPXE_ARM64_PCBIOS_KERNEL is not accidentally picked
    b = BootConfig.defaults(bootloader="uboot", buildarch="arm64", platform="efi")
    assert b == BootConfig(kernel="default_kernel", initrd="arm64_efi_initrd", cmdline="arm64_cmdline")


def test_fixup_missing_fields_with_defaults(monkeypatch):
    def empty_boot_cfg():
        return BootConfig(kernel=None, initrd=None, cmdline=None)

    # Check what happens without boot configs
    with pytest.raises(ValueError, match="No default kernel found.*"):
        empty_boot_cfg().fixup_missing_fields_with_defaults()
    monkeypatch.setenv("BOOTS_DEFAULT_KERNEL", "default_kernel")
    with pytest.raises(ValueError, match="No default initramfs found.*"):
        empty_boot_cfg().fixup_missing_fields_with_defaults()
    monkeypatch.setenv("BOOTS_DEFAULT_INITRD", "default_initrd")

    # Basic test
    bcfg = empty_boot_cfg()
    bcfg.fixup_missing_fields_with_defaults()
    assert bcfg == BootConfig(kernel="default_kernel", initrd="default_initrd", cmdline=None)

    # Test more complex configurations
    monkeypatch.setenv("BOOTS_DEFAULT_IPXE_X86_64_EFI_KERNEL", "ipxe_x86_64_efi_kernel")
    monkeypatch.setenv("BOOTS_DEFAULT_X86_64_INITRD", "ipxe_x86_64_initrd")
    monkeypatch.setenv("BOOTS_DEFAULT_CMDLINE", "cmdline")

    # Make sure both the kernel and initrd get updated, but not the commandline
    bcfg = empty_boot_cfg()
    bcfg.fixup_missing_fields_with_defaults(bootloader="ipxe", buildarch="x86_64", platform="efi")
    assert bcfg == BootConfig(kernel="ipxe_x86_64_efi_kernel", initrd="ipxe_x86_64_initrd", cmdline=None)
