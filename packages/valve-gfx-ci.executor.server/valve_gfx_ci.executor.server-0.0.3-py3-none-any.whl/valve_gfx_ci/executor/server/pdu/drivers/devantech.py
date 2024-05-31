from .. import PDU, PDUPort, PDUState

import socket
from contextlib import contextmanager


class DevantechPDU(PDU):
    def __init__(self, name, config, reserved_port_ids=[]):
        self.host, self.port = config.get('hostname', 'localhost:17494').split(':')
        self.port = int(self.port)
        self.password = config.get('password', None)

        # mapping from module id -> number of relays
        self.devices = {18: 2,    # eth002
                        19: 8,    # eth008
                        20: 4,    # eth484
                        21: 20,   # eth8020
                        22: 4,    # wifi484
                        24: 20,   # wifi8020
                        26: 2,    # wifi002
                        28: 8,    # wifi008
                        51: 20,   # eth1620
                        52: 10}   # eth1610

        # Check for supported module
        with self.conn() as s:
            s.sendall(b"\x10")
            id = s.recv(3)[0]
            if id not in self.devices:
                raise ValueError("not supported module id found")

        self._ports = [PDUPort(self, i) for i in range(self.devices[id])]

        super().__init__(name, config, reserved_port_ids)

    @property
    def ports(self):
        return self._ports

    @contextmanager
    def conn(self, *args, **kw):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            s.connect((self.host, self.port))

            # Check to see if password is enabled
            s.sendall(b"\x7a")
            if s.recv(1)[0] == 0:
                passwordString = b'\x79' + self.password.encode()
                s.sendall(passwordString)
                if s.recv(1)[0] != 1:
                    raise ValueError("wrong password")

            yield s

    def set_port_state(self, port_id, state):
        msg = b'\x21' if state == PDUState.OFF else b'\x20'
        msg += int(port_id).to_bytes(1, 'big')
        msg += b'\x00'

        with self.conn() as s:
            s.sendall(msg)
            if s.recv(1)[0] == 1:
                raise ValueError('failed to set port state')

    def get_port_state(self, port_id):
        num_bytes = (len(self._ports) + 7) // 8

        with self.conn() as s:
            s.sendall(b'\x24')
            port_states = b''
            while len(port_states) != num_bytes:
                buf = s.recv(num_bytes - len(port_states), socket.MSG_WAITALL)
                if len(buf) == 0:
                    raise ValueError("we never received the expected amount of bytes")
                port_states += buf

            byte_index = port_id // 8
            bit_position = port_id % 8

            if port_states[byte_index] & (1 << bit_position):
                return PDUState.ON
            else:
                return PDUState.OFF
