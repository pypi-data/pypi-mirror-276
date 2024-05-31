from easysnmp import Session
import easysnmp.exceptions
from .. import logger, PDU, PDUPort, PDUState
from functools import cached_property
from typing import Dict

import random
import time


def _is_int(s):
    try:
        s = int(s)
        return True
    except ValueError:
        return False


def retry_on_known_errors(func):
    def retry(*args, **kwargs):
        retries = 3

        for i in range(retries):
            try:
                return func(*args, **kwargs)
            except (SystemError, easysnmp.exceptions.EasySNMPError) as e:
                logger.warning(f"Caught the error '{str(e)}', retrying ({i+1}/{retries})")
                # Wait 1 second, plus a random [0,1] second delay to reduce the chances of concurrent requests
                time.sleep(1 + random.random())
                continue

        raise ValueError(f"The function {func} failed {retries} times in a row")

    return retry


class SnmpPDU(PDU):
    oid_enterprise = '1.3.6.1.4.1'

    @property
    def __port_labels(self):
        try:
            return [x.value for x in self.session.walk(self.outlet_labels_oid)]
        except SystemError as e:
            raise ValueError(f"The snmp_walk() call failed with the following error: {e}")

    def __init__(self, name, config, reserved_port_ids=[]):
        super().__init__(name, config, reserved_port_ids)

        assert self.system_id
        assert self.outlet_labels
        assert self.outlet_status

        if not hasattr(self, 'outlet_ctrl'):
            # Some PDUs offer a RW status tree, others require a separate
            # tree for writes. Default to the seemingly more common case
            # of a RW tree.
            self.outlet_ctrl = self.outlet_status

        # FIXME: The UNKNOWN status is a bit of an odd one, not all PDUs expose such a concept.
        assert self.state_mapping.keys() == set([PDUState.ON, PDUState.OFF, PDUState.REBOOT])
        if not hasattr(self, 'inverse_state_mapping'):
            self.inverse_state_mapping: Dict[int, PDUState] = \
                dict([(value, key) for key, value in self.state_mapping.items()])
        else:
            assert self.inverse_state_mapping.keys() == set([PDUState.ON, PDUState.OFF, PDUState.REBOOT])

        # Validate the configuration by getting the list of ports
        self._ports = []
        self.ports

    @cached_property
    def session(self):
        config = self.config

        if 'hostname' not in config:
            raise ValueError('SnmpPDU requires a "hostname" configuration key')

        version = config.get('version', 1)
        if version in [1, 2]:
            session = Session(hostname=config['hostname'], community=config.get('community', 'private'),
                              version=version)
        elif version == 3:
            # Only keep the keys
            supported_keys = {'hostname', 'security_username', 'privacy_protocol', 'privacy_password',
                              'auth_protocol', 'auth_password', 'context_engine_id', 'security_engine_id', 'version'}
            session_cfg = {k: v for k, v in config.items() if k in supported_keys}

            auth_protocol = session_cfg.get('auth_protocol')
            privacy_protocol = session_cfg.get('privacy_protocol')
            if auth_protocol is not None and privacy_protocol is not None:
                session_cfg['security_level'] = 'auth_with_privacy'
            elif auth_protocol is not None and privacy_protocol is None:
                session_cfg['security_level'] = 'auth_without_privacy'
            elif auth_protocol is None and privacy_protocol is None:
                session_cfg['security_level'] = 'no_auth_or_privacy'
            else:
                raise ValueError("Unsupported security level: Can't have a privacy protocol with no auth protocol")

            session = Session(**session_cfg)
        else:
            raise ValueError(f"SNMP version {version} is unsupported")

        # Validate the configuration by reading the state of the first port
        session.get(self.outlet_status_oid(1))

        return session

    @property
    def outlet_system_id(self):
        return f'{self.oid_enterprise}.{self.system_id}'

    @property
    def outlet_labels_oid(self):
        return f'{self.outlet_system_id}.{self.outlet_labels}'

    def outlet_status_oid(self, port_id):
        assert isinstance(port_id, int)
        return f'{self.outlet_system_id}.{self.outlet_status}.{port_id}'

    def outlet_ctrl_oid(self, port_id: int):
        assert isinstance(port_id, int)
        return f'{self.outlet_system_id}.{self.outlet_ctrl}.{port_id}'

    @property
    def ports(self):
        labels = self.__port_labels
        for i, label in enumerate(labels):
            if len(self._ports) <= i:
                port = PDUPort(pdu=self, port_id=i+1)
                self._ports.append(port)
            else:
                port = self._ports[i]

            # Update the label
            port.label = labels[i]

        # Truncate the list of ports if it shrank
        self._ports = self._ports[0:len(labels)]

        return self._ports

    def _port_spec_to_int(self, port_spec):
        if _is_int(port_spec):
            return port_spec
        else:
            for port in self.ports:
                if port.label == port_spec:
                    return port.port_id
            raise ValueError(
                f"{port_spec} can not be interpreted as a valid port")

    @retry_on_known_errors
    def set_port_state(self, port_spec, state):
        SNMP_INTEGER_TYPE = 'i'

        port_id = self._port_spec_to_int(port_spec)
        logger.debug('setting OID %s to state %s with value %d',
                     self.outlet_ctrl_oid(port_id),
                     state,
                     self.state_mapping[state])
        ret = self.session.set(self.outlet_ctrl_oid(port_id),
                               self.state_mapping[state],
                               SNMP_INTEGER_TYPE)

        if self.state_transition_delay_seconds is not None:
            logger.debug("Enforcing %s seconds of delay for state change", self.state_transition_delay_seconds)
            # TODO: keep track of state changes to avoid a forced sleep.
            # TODO: Polling for the state change would be better in general.
            # The root cause of this is because PDUs maintain their
            # own configurables how long to delay between
            # transitions, we should probably control that via SNMP,
            # as well.
            time.sleep(self.state_transition_delay_seconds)

        return ret

    @retry_on_known_errors
    def get_port_state(self, port_spec):
        port_id = self._port_spec_to_int(port_spec)
        vs = self.session.get(self.outlet_status_oid(port_id))
        value = int(vs.value)
        logger.debug('retrieved OID %s with value %d, maps to state %s',
                     self.outlet_status_oid(port_id),
                     value,
                     self.inverse_state_mapping[value])
        return self.inverse_state_mapping[value]

    def __eq__(self, other):
        return not any([
            getattr(self, attr, None) != getattr(other, attr, None)
            for attr in ["name",
                         "config",
                         "system_id",
                         "outlet_labels",
                         "outlet_status",
                         "outlet_ctrl",
                         "state_mapping",
                         "inverse_state_mapping"]])


class ManualSnmpPDU(SnmpPDU):
    def __init__(self, name, config, reserved_port_ids=[]):
        if inverse_state_mapping := config.get('inverse_state_mapping'):
            self.inverse_state_mapping = self.__generate_state_mapping(inverse_state_mapping)

        super().__init__(name, config, reserved_port_ids)

    @property
    def system_id(self):
        return self.config['system_id']

    @property
    def outlet_labels(self):
        return self.config['outlet_labels']

    @property
    def outlet_status(self):
        return self.config['outlet_status']

    # Some PDUs offer a RW status tree, others require a separate
    # tree for writes. Default to the seemingly more common case
    # of a RW tree.
    @property
    def outlet_ctrl(self):
        return self.config.get('outlet_ctrl', self.outlet_status)

    def __generate_state_mapping(self, d):
        state_mapping = dict()

        for state, internal_value in d.items():
            v = int(internal_value)
            if state.lower() == "on":
                state_mapping[PDUState.ON] = v
            elif state.lower() == "off":
                state_mapping[PDUState.OFF] = v
            elif state.lower() == "reboot":
                state_mapping[PDUState.REBOOT] = v
                # Unknown deliberately excluded.

        return state_mapping

    @property
    def state_mapping(self):
        return self.__generate_state_mapping(self.config.get('state_mapping', {}))
