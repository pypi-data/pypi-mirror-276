#
# The MIT License (MIT)
#
# Copyright (c) 2015 PsychoMario (imported from PyPXE)
# Copyright (c) 2023 Martin Roukala
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from functools import cached_property
from enum import Enum, auto
import fcntl
import traceback
import socket
import struct
import logging
import re
from collections import defaultdict
from time import time


class MacAddress:
    def __init__(self, macaddr):
        if isinstance(macaddr, bytes):
            self.as_bytes = macaddr
        elif isinstance(macaddr, str):
            self.as_bytes = self.from_human(macaddr)
        else:
            raise ValueError(f"Unknown type {type(macaddr)}")

        # Now that we decoded the mac address, let's generate a uniform mac address
        self.as_str = self.to_human(self.as_bytes)

    @classmethod
    def to_human(cls, raw_mac):
        '''
            This method converts the MAC Address from binary to
            human-readable format for logging.
        '''
        return ':'.join(map(lambda x: hex(x)[2:].zfill(2), struct.unpack('BBBBBB', raw_mac)))

    @classmethod
    def from_human(cls, mac_addr):
        m = re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$",
                     mac_addr.lower())
        if not m:
            raise ValueError(f"{mac_addr} is not a valid mac address")
        else:
            delim = m.groups()[0]
            if delim:
                mac_bytes_list = mac_addr.split(delim)
            else:
                mac_bytes_list = [mac_addr[i:i+2] for i in range(0, len(mac_addr), 2)]

            return bytes.fromhex(" ".join(mac_bytes_list))

    def __str__(self):
        return self.as_str

    def __hash__(self):
        return hash(self.as_bytes)

    def __eq__(self, other):
        return self.as_bytes == other.as_bytes


class DhcpRequestType53(Enum):
    DISCOVER = 1
    REQUEST = 3

    @property
    def response_value(self):
        if self.name == "DISCOVER":
            return 2  # OFFER
        elif self.name == "REQUEST":
            return 5  # ACK


class CPUArch(Enum):
    X86 = auto()
    X86_64 = auto()
    ARM32 = auto()
    ARM64 = auto()
    RISCV32 = auto()
    RISCV64 = auto()

    @property
    def to_ipxe_buildarch(self):
        if self == CPUArch.X86:
            return "i386"
        elif self in [CPUArch.X86_64, CPUArch.ARM32, CPUArch.ARM64]:
            return self.name.lower()
        else:
            return None

    def __str__(self):
        return self.name


class Firmware(Enum):
    BIOS = auto()
    UEFI = auto()
    UBOOT = auto()
    RPI = auto()

    @property
    def to_ipxe_platform(self):
        if self == Firmware.UEFI:
            return "efi"
        elif self == Firmware.BIOS:
            return "pcbios"
        else:
            return None

    def __str__(self):
        return self.name


class BootProtocol(Enum):
    TFTP = auto()
    HTTP = auto()

    def __str__(self):
        return self.name


class ClientRequest:
    def __init__(self, raw_request):
        self.raw_request = raw_request

        # Parse the architecture field (Opt93)
        self.architecture = self.firmware = self.protocol = None
        if decoded_arch := self.client_system_architecture:
            self.architecture, self.firmware, self.protocol = decoded_arch

    @cached_property
    def client_system_architecture_id(self):
        if opt93 := self.raw_dhcp_options.get(93):
            assert len(opt93) == 2
            [arch] = struct.unpack("!H", self.raw_dhcp_options[93])
            return arch

    @cached_property
    def client_system_architecture(self):
        if self.client_system_architecture_id is not None:
            # DHCPv4 and v6 are supposed to have the same archicture mapping,
            # but they ended up disagreeing on whether EFI x86-64 was ID 7 or 9,
            # and it doesn't seem like it got clarified[3]. Given how unlikely
            # bytecode EFI implementations are, let's just pretend both are EFI
            # x86-64 :)
            # [1]: https://www.rfc-editor.org/rfc/rfc4578#section-2.1
            # [2]: https://www.iana.org/assignments/dhcpv6-parameters/dhcpv6-parameters.xhtml#processor-architecture
            # [3]: https://www.syslinux.org/archives/2014-October/022684.html
            known_architectures = {
                # X86 (TFTP)
                0x00: (CPUArch.X86, Firmware.BIOS, BootProtocol.TFTP),
                0x06: (CPUArch.X86, Firmware.UEFI, BootProtocol.TFTP),
                0x07: (CPUArch.X86_64, Firmware.UEFI, BootProtocol.TFTP),
                0x09: (CPUArch.X86_64, Firmware.UEFI, BootProtocol.TFTP),

                # ARM 32-64 (TFTP)
                0x0a: (CPUArch.ARM32, Firmware.UEFI, BootProtocol.TFTP),
                0x0b: (CPUArch.ARM64, Firmware.UEFI, BootProtocol.TFTP),

                # HTTP Boot
                0x0f: (CPUArch.X86, Firmware.UEFI, BootProtocol.HTTP),
                0x10: (CPUArch.X86_64, Firmware.UEFI, BootProtocol.HTTP),
                0x12: (CPUArch.ARM32, Firmware.UEFI, BootProtocol.HTTP),
                0x13: (CPUArch.ARM64, Firmware.UEFI, BootProtocol.HTTP),
                0x14: (CPUArch.X86, Firmware.BIOS, BootProtocol.HTTP),

                # ARM 32-64 U-boot (TFTP & HTTP)
                0x15: (CPUArch.ARM32, Firmware.UBOOT, BootProtocol.TFTP),
                0x16: (CPUArch.ARM64, Firmware.UBOOT, BootProtocol.TFTP),
                0x17: (CPUArch.ARM32, Firmware.UBOOT, BootProtocol.HTTP),
                0x18: (CPUArch.ARM64, Firmware.UBOOT, BootProtocol.HTTP),

                # RISC-V EFI (TFTP & HTTP)
                0x19: (CPUArch.RISCV32, Firmware.UEFI, BootProtocol.TFTP),
                0x1a: (CPUArch.RISCV32, Firmware.UEFI, BootProtocol.HTTP),
                0x1b: (CPUArch.RISCV64, Firmware.UEFI, BootProtocol.TFTP),
                0x1c: (CPUArch.RISCV64, Firmware.UEFI, BootProtocol.HTTP),

                # Raspberry Pi 4 / CM4 (may be limited to IPv6)
                0x29: (CPUArch.ARM64, Firmware.RPI, BootProtocol.TFTP),
            }

            return known_architectures.get(self.client_system_architecture_id)

    @property
    def requested_fields(self):
        return set(self.raw_dhcp_options.get(55, b''))

    @property
    def is_valid_netboot_request(self):
        ''' Verify that all the mandatory fields are present, as mandated by rfc4578 '''

        if 93 not in self.raw_dhcp_options:
            # We are not given the client architecture ID, we can't know what to send!
            return False
        elif not self.requested_fields.issuperset({67}) and self.firmware != Firmware.UBOOT:
            # We are not asked for the boot target, sounds really fishy
            # U-Boot doesn't include this option, but is happy to process it,
            # so allow it just for U-Boot.
            return False
        else:
            return True

        # The following *are* mandated by the spec, but many implementations don't actually
        # provide them. So let's be defensive, and only require fields that we *need* as
        # DHCP clients will ignore
        #
        # if not self.requested_fields.issuperset({128, 129, 130, 131, 132, 133, 134, 135}):
        #     return False
        # elif 94 not in self.raw_dhcp_options:
        #     return False
        # elif 97 not in self.raw_dhcp_options:
        #     return False

    @cached_property
    def mac_addr(self):
        [client_mac] = struct.unpack('!28x6s', self.raw_request[:34])
        return MacAddress(client_mac)

    @cached_property
    def raw_dhcp_options(self):
        '''Parse a string of TLV-encoded options.'''
        raw = self.raw_request[240:]
        ret = {}
        while raw:
            [tag] = struct.unpack('B', raw[0:1])
            if tag == 0:       # padding
                raw = raw[1:]
                continue
            if tag == 255:     # end marker
                break
            [length] = struct.unpack('B', raw[1:2])
            value = raw[2:2 + length]
            raw = raw[2 + length:]
            ret[tag] = value
        return ret

    @cached_property
    def req_type(self):
        if opt53 := self.raw_dhcp_options.get(53):
            return DhcpRequestType53(ord(opt53))  # see RFC2131, page 10

    def __opt_to_str(self, opt):
        if val := self.raw_dhcp_options.get(opt):
            return val.decode('ascii')
        return None

    @cached_property
    def vendor_class(self):
        return self.__opt_to_str(60)

    @cached_property
    def user_class(self):
        return self.__opt_to_str(77)

    def __str__(self):
        mac_addr = self.mac_addr.as_str

        if self.req_type is None:  # pragma: nocover
            return f"InvalidDHCPRequest<{mac_addr}>"
        req_type = self.req_type.name

        vendor_class = self.vendor_class
        user_class = self.user_class
        str_class = user_class if user_class else vendor_class

        details = ""
        if self.client_system_architecture:
            arch = self.architecture.name
            firmware = self.firmware.name
            protocol = self.protocol.name
            details = f" ({arch}/{firmware}/{protocol})"

        return f"DHCP{req_type}<{mac_addr}/{str_class}{details}>"


class OutOfLeasesError(Exception):
    pass


class DHCPD:
    # Callbacks that should be implemented by the user
    @property
    def static_clients(self):  # pragma: nocover
        """" Return here a dictionary that maps a client MAC address to it
        Example: [{"mac_addr": "00:01:02:03:04:05", "ipaddr": "10.0.0.1"}}]
        """

        return []

    def boot_target(self, client_request):  # pragma: nocover
        raise NotImplementedError

    # Implementation details

    '''
        This class implements a DHCP Server, limited to PXE options.
        Implemented from RFC2131, RFC2132,
        https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol,
        and http://www.pix.net/software/pxeboot/archive/pxespec.pdf.
    '''
    def __init__(self, interface, **kwargs):
        self.interface = interface
        self.broadcast = '255.255.255.255'

        self.router = kwargs.get('router', self.ip)
        self.dns_servers = kwargs.get('dns_servers', ["9.9.9.9"])
        self.file_server = kwargs.get('file_server', self.ip)   # TFTP / HTTP Server
        self.lease_time = kwargs.get('lease_time', 86400)

        self.logger = kwargs.get('logger', None)

        # setup logger
        if self.logger is None:
            self.logger = logging.getLogger('DHCP')
            self.logger.propagate = False
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        # In-memory storage of leases, using the MAC address as a key
        self.leases = defaultdict(lambda: {'ip': '', 'expire': 0})

    @classmethod
    def __iface_query_param(cls, iface, param):
        # Implementation from:
        # https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                return socket.inet_ntop(socket.AF_INET,
                                        fcntl.ioctl(s.fileno(), param,
                                                    struct.pack('256s',
                                                                iface.encode('utf8'))
                                                    )[20:24])
            except OSError:
                # Iface doesn't exist, or no IP assigned
                raise ValueError(f"The interface {iface} has no IP assigned") from None

    @property
    def ip(self):
        """" Returns the ipv4 address, or None if the iface is unavailable or has
        no IP assigned."""
        return self.__iface_query_param(self.interface, 0x8915)  # SIOCGIFADDR

    @property
    def netmask(self):
        """" Returns the ipv4 netmask, or None if the iface is unavailable or has
        no IP assigned."""
        return self.__iface_query_param(self.interface, 0x891b)  # SIOCGIFNETMASK

    def find_first_available_ip(self):
        '''
            This method returns the next unleased IP from range;
            also does lease expiry by overwrite.
        '''

        # If we use ints, we don't have to deal with octet overflow
        # or nested loops (up to 3 with 10/8); convert both to 32-bit integers
        # e.g '192.168.1.1' <-> 3232235777
        def encode(x):
            return struct.unpack('!I', socket.inet_aton(x))[0]

        def decode(x):
            return socket.inet_ntoa(struct.pack('!I', x))

        # Use the current network settings to identify the list of valid IPs
        nmask = encode(self.netmask)
        network = encode(self.ip) & nmask
        from_host = network + 1
        to_host = (network | ((~ nmask) & 0xffffffff)) - 1

        # Create the list of used IP addresses
        reserved = [self.leases[i]['ip'] for i in self.leases if self.leases[i]['expire'] > time()]
        reserved.extend([c["ipaddr"] for c in self.static_clients if "ipaddr" in c])
        reserved.append(self.ip)                # pull out our own IP
        reserved = list(map(encode, reserved))  # convert to 32-bit int

        # loop through, make sure not already reserved and not in form X.Y.Z.0
        for offset in range(to_host - from_host):
            cur_addr = from_host + offset
            if cur_addr % 256 and cur_addr not in reserved:
                return decode(cur_addr)

        # Couldn't find any available IP, bail out!
        raise OutOfLeasesError('Ran out of IP addresses to lease!')  # pragma: nocover

    def get_or_assign_ip_for_client(self, client_mac):
        # Use the defined static IP, if available
        for client in self.static_clients:
            if client.get("mac_addr") == client_mac:
                return client.get("ipaddr"), "static client"

        # Re-use an existing lease, if we do have one
        if self.leases[client_mac]['ip'] and self.leases[client_mac]['expire'] > time():
            return self.leases[client_mac]['ip'], "rebinding lease"

        # Find the first available IP
        return self.find_first_available_ip(), "new client"

    @classmethod
    def tlv_encode(cls, tag, value):
        '''Encode a TLV option.'''
        if isinstance(value, str):
            value = value.encode('ascii')
        value = bytes(value)
        return struct.pack('BB', tag, len(value)) + value

    def craft_response(self, client_request, offer, boot_target):
        '''This method crafts the full response to the request'''

        # The header
        xid, _, _, _, chaddr = struct.unpack('!4x4s2x2s4x4s4x4s16s', client_request.raw_request[:44])
        response = struct.pack('!BBBB4s',
                               2,                      # Boot reply
                               1,                      # Hardware type: Ethernet
                               6,                      # MAC Address length
                               0,                      # Hops
                               xid)                    # Transaction ID (copied from the request)

        response += struct.pack('!HHI', 0, 0x8000, 0)  # BOOTP flags (Broadcast = 1)

        response += socket.inet_aton(offer)            # Client IP address

        response += socket.inet_aton(self.ip)          # Server IP address
        response += socket.inet_aton('0.0.0.0')        # Relay Agent IP (N/A)
        response += chaddr                             # Client MAC address

        # BOOTP legacy pad
        response += b'\x00' * 64                       # server name
        response += b'\x00' * 128                      # filename
        response += struct.pack('!I', 0x63825363)      # magic cookie

        # The DHCP options
        response += self.tlv_encode(53, struct.pack('!B',
                                                    client_request.req_type.response_value))  # message type
        response += self.tlv_encode(54, socket.inet_aton(self.ip))                            # DHCP Server

        # IP/network configuration
        response += self.tlv_encode(1, socket.inet_aton(self.netmask))                        # subnet mask
        response += self.tlv_encode(3, socket.inet_aton(self.router))                         # router
        dns_servers = b''.join([socket.inet_aton(i) for i in self.dns_servers])
        response += self.tlv_encode(6, dns_servers)                                           # DNS Servers
        response += self.tlv_encode(51, struct.pack('!I', self.lease_time))                   # lease time

        # If we have a boot target / filename, let's send the needed parameters
        if boot_target:
            response += self.tlv_encode(66, self.file_server)                                 # TFTP/HTTP Server
            response += self.tlv_encode(67, boot_target.encode('ascii') + b'\x00')

        response += b'\xff'
        return response

    # TODO: Add tests for this function
    def listen(self, sock=None):  # pragma: nocover
        '''Main listen loop.'''
        def main_loop(sock):
            while True:
                self.current_request = None
                try:
                    raw_request, _ = sock.recvfrom(1024)

                    # Parse the request
                    self.current_request = ClientRequest(raw_request=raw_request)
                    self.logger.info(f"Received the request {str(self.current_request)}")

                    # Find or assign an IP for the client
                    offer, offer_reason = self.get_or_assign_ip_for_client(self.current_request.mac_addr)
                    self.leases[self.current_request.mac_addr]['ip'] = offer
                    self.leases[self.current_request.mac_addr]['expire'] = time() + self.lease_time

                    # Get the expected boot target
                    boot_target = None
                    if self.current_request.is_valid_netboot_request:
                        boot_target = self.boot_target(self.current_request)

                    self.logger.info(f"Offering IP {offer} ({offer_reason}), boot target {boot_target}")

                    # Generate the response
                    if response := self.craft_response(self.current_request, offer, boot_target):
                        sock.sendto(response, (self.broadcast, 68))
                except Exception:
                    self.logger.error(f"Exception caught:\n{traceback.format_exc()}")

        # Use the provided socket if specified, or create our own
        if sock:
            main_loop(sock)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:  # IPv4 UDP socket
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow quick rebinding after restart
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Allow sending packets to a broadcast addr
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BINDTODEVICE,  # Only listen to msgs from the wanted iface
                                self.interface.encode())
                sock.bind(('', 67))                                         # Bind to port 67

                main_loop(sock)
