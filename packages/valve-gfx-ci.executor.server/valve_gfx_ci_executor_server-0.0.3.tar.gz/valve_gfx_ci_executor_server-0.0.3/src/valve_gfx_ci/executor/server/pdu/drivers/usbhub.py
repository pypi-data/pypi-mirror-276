from dataclasses import asdict
from functools import cached_property
from pathlib import Path
from typing import List, Optional
import re

from pydantic import NonNegativeInt, DirectoryPath, field_validator, model_validator
from pydantic.dataclasses import dataclass

from .. import PDU, PDUPort, PDUState


class USBHubDevice:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()

        if self.bDeviceClass != 0x09:
            raise ValueError(f"The USB device at location '{self.base_path}' is not a USB hub")

        self.ports = [
            str(oid) for oid in [i + 1 for i in range(self.maxchild)] if self.port_path(oid).exists()
        ]

    def __read(self, filename):
        return (self.base_path / filename).read_text().strip()

    def __read_int(self, filename, base=10):
        if v := self.__read(filename):
            return int(v, base)

    @cached_property
    def devpath(self):
        return self.__read("devpath")

    @cached_property
    def serial(self):
        return self.__read("serial")

    @cached_property
    def maxchild(self):
        return self.__read_int("maxchild")

    @cached_property
    def idVendor(self):
        return self.__read_int("idVendor", 16)

    @cached_property
    def idProduct(self):
        return self.__read_int("idProduct", 16)

    @cached_property
    def bDeviceClass(self):
        return self.__read_int("bDeviceClass", 16)

    @cached_property
    def speed(self):
        return self.__read_int("speed")

    @cached_property
    def controller_path(self):
        return self.base_path.parent.parent

    def port_path(self, port_id):
        paths = list(self.base_path.glob(f"*:1.0/*-port{port_id}/disable"))

        if len(paths) > 1:
            msg = f"Found more than one candidate port for port_id {port_id} in the hub at location '{self.base_path}'"
            raise ValueError(msg)
        elif len(paths) == 1:
            return paths[0]
        else:
            return Path()

    def set_port_state(self, port_id, state):
        if state not in [PDUState.OFF, PDUState.ON]:
            raise ValueError(f"Unsupported state {state.name}")

        self.port_path(port_id).write_text("0\n" if state == PDUState.ON else "1\n")

    def get_port_state(self, port_id):
        state = self.port_path(port_id).read_text().strip()
        return PDUState.ON if state == "0" else PDUState.OFF


@dataclass
class USBHubDeviceMatchConfig:
    devpath: str
    idVendor: NonNegativeInt
    idProduct: NonNegativeInt

    maxchild: Optional[NonNegativeInt] = None
    speed: Optional[NonNegativeInt] = None

    @field_validator("devpath")
    @classmethod
    def devpath_has_expected_format(cls, v):
        if not re.match(r"^(\d+\.?)*\d+$", v):
            raise ValueError("The devpath is not a dot-separated list of integers")
        return v

    def matches(self, hub):
        for field_name in asdict(self):
            if value := getattr(self, field_name):
                if getattr(hub, field_name) != value:
                    return False
        return True


@dataclass
class USBHubPDUConfig:
    controller: Optional[DirectoryPath] = None
    devices: Optional[List[USBHubDeviceMatchConfig]] = None

    serial: Optional[str] = None

    # Default paths
    USB_DEVICES_PATH = Path("/sys/bus/usb/devices")

    @field_validator("serial")
    @classmethod
    def serial_is_stripped(cls, v):
        return v.strip()

    @model_validator(mode="after")
    def ensure_we_have_the_right_parameters(self) -> "USBHubPDUConfig":
        if self.serial is not None:
            return self
        elif self.controller is not None and self.devices is not None:
            if len(self.devices) == 0:
                raise ValueError("At least one device should be set")
            return self
        else:
            raise ValueError("Neither a `serial` nor the tuple (`controller`, `devices`) was found in the config")

    @property
    def hubs(self):
        hubs = []
        if self.serial:
            for serial_path in self.USB_DEVICES_PATH.glob("*/serial"):
                if serial_path.read_text().strip() == self.serial:
                    try:
                        hubs.append(USBHubDevice(serial_path.parent))
                    except Exception:  # pragma: nocover
                        continue

            if len(hubs) == 0:
                raise ValueError(f"No USB Hubs with serial '{self.serial}' found")
        elif self.controller and self.devices:
            for dev_cfg in self.devices:
                dev_cfg_hubs = []
                for dev in self.controller.glob(f"usb*/*-{dev_cfg.devpath}"):
                    try:
                        hub = USBHubDevice(dev)
                    except Exception:
                        continue

                    if dev_cfg.matches(hub):
                        dev_cfg_hubs.append(hub)
                    else:
                        print(f"{dev_cfg}.matches({hub}) = False")
                if len(dev_cfg_hubs) == 0:
                    raise ValueError(f"Could not find a USB device matching {dev_cfg}")
                elif len(dev_cfg_hubs) == 1:
                    hubs.extend(dev_cfg_hubs)
                else:
                    raise ValueError(f"Found more than one USB device match {dev_cfg}")

        return hubs


class USBHubPDU(PDU):
    @cached_property
    def associated_hubs(self):
        hubs = USBHubPDUConfig(**self.config).hubs
        if len(hubs) == 0:
            return []

        # Use the first hub as a reference
        ref = hubs[0]

        # Ensure that all the hubs share the same controller (needed for serial-based devices)
        if not all([h.controller_path == ref.controller_path for h in hubs]):
            raise ValueError("Not all hubs are connected to the same USB controller")

        # Ensure that all the hubs have the same ports
        if not all([h.ports == ref.ports for h in hubs]):
            raise ValueError("Not all hubs agree on the list of ports")

        # Ensure that all the hubs have different speeds like they should if a controller had
        # support for multiple USB versions, but all connected to the same USB lines
        speeds = {h.speed for h in hubs}
        if len(speeds) != len(hubs):
            raise ValueError("Some hubs unexpectedly share the same speed")

        return hubs

    def __init__(self, name, config, reserved_port_ids=[]):
        super().__init__(name, config, reserved_port_ids)

        if len(list(self.associated_hubs)) == 0:
            raise ValueError("No associated hub devices found")

        self._ports = [
            PDUPort(self, str(oid))
            for oid in self.associated_hubs[0].ports
        ]

    @property
    def ports(self):
        return self._ports

    def set_port_state(self, port_id, state):
        for h in self.associated_hubs:
            h.set_port_state(port_id, state)

    def get_port_state(self, port_id):
        states = {h.get_port_state(port_id) for h in self.associated_hubs}

        if len(states) == 1:
            return states.pop()
        else:
            return PDUState.UNKNOWN
