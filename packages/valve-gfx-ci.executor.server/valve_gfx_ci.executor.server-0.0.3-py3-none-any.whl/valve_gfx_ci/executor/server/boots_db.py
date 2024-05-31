from dataclasses import field, fields
from typing import Dict, List, Optional

from jinja2 import Template, ChainableUndefined
from pydantic.dataclasses import dataclass
import usb.core
import yaml

from .job import DeploymentState
from . import config


@dataclass
class USBMatcher:
    idVendor: Optional[int | List[int]] = None
    idProduct: Optional[int | List[int]] = None
    iManufacturer: Optional[str | List[str]] = None
    iProduct: Optional[str | List[str]] = None
    iSerialNumber: Optional[str | List[str]] = None

    def matches(self, device: 'usb.core.Device'):
        for f in fields(self):
            if expected_values := getattr(self, f.name, None):
                if not isinstance(expected_values, list):
                    expected_values = [expected_values]

                if getattr(device, f.name) not in expected_values:
                    return False

        return True


@dataclass
class FastbootDeviceMatcher:
    # NOTE: All the specified values must be a match to be considered a valid match
    usb: Optional[USBMatcher] = None
    variables: Optional[Dict[str, str | List[str]]] = field(default_factory=dict)  # The values are regular expressions

    def matches(self, fbdev: 'FastbootDevice'):
        if self.usb and not self.usb.matches(fbdev.device):
            return False

        # Match the expected variables
        fbdev_vars = fbdev.variables
        for name, expected_values in self.variables.items():
            if not isinstance(expected_values, list):
                expected_values = [expected_values]

            if fbdev_vars.get(name) not in expected_values:
                return False

        return True


@dataclass
class FastbootDevice:
    match: FastbootDeviceMatcher
    defaults: DeploymentState


@dataclass
class BootsDB:
    fastboot: Optional[Dict[str, FastbootDevice]] = field(default_factory=dict)

    @classmethod
    def render_with_resources(cls, db_str, machine=None, **kwargs):
        template_params = {
            **{k.lower(): v for k, v in config.job_environment_vars().items()},
            "machine": machine.safe_attributes if machine else None,
            **kwargs,
        }

        rendered_db_str = Template(db_str, undefined=ChainableUndefined).render(**template_params)
        return cls(**yaml.safe_load(rendered_db_str))

    @classmethod
    def from_path(cls, filepath, **kwargs):
        with open(filepath, "r") as f_template:
            db_str = f_template.read()
            return cls.render_with_resources(db_str, **kwargs)
