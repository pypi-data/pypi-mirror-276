from server.pdu import PDUState
from server.pdu.drivers.dummy import DummyPDU


def test_driver_DummyPDU():
    ports = ['P1', 'P2', 'P3']
    pdu = DummyPDU("MyPDU", {"ports": ports})

    assert [p.label for p in pdu.ports] == ports
    assert pdu.get_port_state(0) == PDUState.ON
    pdu.set_port_state(0, PDUState.OFF)
    assert pdu.get_port_state(0) == PDUState.OFF
