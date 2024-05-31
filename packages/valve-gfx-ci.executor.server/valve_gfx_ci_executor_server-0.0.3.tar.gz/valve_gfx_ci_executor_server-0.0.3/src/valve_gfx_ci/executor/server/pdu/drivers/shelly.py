from functools import cached_property
import re

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import requests

from .. import PDU, PDUPort, PDUState


class ShellyPDU(PDU):
    @property
    def requests_retry_session(self, retries=3, backoff_factor=1,
                               status_forcelist=[], session=None):  # pragma: nocover
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def url(self, path):
        hostname = self.config['hostname']
        return f"http://{hostname}{path}"

    def get(self, path):
        r = self.requests_retry_session.get(self.url(path), timeout=1)
        r.raise_for_status()
        return r.json()

    @property
    def gen(self):
        if gen := self.raw_dev.get('gen'):  # Gen 2+ hardware
            return gen
        else:
            return 1

    @cached_property
    def num_ports(self):
        # NOTE: We really want to have a stable amount of ports, even in the presence
        # of network issues, so let's depend on the one thing we have: `/shelly`

        if self.gen == 1:
            return self.raw_dev.get('num_outputs')
        elif app := self.raw_dev.get('app'):
            if app in ['PlusPlugS']:
                return 1
            elif m := re.match(r'^(Pro|Plus)(\d)(PM)?$', app):
                return int(m.groups()[1])

        # Assume the worst: no controllable ports
        return 0

    def __init__(self, name, config, reserved_port_ids=[]):
        super().__init__(name, config, reserved_port_ids)

        self.raw_dev = self.get('/shelly')

        if self.gen not in [1, 2] or self.num_ports == 0:
            t = self.raw_dev.get('type')
            m = self.raw_dev.get('model')
            a = self.raw_dev.get('app')
            raise ValueError(f"Unknown Shelly device: gen={self.gen}, type={t}, model={m}, app={a}")

        self._ports = [PDUPort(self, str(oid)) for oid in range(self.num_ports)]

    @property
    def ports(self):
        # Update the ports, in case their name changed
        for port in self._ports:
            if self.gen == 1:
                raw_port = self.get(f'/settings/relay/{port.port_id}')
                port.label = raw_port.get('name')
            else:
                raw_port = self.get(f'/rpc/Switch.GetConfig?id={port.port_id}')
                port.label = raw_port.get('name')

        return self._ports

    def __ison_to_PDUState(self, ison):
        return PDUState.ON if ison else PDUState.OFF

    def set_port_state(self, port_id, state):
        if self.gen == 1:
            raw_port = self.get(f'/relay/{port_id}?turn={state.name.lower()}')
            return self.__ison_to_PDUState(raw_port.get('ison')) == state
        else:
            ison = str(state == PDUState.ON).lower()
            self.get(f'/rpc/Switch.Set?id={port_id}&on={ison}')
            return True

    def get_port_state(self, port_id):
        if self.gen == 1:
            raw_port = self.get(f'/relay/{port_id}')
            return self.__ison_to_PDUState(raw_port.get('ison'))
        else:
            raw_port = self.get(f'/rpc/Switch.GetStatus?id={port_id}')
            return self.__ison_to_PDUState(raw_port.get('output'))
