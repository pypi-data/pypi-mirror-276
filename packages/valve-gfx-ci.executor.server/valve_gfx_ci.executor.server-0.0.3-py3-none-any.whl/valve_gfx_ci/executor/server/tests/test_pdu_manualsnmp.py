from unittest.mock import MagicMock
import pytest
import copy
import time

from server.pdu import PDUState
from server.pdu.drivers.snmp import ManualSnmpPDU


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


def test_driver_ManualSnmpPDU_check_OIDs_and_default_actions():
    pdu = ManualSnmpPDU("MyPDU", config={
        "hostname": "127.0.0.1",
        "system_id": "1.2.3.4",
        "outlet_labels": "5.6.7.8",
        "outlet_status": "5.6.7.9",
        "outlet_ctrl": "5.6.7.10",
        "state_mapping": {
            "on": 1,
            "off": 2,
            "reboot": 3,
        },
    })

    Session.assert_called_with(hostname=pdu.config['hostname'], community="private", version=1)

    assert pdu.outlet_labels == "5.6.7.8"
    assert pdu.outlet_status_oid(10) == "1.3.6.1.4.1.1.2.3.4.5.6.7.9.10"
    assert pdu.outlet_ctrl_oid(10) == "1.3.6.1.4.1.1.2.3.4.5.6.7.10.10"
    assert pdu.state_mapping.keys() == set([PDUState.ON, PDUState.OFF, PDUState.REBOOT])
    assert pdu.inverse_state_mapping.keys() == set([1, 2, 3])
    for k, _ in pdu.state_mapping.items():
        assert pdu.inverse_state_mapping[pdu.state_mapping[k]] == k


def test_driver_ManualSnmpPDU_check_v3_codepath():
    config = {
        "hostname": "127.0.0.1",
        "system_id": "1.2.3.4",
        "outlet_labels": "5.6.7.8",
        "outlet_status": "5.6.7.9",
        "outlet_ctrl": "5.6.7.10",
        "version": 3,
        "state_mapping": {
            "on": 1,
            "off": 2,
            "reboot": 3,
        },
    }

    # No username, authentication nor privacy
    pdu = ManualSnmpPDU("MyPDU", config=config)
    Session.assert_called_with(hostname=pdu.config['hostname'], version=3, security_level='no_auth_or_privacy')
    Session.reset_mock()

    # Check that adding the following fields does not impact the security_level parameter
    config['security_username'] = 'security_username'
    config['privacy_password'] = 'privacy_password'
    config['auth_password'] = 'auth_password'
    config['context_engine_id'] = 'context_engine_id'
    config['security_engine_id'] = 'security_engine_id'
    pdu = ManualSnmpPDU("MyPDU", config=config)
    Session.assert_called_with(hostname=pdu.config['hostname'], version=3, security_username='security_username',
                               privacy_password='privacy_password', auth_password='auth_password',
                               context_engine_id='context_engine_id', security_engine_id='security_engine_id',
                               security_level='no_auth_or_privacy')
    Session.reset_mock()

    # Check auth_without_privacy
    config['auth_protocol'] = 'auth_protocol'
    pdu = ManualSnmpPDU("MyPDU", config=config)
    Session.assert_called_with(hostname=pdu.config['hostname'], version=3, security_username='security_username',
                               privacy_password='privacy_password', auth_password='auth_password',
                               context_engine_id='context_engine_id', security_engine_id='security_engine_id',
                               auth_protocol='auth_protocol', security_level='auth_without_privacy')
    Session.reset_mock()

    # Check auth_with_privacy
    config['privacy_protocol'] = 'privacy_protocol'
    pdu = ManualSnmpPDU("MyPDU", config=config)
    Session.assert_called_with(hostname=pdu.config['hostname'], version=3, security_username='security_username',
                               privacy_password='privacy_password', auth_password='auth_password',
                               context_engine_id='context_engine_id', security_engine_id='security_engine_id',
                               auth_protocol='auth_protocol', privacy_protocol='privacy_protocol',
                               security_level='auth_with_privacy')
    Session.reset_mock()

    # Verify that we cannot have a privacy protocol without an auth protocol
    del config['auth_protocol']
    with pytest.raises(ValueError):
        pdu = ManualSnmpPDU("MyPDU", config=config)


def test_driver_ManualSnmpPDU_invalid_snmp_version():
    config = {
        "hostname": "127.0.0.1",
        "system_id": "1.2.3.4",
        "outlet_labels": "5.6.7.8",
        "outlet_status": "5.6.7.9",
        "outlet_ctrl": "5.6.7.10",
        "version": 3,
        "state_mapping": {
            "on": 1,
            "off": 2,
            "reboot": 3,
        },
    }

    ManualSnmpPDU("MyPDU", config=config)
    with pytest.raises(ValueError):
        config['version'] = 4
        ManualSnmpPDU("MyPDU", config=config)


def test_driver_ManualSnmpPDU_invalid_actions():
    with pytest.raises(ValueError):
        ManualSnmpPDU("MyPDU", config={
            "hostname": "127.0.0.1",
            "system_id": "1.2.3.4",
            "outlet_labels": "5.6.7.8",
            "outlet_status": "5.6.7.9",
            "outlet_ctrl": "5.6.7.10",
            "state_mapping": {
                "on": "FUDGE",
                "off": 2,
                "reboot": 3,
            },
        })


def test_driver_ManualSnmpPDU_missing_actions():
    with pytest.raises(AssertionError):
        ManualSnmpPDU("MyPDU", config={
            "hostname": "127.0.0.1",
            "system_id": "1.2.3.4",
            "outlet_labels": "5.6.7.8",
            "outlet_status": "5.6.7.9",
            "outlet_ctrl": "5.6.7.10",
            "state_mapping": {
                "off": 2,
                "reboot": 3,
            },
        })


def test_driver_ManualSnmpPDU_missing_parameters():
    valid_config = {
        "hostname": "127.0.0.1",
        "system_id": "1.2.3.4",
        "outlet_labels": "5.6.7.8",
        "outlet_status": "5.6.7.9",
        "outlet_ctrl": "5.6.7.10",
        "state_mapping": {
            "on": 1,
            "off": 2,
            "reboot": 3,
        },
    }

    ManualSnmpPDU("MyPDU", config=valid_config)
    for required_param in ["hostname", "system_id", "outlet_labels", "outlet_status", "state_mapping"]:
        new_config = copy.deepcopy(valid_config)
        del new_config[required_param]
        with pytest.raises((ValueError, AssertionError, KeyError)):
            ManualSnmpPDU("MyPDU", config=new_config)


def test_driver_ManualSnmpPDU_weird_inverses():
    valid_config = {
        "hostname": "127.0.0.1",
        "system_id": "1.2.3.4",
        "outlet_labels": "5.6.7.8",
        "outlet_status": "5.6.7.9",
        "outlet_ctrl": "5.6.7.10",
        "state_mapping": {
            "on": 1,
            "off": 2,
            "reboot": 3,
        },
        "inverse_state_mapping": {
            "on": 2,
            "off": 3,
            "reboot": 4,
        },
    }

    pdu = ManualSnmpPDU("MyPDU", config=valid_config)
    for k, _ in pdu.state_mapping.items():
        assert pdu.inverse_state_mapping[pdu.state_mapping[k]] == k + 1
