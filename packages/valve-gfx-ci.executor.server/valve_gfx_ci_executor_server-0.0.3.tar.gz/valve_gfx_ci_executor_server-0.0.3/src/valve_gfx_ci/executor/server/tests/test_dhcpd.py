from server.dhcpd import MacAddress, DhcpRequestType53, CPUArch, Firmware, BootProtocol, ClientRequest, DHCPD
import binascii
import pytest
import time


def test_MacAddress_colon_separated():
    assert MacAddress('00:01:02:03:04:05').as_bytes == b'\x00\x01\x02\x03\x04\x05'


def test_MacAddress_dash_separated():
    assert MacAddress('00-01-02-03-04-05').as_bytes == b'\x00\x01\x02\x03\x04\x05'


def test_MacAddress_no_separator():
    assert MacAddress('000102030405').as_bytes == b'\x00\x01\x02\x03\x04\x05'


def test_MacAddress_too_long():
    with pytest.raises(ValueError):
        MacAddress('00:01:02:03:04:05:06')


def test_MacAddress_too_short():
    with pytest.raises(ValueError):
        MacAddress('00:01:02:03:04')


def test_MacAddress_bad_separator():
    with pytest.raises(ValueError):
        MacAddress('00:01:02:03:04?05')


def test_MacAddress_invalid():
    with pytest.raises(ValueError):
        MacAddress('garbage')


def test_MacAddress_invalid_type():
    with pytest.raises(ValueError):
        MacAddress([])


def test_MacAddress_identity():
    mac_addr = MacAddress('00:01:02:03:04:05')
    assert MacAddress(mac_addr.as_bytes) == mac_addr
    assert MacAddress(str(mac_addr)) == mac_addr
    assert hash(MacAddress(str(mac_addr))) == hash(mac_addr)


def test_DhcpRequestType53_response_value():
    # DISCOVER --> OFFER
    assert DhcpRequestType53.DISCOVER.response_value == 2

    # REQUEST --> ACK
    assert DhcpRequestType53.REQUEST.response_value == 5


def test_CPUArch_str():
    assert str(CPUArch.RISCV32) == "RISCV32"


def test_CPUArch_ipxe_buildarch():
    assert CPUArch.X86.to_ipxe_buildarch == "i386"
    assert CPUArch.X86_64.to_ipxe_buildarch == "x86_64"
    assert CPUArch.ARM32.to_ipxe_buildarch == "arm32"
    assert CPUArch.ARM64.to_ipxe_buildarch == "arm64"

    # No targets available
    assert CPUArch.RISCV32.to_ipxe_buildarch is None
    assert CPUArch.RISCV64.to_ipxe_buildarch is None


def test_Firmware_str():
    assert str(Firmware.UBOOT) == "UBOOT"


def test_Firmware_ipxe_buildarch():
    assert Firmware.BIOS.to_ipxe_platform == "pcbios"
    assert Firmware.UEFI.to_ipxe_platform == "efi"
    assert Firmware.UBOOT.to_ipxe_platform is None
    assert Firmware.RPI.to_ipxe_platform is None


def test_BootProtocol_str():
    assert str(BootProtocol.TFTP) == "TFTP"


X86_TFTP_DISCOVER = binascii.unhexlify((
    '0101060026f303390000000000000000000000000000000000000000b827eb9b65d4000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000063825363350101370e2b3c4380818283848586874201035d'
    '0200005e03010201611100d4659bbdd4659bbdd4659bbdd4659bbd3c20505845436c69656e743a417263683a30303030303a554e'
    '44493a303032303031ff').encode())


X86_64_HTTP_DISCOVER = binascii.unhexlify((
    '010106009d9ff879000480000000000000000000000000000000000060beb4061337000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000063825363350101390205c0371b0102030405060c0d0f1112'
    '16171c28292a2b3233363a3b3ccc4361611100000200030004000500060007000800095e030103105d0200103c2148545450436c'
    '69656e743a417263683a30303031363a554e44493a303033303136ff').encode())


ARMv8_UBOOT_TFTP = binascii.unhexlify((
    '0101060001d045a70003000000000000000000000000000000000000e45f01d02af3000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000638253633501033902024036040a00000132040a0000135d'
    '0200165e030100003c0c552d426f6f742e61726d763837050103060c11ff00000000000000000000').encode())


# NOTE: This is a rebinding request from NetworkManager on my desktop PC, with an added padding DHCP option at the top
SIMPLE_DHCP_REQUEST = binascii.unhexlify((
    '0101060031fb9b3600010000000000000000000000000000000000001c61b463ba2c000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000063825363003501033d07011c61b463ba2c37110102060c0f'
    '1a1c79032128292a77f9fc11390202403204c0a800210c0a6d757075663539353078ff').encode())

# Manually crafted to include option 93, but still fail the is_valid_netboot_request check
SIMPLE2_DHCP_REQUEST = binascii.unhexlify((
    '0101060031fb9b3600010000000000000000000000000000000000001c61b463ba2c000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    '0000000000000000000000000000000000000000000000000000000063825363003501033d07011c61b463ba2c37110102060c0f'
    '1a1c79032128292a77f9fc11390202403204c0a800210c0a6d7570756635393530785d020010ff').encode())


def test_ClientRequest_basic_x86_tftp():
    req = ClientRequest(X86_TFTP_DISCOVER)
    assert req.client_system_architecture_id == 0
    assert req.architecture == CPUArch.X86
    assert req.firmware == Firmware.BIOS
    assert req.protocol == BootProtocol.TFTP
    assert req.requested_fields == {1, 3, 43, 60, 66, 67, 128, 129, 130, 131, 132, 133, 134, 135}
    assert req.is_valid_netboot_request
    assert req.req_type == DhcpRequestType53.DISCOVER
    assert req.vendor_class == "PXEClient:Arch:00000:UNDI:002001"
    assert req.user_class is None
    assert str(req) == "DHCPDISCOVER<b8:27:eb:9b:65:d4/PXEClient:Arch:00000:UNDI:002001 (X86/BIOS/TFTP)>"


def test_ClientRequest_x86_64_http_netboot():
    req = ClientRequest(X86_64_HTTP_DISCOVER)
    assert req.client_system_architecture_id == 16
    assert req.architecture == CPUArch.X86_64
    assert req.firmware == Firmware.UEFI
    assert req.protocol == BootProtocol.HTTP
    assert req.requested_fields == {1, 2, 3, 4, 5, 6, 12, 13, 15, 17, 18, 22, 23, 28, 40, 41, 42, 43, 50, 51, 54, 58,
                                    59, 60, 67, 97, 204}
    assert req.is_valid_netboot_request
    assert req.req_type == DhcpRequestType53.DISCOVER
    assert req.vendor_class == "HTTPClient:Arch:00016:UNDI:003016"
    assert req.user_class is None
    assert str(req) == "DHCPDISCOVER<60:be:b4:06:13:37/HTTPClient:Arch:00016:UNDI:003016 (X86_64/UEFI/HTTP)>"


def test_ClientRequest_armv8_uboot_tftp():
    req = ClientRequest(ARMv8_UBOOT_TFTP)
    assert req.client_system_architecture_id == 22
    assert req.architecture == CPUArch.ARM64
    assert req.firmware == Firmware.UBOOT
    assert req.protocol == BootProtocol.TFTP
    assert req.requested_fields == {1, 3, 6, 12, 17}
    assert req.is_valid_netboot_request
    assert req.req_type == DhcpRequestType53.REQUEST
    assert req.vendor_class == "U-Boot.armv8"
    assert req.user_class is None
    assert str(req) == "DHCPREQUEST<e4:5f:01:d0:2a:f3/U-Boot.armv8 (ARM64/UBOOT/TFTP)>"


def test_ClientRequest_normal_dhcp_request():
    req = ClientRequest(SIMPLE_DHCP_REQUEST)
    assert req.client_system_architecture_id is None
    assert req.architecture is None
    assert req.firmware is None
    assert req.protocol is None
    assert req.requested_fields == {1, 2, 3, 6, 12, 15, 17, 26, 28, 33, 40, 41, 42, 119, 121, 249, 252}
    assert not req.is_valid_netboot_request
    assert req.req_type == DhcpRequestType53.REQUEST
    assert req.vendor_class is None
    assert req.user_class is None
    assert str(req) == "DHCPREQUEST<1c:61:b4:63:ba:2c/None>"


def test_ClientRequest_normal_with_93_dhcp_request():
    req = ClientRequest(SIMPLE2_DHCP_REQUEST)
    assert req.client_system_architecture_id == 16
    assert req.architecture == CPUArch.X86_64
    assert req.firmware == Firmware.UEFI
    assert req.protocol == BootProtocol.HTTP
    assert req.requested_fields == {1, 2, 3, 6, 12, 15, 17, 26, 28, 33, 40, 41, 42, 119, 121, 249, 252}
    assert not req.is_valid_netboot_request
    assert req.req_type == DhcpRequestType53.REQUEST
    assert req.vendor_class is None
    assert req.user_class is None
    assert str(req) == "DHCPREQUEST<1c:61:b4:63:ba:2c/None (X86_64/UEFI/HTTP)>"


def test_DHCPD_network_detection():
    dhcpd = DHCPD(interface='lo')
    assert dhcpd.ip == '127.0.0.1'
    assert dhcpd.netmask == '255.0.0.0'


def test_DHCPD_network_detection_with_invalid_interface():
    with pytest.raises(ValueError):
        DHCPD(interface='invalid_ip')


def test_DHCPD_ip_allocation():
    class Dhcpd(DHCPD):
        @property
        def static_clients(self):
            return [
                {"mac_addr": "00:01:02:03:04:00", "ipaddr": "127.0.0.2"},
                {"mac_addr": "00:01:02:03:04:01", "ipaddr": "127.0.0.3"},
                {"mac_addr": "00:01:02:03:04:03", "ipaddr": "127.0.0.5"},
            ]

    dhcpd = Dhcpd(interface='lo')

    # Static clients
    assert dhcpd.get_or_assign_ip_for_client("00:01:02:03:04:00") == ('127.0.0.2', "static client")
    assert dhcpd.get_or_assign_ip_for_client("00:01:02:03:04:01") == ('127.0.0.3', "static client")

    # Non-static client keeps getting the same IP back
    assert dhcpd.get_or_assign_ip_for_client("00:01:02:03:04:02") == ('127.0.0.4', "new client")
    dhcpd.leases['00:01:02:03:04:02']['ip'] = '127.0.0.4'
    dhcpd.leases['00:01:02:03:04:02']['expire'] = time.time() + 120
    assert dhcpd.get_or_assign_ip_for_client("00:01:02:03:04:02") == ('127.0.0.4', "rebinding lease")

    # Re-use of a lease by another client when expired
    dhcpd.leases['00:01:02:03:04:02']['expire'] = time.time() - 1
    assert dhcpd.get_or_assign_ip_for_client("00:01:02:03:04:04") == ('127.0.0.4', "new client")


def test_DHCPD_response():
    dhcpd = DHCPD(interface='lo')
    r = dhcpd.craft_response(ClientRequest(ARMv8_UBOOT_TFTP), offer='192.168.42.42', boot_target='my_boot_target')

    # Sanity check that we got the offer and the boot target in the answer
    assert b'my_boot_target' in r
    assert b'\xc0\xa8\x2a\x2a' in r
