from unittest.mock import MagicMock, PropertyMock, patch, call
import io

from server.android.fastbootd import FastbootDevice, Fastbootd

import pytest
import usb.util


@patch("server.android.fastbootd.usb.util.find_descriptor")
@patch("server.android.fastbootd.usb.util.endpoint_type")
@patch("server.android.fastbootd.usb.util.endpoint_direction")
def FastbootDeviceMock(endpoint_direction_mock, endpoint_type_mock, find_descriptor_mock, *args, **kwargs):
    device = MagicMock()
    cfg = MagicMock()
    intf = MagicMock()
    ep_write = MagicMock()
    ep_read = MagicMock()

    device.__iter__.return_value = [cfg]
    find_descriptor_mock.return_value = intf
    intf.__iter__.return_value = [ep_read, ep_write]
    endpoint_type_mock.return_value = usb.util.ENDPOINT_TYPE_BULK
    endpoint_direction_mock.side_effect = [usb.util.ENDPOINT_IN, usb.util.ENDPOINT_OUT]

    fb_dev = FastbootDevice(device, *args, **kwargs)

    find_descriptor_mock.assert_called_once_with(cfg,
                                                 bInterfaceClass=0xff,
                                                 bInterfaceSubClass=0x42,
                                                 bInterfaceProtocol=0x03)
    endpoint_type_mock.assert_any_call(ep_write.bmAttributes)
    endpoint_type_mock.assert_any_call(ep_read.bmAttributes)
    endpoint_direction_mock.assert_any_call(ep_write.bEndpointAddress)
    endpoint_direction_mock.assert_any_call(ep_read.bEndpointAddress)

    return fb_dev


@patch("server.android.fastbootd.usb.core.find")
def test_FastbootDevice__from_serial(find_mock):
    dev0 = MagicMock()
    dev1 = MagicMock(serial_number="0123456789")
    dev2 = MagicMock(serial_number="9876543210")

    # Make the first device always raise an exception when accessing its serial number
    type(dev0).serial_number = PropertyMock(side_effect=ValueError)

    find_mock.return_value = [dev0, dev1, dev2]
    with patch("server.android.fastbootd.FastbootDevice.__init__", return_value=None) as init_mock:
        FastbootDevice.from_serial("9876543210", 42)
        find_mock.assert_called_once_with(find_all=True)
        init_mock.assert_called_once_with(dev2, write_chunk=42)

    with pytest.raises(ValueError):
        FastbootDevice.from_serial("serial", 42)


def test_FastbootDevice__basic_io__read():
    dev = FastbootDeviceMock()
    assert dev.read(1024, timeout=42) == dev.ep_read.read.return_value
    dev.ep_read.read.assert_called_once_with(1024, timeout=42)


def test_FastbootDevice__release():
    dev = FastbootDeviceMock()

    dev.device._ctx.release_all_interfaces.assert_not_called()
    dev.release()
    dev.device._ctx.release_all_interfaces.assert_called_once_with(dev.device)


def test_FastbootDevice__basic_io__write():
    dev = FastbootDeviceMock(write_chunk=2)

    dev.write(b"abcde", timeout=42) == dev.ep_read.read.return_value

    assert dev.ep_write.write.call_count == 3
    dev.ep_write.write.assert_has_calls([call(b"ab", timeout=42), call(b"cd", timeout=42), call(b"e", timeout=42)])


def test_FastbootDevice__runcmd__basic():
    dev = FastbootDeviceMock()
    dev.write = MagicMock()
    dev.read = MagicMock(side_effect=[b"INFOline1", b"INFOline2", b"INFOline3", b"OKAY"])

    dev.run_cmd("cmd", "arg", timeout=1)

    dev.write.assert_called_once_with(b"cmd:arg")
    assert dev.read.call_count == 4
    dev.read.assert_has_calls([call(64, timeout=1), call(64, timeout=1), call(64, timeout=1), call(64, timeout=1)])


def test_FastbootDevice__runcmd__fail():
    dev = FastbootDeviceMock()
    dev.read = MagicMock(return_value=b"FAILcmd failed!")

    with pytest.raises(ValueError):
        dev.run_cmd("cmd")


def test_FastbootDevice__runcmd__unwanted_status():
    dev = FastbootDeviceMock()
    dev.read = MagicMock(return_value=b"DATAcmd failed!")

    with pytest.raises(ValueError):
        dev.run_cmd("cmd", wanted_status="OKAY")


def test_FastbootDevice__getvar():
    dev = FastbootDeviceMock()

    # Missing variable
    dev.run_cmd = MagicMock(return_value=[(None, None)])
    assert dev.getvar("KEY") is None

    # Single variable
    dev.run_cmd = MagicMock(return_value=[(None, b"KEY:VAL"), (None, None)])
    assert dev.getvar("KEY") == "VAL"

    # Multiple variables
    dev.run_cmd = MagicMock(return_value=[(None, b"KEY:VAL"), (None, b"KEY2:VAL2"), (None, None)])
    assert dev.getvar("all") == {"KEY": "VAL", "KEY2": "VAL2"}


def test_FastbootDevice__variables():
    dev = FastbootDeviceMock()

    dev.getvar = MagicMock()
    assert dev.variables == dev.getvar.return_value
    dev.getvar.assert_called_once_with(b"all")


def test_FastbootDevice__upload():
    data = io.BytesIO(b"My data")

    dev = FastbootDeviceMock(write_chunk=2)
    dev.read = MagicMock(side_effect=[b"DATA00000007", b"OKAY"])

    dev.upload(data)

    dev.ep_write.write.assert_has_calls([call(b"My"), call(b" d"), call(b"at"), call(b"a")])


@patch("server.android.fastbootd.usb.core.find")
def test_FastbootDevice__boot(find_mock):
    dev = FastbootDeviceMock()

    dev.run_cmd = MagicMock()
    dev.boot()
    dev.run_cmd.assert_called_once_with(b"boot", timeout=15000)


def FastbootDeviceNewMock(cls, device, **kwargs):
    if device.raises:
        raise ValueError("Mock Error!")

    return MagicMock(device=device, **kwargs)


@patch("server.android.fastbootd.FastbootDevice.__new__", side_effect=FastbootDeviceNewMock)
def test_Fastbootd(fbdev_mock):
    def new_loop(found={}, added=set(), rmed=set()):
        # Mock the callbacks and make them assert to ensure the daemon keeps going no matter what
        daemon.new_device_found = MagicMock(side_effect=AssertionError)
        daemon.device_removed = MagicMock(side_effect=ValueError)

        with patch("server.android.fastbootd.usb.core.find", return_value=found) as find_mock:
            daemon.update_device_list()

            find_mock.assert_called_once_with(find_all=True)
            assert {call.args[0].device for call in daemon.new_device_found.call_args_list} == added
            assert {call.args[0].device for call in daemon.device_removed.call_args_list} == rmed

    daemon = Fastbootd()

    devs = [MagicMock(raises=False) for i in range(3)]
    non_fastbootd_dev = MagicMock(raises=True)

    # Make sure any assert from core find does not get propagated
    with patch("server.android.fastbootd.usb.core.find", side_effect=Exception):
        daemon.update_device_list()

    # First discovery
    new_loop(found=[devs[0], devs[1]], added={devs[0], devs[1]}, rmed=set())

    # No changes but order different
    new_loop(found=[devs[1], devs[0]], added=set(), rmed=set())

    # Remove one, add a new one
    new_loop(found=[devs[2], devs[0]], added={devs[2]}, rmed={devs[1]})

    # Add a non-fastboot device
    new_loop(found=[devs[2], non_fastbootd_dev, devs[0]], added=set(), rmed=set())
