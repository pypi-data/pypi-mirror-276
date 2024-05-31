from collections import namedtuple
from pathlib import Path
from unittest.mock import patch, MagicMock, call

import pytest

from pydantic import ValidationError

from server.pdu import PDUState, PDUPort
from server.pdu.drivers.usbhub import USBHubDevice, USBHubPDU, USBHubDeviceMatchConfig, USBHubPDUConfig


DEFAULT_LOCATION = "usbaddress"


def create_usbhubdevice(tmpdir, location=DEFAULT_LOCATION, controllable_ports={1, 2, 3, 4}, **files):
    base = Path(tmpdir) / location
    base.mkdir(parents=True)

    # Create all the ports
    for port_id in controllable_ports:
        port_path = Path(base / f"{location}:1.0" / f"{location}-port{port_id}" / "disable")
        port_path.parent.mkdir(parents=True, exist_ok=True)
        port_path.write_text("0\n")

    default_files = {
        "maxchild": "4",
        "serial": None,
        "bDeviceClass": "09",
        "speed": "10000",
        "idVendor": "2109",
        "idProduct": "2817",
        "devpath": location,
    }
    for filename, default in default_files.items():
        if value := files.get(filename, default):
            (base / filename).write_text(value + "\n")

    return USBHubDevice(base)


def test_USBHubDevice__not_a_hub(tmpdir):
    with pytest.raises(ValueError) as excinfo:
        create_usbhubdevice(tmpdir, bDeviceClass="08")
    assert f"The USB device at location '{tmpdir / DEFAULT_LOCATION}' is not a USB hub" in str(excinfo)


def test_USBHubDevice__more_than_one_path_to_port_id(tmpdir):
    hub = create_usbhubdevice(tmpdir)
    hub.base_path = MagicMock(glob=MagicMock(return_value=["/path1", "/path2"]))

    with pytest.raises(ValueError) as excinfo:
        hub.port_path(1)
    assert f"Found more than one candidate port for port_id 1 in the hub at location '{hub.base_path}'" in str(excinfo)


def test_USBHubDevice__attributes(tmpdir):
    files = {
        "maxchild": "6",
        "serial": "serial",
        "bDeviceClass": "09",
        "speed": "5000",
        "idVendor": "8086",
        "idProduct": "4242",
        "devpath": DEFAULT_LOCATION,
    }

    hub = create_usbhubdevice(tmpdir, **files)

    for attr, value in files.items():
        if attr in ["maxchild", "speed"]:
            value = int(value)
        elif attr in ["bDeviceClass", "idVendor", "idProduct"]:
            value = int(value, 16)
        assert getattr(hub, attr) == value

    assert hub.controller_path == Path(tmpdir).parent


def test_USBHubDevice__set_port_state(tmpdir):
    hub = create_usbhubdevice(tmpdir)

    with pytest.raises(ValueError) as excinfo:
        hub.set_port_state(1, PDUState.REBOOT)
    assert "Unsupported state REBOOT" in str(excinfo)

    for port, state, expected_value in [(1, PDUState.ON, "0\n"), (2, PDUState.OFF, "1\n")]:
        with patch.object(hub, 'port_path') as port_path_mock:
            hub.set_port_state(port, state)
            port_path_mock.assert_called_once_with(port)
            port_path_mock.return_value.write_text.assert_called_once_with(expected_value)


def test_USBHubDevice__get_port_state(tmpdir):
    hub = create_usbhubdevice(tmpdir)

    for port, file_value, expected_state in [(1, "0\n", PDUState.ON), (2, "1\n", PDUState.OFF)]:
        with patch.object(hub, 'port_path') as port_path_mock:
            port_path_mock.return_value.read_text.return_value = file_value
            assert hub.get_port_state(port) == expected_state
            port_path_mock.assert_called_once_with(port)


def test_USBHubDeviceMatchConfig__invalid_devpath():
    for value in ["yoooo", "1.2.3."]:
        with pytest.raises(ValidationError) as excinfo:
            USBHubDeviceMatchConfig(devpath=value, idVendor=1, idProduct=2)
        assert "The devpath is not a dot-separated list of integer" in str(excinfo._excinfo)


def test_USBHubDeviceMatchConfig__matches():
    fields = dict(devpath="1.2.3", idVendor=42, idProduct=1)

    matcher = USBHubDeviceMatchConfig(**fields)
    assert matcher.matches(MagicMock(**fields))

    matcher = USBHubDeviceMatchConfig(**fields, maxchild=10)
    assert not matcher.matches(MagicMock(**fields))


def test_USBHubPDUConfig__invalid_config():
    with pytest.raises(ValidationError) as excinfo:
        USBHubPDUConfig()

    assert "Neither a `serial` nor the tuple (`controller`, `devices`) was found in the config" in str(excinfo._excinfo)


@patch("server.pdu.drivers.usbhub.USBHubDevice")
def test_USBHubPDUConfig__controller_and_devices(hub_mock, tmpdir):
    USBHubDeviceMock = namedtuple('USBHubDeviceMock', ['devpath'])

    # Check that we enforce that at least one device is set
    with pytest.raises(ValidationError) as excinfo:
        USBHubPDUConfig(controller=str(tmpdir), devices=[])
    assert "At least one device should be set" in str(excinfo._excinfo)

    # Create a list of device matchers that will respectively match any hub
    # that has a devpath == /devpath1 and devpath == /devpath2. We then make
    # sure that the mocked USBHubDevice returns a USBHubDeviceMock where only
    # the devpath is set unless the path is /devpath2 in which case we want to
    # raise an exception to simulate having an invalid hub
    dev_matchs = [
        USBHubDeviceMatchConfig(devpath="1.2.3", idVendor=0x123, idProduct=0x456),
        USBHubDeviceMatchConfig(devpath="2.3.4", idVendor=0x789, idProduct=0x123),
    ]
    dev_matchs[0].matches = MagicMock(side_effect=lambda hub: hub.devpath == "/devpath1")
    dev_matchs[1].matches = MagicMock(side_effect=lambda hub: hub.devpath == "/devpath3")
    hub_mock.side_effect = lambda path: USBHubDeviceMock(path) if path != "/devpath2" else exec("raise ValueError()")

    cfg = USBHubPDUConfig(controller=str(tmpdir), devices=dev_matchs)

    # No devices found in controller
    with pytest.raises(ValueError) as excinfo:
        cfg.hubs
    assert f"Could not find a USB device matching {dev_matchs[0]}" in str(excinfo._excinfo)

    # Right amount of devices found
    with patch.object(cfg, "controller") as controller_mock:
        controller_mock.glob.return_value = ["/devpath1", "/devpath2", "/devpath3"]

        hubs = cfg.hubs

        assert len(hubs) == len(dev_matchs)
        assert hubs[0].devpath == "/devpath1"
        assert hubs[1].devpath == "/devpath3"

        assert controller_mock.glob.call_count == len(dev_matchs)
        for dev_match in dev_matchs:
            controller_mock.glob.assert_any_call(f"usb*/*-{dev_match.devpath}")

    # More than one device returned
    with patch.object(cfg, "controller") as controller_mock:
        controller_mock.glob.return_value = ["/devpath1", "/devpath2", "/devpath3", "/devpath3"]
        with pytest.raises(ValueError) as excinfo:
            cfg.hubs
        assert f"Found more than one USB device match {dev_matchs[1]}" in str(excinfo._excinfo)


@patch("server.pdu.drivers.usbhub.USBHubDevice")
def test_USBHubPDUConfig__serial(hub_mock):
    serial = "serial1"
    parent1 = "/parent1"
    parent2 = "/parent2"

    cfg = USBHubPDUConfig(serial=f" {serial} \n")

    # Make sure that we strip the serial passed as a parameter
    assert cfg.serial == serial

    # Check the error message if no serial devices were found
    with patch.object(cfg, "USB_DEVICES_PATH") as path_mock:
        with pytest.raises(ValueError) as excinfo:
            cfg.hubs

        assert f"No USB Hubs with serial '{serial}' found" in str(excinfo._excinfo)
        path_mock.glob.assert_called_once_with("*/serial")
        hub_mock.assert_not_called()

    with patch.object(cfg, "USB_DEVICES_PATH") as path_mock:
        path_mock.glob.return_value = [
            MagicMock(read_text=MagicMock(return_value="serial0\n")),
            MagicMock(read_text=MagicMock(return_value=f"{serial}")),
            MagicMock(read_text=MagicMock(return_value=f" {serial} \n")),
            MagicMock(read_text=MagicMock(return_value="serial2")),
            MagicMock(read_text=MagicMock(return_value="serial3")),
        ]

        # Assign a parent to the paths of the devices with the right serial
        # NOTE: This could not be done directly inline because MagicMock was
        # interpreting the `parent` parameter as a MagicMock parenthood...
        path_mock.glob.return_value[1].parent = parent1
        path_mock.glob.return_value[2].parent = parent2

        assert len(cfg.hubs) == 2

        path_mock.glob.assert_called_once_with("*/serial")
        assert hub_mock.call_count == 2
        assert hub_mock.call_args_list[0] == call(parent1)
        assert hub_mock.call_args_list[1] == call(parent2)


@patch("server.pdu.drivers.usbhub.USBHubPDUConfig")
def test_USBHubPDU(usbhubcfg_mock):
    config = {"my": "config"}

    # No devices found
    usbhubcfg_mock.return_value.hubs = []
    with pytest.raises(ValueError) as excinfo:
        USBHubPDU("TestPDU", config)
    usbhubcfg_mock.assert_called_once_with(**config)
    assert "No associated hub devices found" in str(excinfo._excinfo)

    # Different controllers
    usbhubcfg_mock.return_value.hubs = [
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=480),
        MagicMock(controller_path="/controller2", ports=[1, 2, 3], speed=5000)
    ]
    with pytest.raises(ValueError) as excinfo:
        USBHubPDU("TestPDU", config)
    assert "Not all hubs are connected to the same USB controller" in str(excinfo._excinfo)

    # Different list of ports
    usbhubcfg_mock.return_value.hubs = [
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=480),
        MagicMock(controller_path="/controller1", ports=[1, 2, 4], speed=5000)
    ]
    with pytest.raises(ValueError) as excinfo:
        USBHubPDU("TestPDU", config)
    assert "Not all hubs agree on the list of ports" in str(excinfo._excinfo)

    # Same speeds
    usbhubcfg_mock.return_value.hubs = [
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=480),
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=480)
    ]
    with pytest.raises(ValueError) as excinfo:
        USBHubPDU("TestPDU", config)
    assert "Some hubs unexpectedly share the same speed" in str(excinfo._excinfo)

    # Valid configuration
    usbhubcfg_mock.return_value.hubs = [
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=480),
        MagicMock(controller_path="/controller1", ports=[1, 2, 3], speed=5000)
    ]
    pdu = USBHubPDU("TestPDU", config)
    assert pdu.associated_hubs == usbhubcfg_mock.return_value.hubs
    assert pdu.ports == [PDUPort(pdu, "1"), PDUPort(pdu, "2"), PDUPort(pdu, "3")]

    # Set port state
    pdu.set_port_state(1, PDUState.ON)
    for hub in usbhubcfg_mock.return_value.hubs:
        hub.set_port_state.assert_called_once_with(1, PDUState.ON)

    # Get port state -- All agree
    pdu.associated_hubs = [
        MagicMock(get_port_state=MagicMock(return_value=PDUState.ON)),
        MagicMock(get_port_state=MagicMock(return_value=PDUState.ON)),
    ]
    assert pdu.get_port_state(1) == PDUState.ON

    # Get port state -- Disagreement
    pdu.associated_hubs.append(MagicMock(get_port_state=MagicMock(return_value=PDUState.OFF)))
    assert pdu.get_port_state(1) == PDUState.UNKNOWN
