from unittest.mock import MagicMock
import pytest
import time

from server.pdu.drivers.cyberpower import PDU41004


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


def test_driver_PDU41004_check_OIDs():
    pdu = PDU41004("MyPDU", {"hostname": "127.0.0.1"})
    assert pdu.outlet_labels_oid == f"{pdu.oid_enterprise}.3808.1.1.3.3.3.1.1.2"
    assert pdu.outlet_status_oid(10) == f"{pdu.oid_enterprise}.3808.1.1.3.3.3.1.1.4.10"
    assert pdu.outlet_ctrl_oid(10) == f"{pdu.oid_enterprise}.3808.1.1.3.3.3.1.1.4.10"
