from .. import PDU, PDUPort, PDUState

import itertools
import socket
import time
from contextlib import contextmanager

# The driver for KernelChip Lauren-2, Laurent-112, Laurent-128 relays,
# controlled over IP network.
#
# Example protocol ('>' and '<' mark sent and received strings and are not a
# part of the protocol)
#
# < #FLG,AB,11,11
# < JConfig from FLASH
# > $KE
# < #OK
# > $KE,INF
# < #INF,Laurent-128,LX11,Y18J-K78C-2D51-M199
# > $KE,RDR,1
# < #Access denied. Password is needed.
# > $KE,PSW,SET,Laurent
# < #PSW,SET,OK
# > $KE,RDR,1
# < #RDR,1,0
# > $KE,REL,1,1
# < #REL,OK
# > $KE,RDR,1
# < #RDR,1,1
# > $KE,REL,1,0
# < #REL,OK
# > $KE,RDR,ALL
# < #RDR,ALL,0000000000000000000000000000


class KernelChipConnection:
    def __init__(self, socket):
        self.socket = socket
        self.reader = self.reader()

    def send_msg(self, *args):
        out = b','.join(itertools.chain([b'$KE'], args)) + b'\r\n'
        self.socket.sendall(out)

    def reader(self):
        chunks = []
        seen_cr = False
        while True:
            chunk = self.socket.recv(2048)
            pos = 0
            for (i, c) in enumerate(chunk):
                if c == ord('\r'):
                    if seen_cr:
                        raise ValueError("Duplicate '\\r'")
                    if i != pos:
                        chunks.append(chunk[pos:i])
                    pos = i + 1
                    seen_cr = True
                elif c == ord('\n'):
                    if seen_cr:
                        yield b''.join(chunks)
                        chunks = []
                        pos = i + 1
                        seen_cr = False
                else:
                    seen_cr = False
            if pos != len(chunk):
                chunks.append(chunk[pos:])

    def recv_msg(self):
        buf = next(self.reader)

        # Workarounds for the rogue message after boot
        if buf.startswith(b'#FLG,'):
            buf = next(self.reader)
        if buf.startswith(b'JConfig'):
            buf = next(self.reader)

        if buf[0] != ord('#'):
            raise ValueError('Invalid first byte')
        return buf[1:].split(b',')


# in seconds
PORT_STATE_TIMEOUT = 0.1


class KernelChipPDU(PDU):
    def __init__(self, name, config, reserved_port_ids=[]):
        self.host, self.port = config.get('hostname', 'localhost:2424').split(':')
        self.port = int(self.port)
        self.password = config.get('password', None)

        # Check for supported module
        with self.conn() as s:
            # Protocol check to make sure we speak to a compatible PDU.
            s.send_msg()
            r = s.recv_msg()[0]
            if r != b'OK':
                raise ValueError("Protocol error")

            self._auth(s)

            self._update_state(s)
            self.num_relay = len(self.cached_state)

        self._ports = [PDUPort(self, i) for i in range(1, self.num_relay + 1)]

        super().__init__(name, config, reserved_port_ids)

    def _auth(self, s):
        if self.password:
            s.send_msg(b'PSW', b'SET', bytes(self.password, 'ascii'))
            if s.recv_msg() != [b'PSW', b'SET', b'OK']:
                raise ValueError("Password Verification failure")

    def _is_cached_state_valid(self):
        return self.state_stamp and time.time() - self.state_stamp < PORT_STATE_TIMEOUT

    def _update_state(self, s):
        cur_time = time.time()

        s.send_msg(b'RDR', b'ALL')
        r = s.recv_msg()
        if r[0].startswith(b'Access'):
            raise ValueError("Password is required")

        if len(r) != 3 or r[0] != b'RDR' or r[1] != b'ALL':
            raise ValueError("Failure getting relays state")

        self.state_stamp = cur_time
        self.cached_state = r[2]

    @property
    def ports(self):
        return self._ports

    @contextmanager
    def conn(self, *args, **kw):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((self.host, self.port))

            yield KernelChipConnection(s)

    def set_port_state(self, port_id, state):
        if port_id < 1 or port_id > self.num_relay:
            raise ValueError('Invalid port id')

        port = bytes(str(port_id), 'ascii')
        msg = b'0' if state == PDUState.OFF else b'1'

        with self.conn() as s:
            self._auth(s)

            s.send_msg(b'REL', port, msg)
            r = s.recv_msg()

            # safety net, __init__ checks whether the password is required
            if r[0].startswith(b'Access'):  # pragma: no cover
                raise ValueError("Password is required")

            if r != [b'REL', b'OK']:
                raise ValueError("Incorrect response")

            self._update_state(s)

    def get_port_state(self, port_id):
        if port_id < 1 or port_id > self.num_relay:
            raise ValueError('Invalid port id')

        if not self._is_cached_state_valid():
            with self.conn() as s:
                self._auth(s)
                self._update_state(s)

        if self.cached_state[port_id - 1] == ord(b'1'):
            return PDUState.ON
        else:
            return PDUState.OFF
