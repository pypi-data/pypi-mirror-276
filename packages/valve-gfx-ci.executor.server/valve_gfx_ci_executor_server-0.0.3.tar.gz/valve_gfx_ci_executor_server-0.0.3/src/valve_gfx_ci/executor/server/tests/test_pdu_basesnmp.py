from unittest.mock import MagicMock, patch, PropertyMock
import pytest
import time

from server.pdu import PDUState
from server.pdu.drivers.snmp import (
    retry_on_known_errors,
    SnmpPDU,
    Session
)


@pytest.fixture(autouse=True)
def reset_easysnmp_mock(monkeypatch):
    import server.pdu.drivers.snmp as snmp

    global Session, time_sleep
    m1, m2 = MagicMock(), MagicMock()
    # REVIEW: I wonder if there's a clever way of covering the
    # difference in import locations between here and snmp.py
    monkeypatch.setattr(snmp, "Session", m1)
    monkeypatch.setattr(time, "sleep", m2)
    Session = m1
    time_sleep = m2


@patch("random.random", return_value=0.42)
def test_driver_BaseSnmpPDU_retry_on_known_errors__known_error(random_mock):
    global retriable_error_call_count
    retriable_error_call_count = 0

    @retry_on_known_errors
    def retriable_error():
        global retriable_error_call_count

        assert time_sleep.call_count == retriable_error_call_count

        retriable_error_call_count += 1
        raise SystemError("<built-in function set> returned NULL without setting an error")

    with pytest.raises(ValueError):
        retriable_error()

    time_sleep.assert_called_with(1.42)
    assert time_sleep.call_count == retriable_error_call_count
    assert retriable_error_call_count == 3


class MockSnmpPDU(SnmpPDU):
    system_id = '1234.1.2.3.4'
    outlet_labels = '4.5.4.5'
    outlet_status = '4.5.4.6'

    state_mapping = {
        PDUState.ON: 2,
        PDUState.OFF: 3,
        PDUState.REBOOT: 4,
    }

    state_transition_delay_seconds = 5


def test_driver_SnmpPDU_eq():
    params = {
        "hostname": "hostname",
        "community": "community"
    }

    assert MockSnmpPDU("name", params) == MockSnmpPDU("name", params)
    for param in params:
        n_params = dict(params)
        n_params[param] = "modified"
        assert MockSnmpPDU("name", params) != MockSnmpPDU("name", n_params)


def test_driver_SnmpPDU_listing_ports():
    walk_mock = Session.return_value.walk
    walk_mock.return_value = [MagicMock(value="P1"), MagicMock(value="P2")]

    pdu = MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})
    walk_mock.assert_called_with(pdu.outlet_labels_oid)
    ports = pdu.ports

    # Check that the labels are stored, and the port IDs are 1-indexed
    for i in range(0, 2):
        assert ports[i].port_id == i+1
        assert ports[i].label == f"P{i+1}"


def test_driver_SnmpPDU_listing_ports__walk_failure():
    err_msg = "<built-in function walk> returned NULL without setting an error"
    Session.return_value.walk.side_effect = SystemError(err_msg)

    with pytest.raises(ValueError):
        MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})


def test_driver_BaseSnmpPDU_port_label_mapping():
    walk_mock = Session.return_value.walk
    set_mock = Session.return_value.set
    walk_mock.return_value = [
        MagicMock(value="P1"),
        MagicMock(value="P2")
    ]

    pdu = MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})

    set_mock.return_value = True
    assert pdu.set_port_state("P1", PDUState.REBOOT) is True
    set_mock.assert_called_with(pdu.outlet_ctrl_oid(1), pdu.state_mapping[PDUState.REBOOT], 'i')
    assert pdu.set_port_state("P2", PDUState.REBOOT) is True
    set_mock.assert_called_with(pdu.outlet_ctrl_oid(2), pdu.state_mapping[PDUState.REBOOT], 'i')
    with pytest.raises(ValueError):
        pdu.set_port_state("flubberbubber", PDUState.OFF)


def test_driver_BaseSnmpPDU_get_port():
    get_mock = Session.return_value.get

    pdu = MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})
    get_mock.return_value.value = pdu.state_mapping[PDUState.REBOOT]
    get_mock.assert_called_with(pdu.outlet_status_oid(1))
    pdu_state = pdu.get_port_state(2)
    assert pdu_state == PDUState.REBOOT
    get_mock.assert_called_with(pdu.outlet_status_oid(2))

    get_mock.side_effect = SystemError("<built-in function get> returned NULL without setting an error")
    with pytest.raises(ValueError):
        pdu.get_port_state(2)


def test_driver_BaseSnmpPDU_set_port():
    set_mock = Session.return_value.set

    pdu = MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})
    type(set_mock).value = PropertyMock(return_value=pdu.state_mapping[PDUState.REBOOT])
    set_mock.return_value = True
    set_mock.assert_not_called()
    assert pdu.set_port_state(2, PDUState.REBOOT) is True
    set_mock.assert_called_with(pdu.outlet_ctrl_oid(2), pdu.state_mapping[PDUState.REBOOT], 'i')

    set_mock.side_effect = SystemError("<built-in function set> returned NULL without setting an error")
    with pytest.raises(ValueError):
        pdu.set_port_state(2, PDUState.REBOOT)


def test_driver_BaseSnmpPDU_action_translation():
    pdu = MockSnmpPDU("MyPDU", {"hostname": "127.0.0.1"})

    # Check the state -> SNMP value translation
    for action in PDUState.valid_actions():
        assert pdu.inverse_state_mapping[pdu.state_mapping[action]] == action

    with pytest.raises(KeyError):
        pdu.state_mapping[PDUState.UNKNOWN]
