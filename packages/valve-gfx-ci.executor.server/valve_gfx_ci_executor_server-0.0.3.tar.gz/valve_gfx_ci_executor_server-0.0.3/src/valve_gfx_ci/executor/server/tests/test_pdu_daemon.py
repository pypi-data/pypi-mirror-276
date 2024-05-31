from copy import copy
from datetime import timedelta
from threading import Event
from unittest.mock import MagicMock, patch, PropertyMock, call

from server.pdu.daemon import AsyncPDU, AsyncPDUState, PDUDaemon


def init_mocked_pdu_ports(pdu_ports):
    pdu_ports.unlock_event = Event()

    def mockedPorts():
        pdu_ports.unlock_event.wait()
        return []

    pdu_ports.side_effect = mockedPorts


def test_AsyncPDU__eq():
    model_name = "dummy"
    pdu_name = "MyPDU"
    config = {"ports": ['P1', 'P2', 'P3']}
    reserved_port_ids = ["P1", "P2"]
    polling_interval = timedelta(seconds=1)

    pdu = AsyncPDU(model_name, pdu_name, config, reserved_port_ids, polling_interval)

    assert pdu == AsyncPDU(model_name, pdu_name, config, reserved_port_ids, polling_interval)
    assert pdu != AsyncPDU("vpdu", pdu_name, config, reserved_port_ids, polling_interval)
    assert pdu != AsyncPDU(model_name, "alternate name", config, reserved_port_ids, polling_interval)
    assert pdu != AsyncPDU(model_name, pdu_name, {"key": "value"}, reserved_port_ids, polling_interval)
    assert pdu != AsyncPDU(model_name, pdu_name, config, {'2', 'P2'}, polling_interval)
    assert pdu == AsyncPDU(model_name, pdu_name, config, reserved_port_ids, timedelta(seconds=2))


def test_AsyncPDU__get_port_by_id():
    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})

    pdu.started_event = MagicMock(is_set=MagicMock(return_value=False))
    pdu.ports = [MagicMock(port_id=0), MagicMock(port_id=1), MagicMock(port_id=2)]

    assert pdu.get_port_by_id(1) == pdu.ports[1]
    pdu.started_event.wait.assert_called_with(None)

    assert pdu.get_port_by_id(0, timeout=3) == pdu.ports[0]
    pdu.started_event.wait.assert_called_with(3)

    assert pdu.get_port_by_id(42) is None


@patch('server.pdu.drivers.dummy.DummyPDU.ports', new_callable=PropertyMock)
def test_AsyncPDU__run_keeps_going_when_failing_driver_setup(dummyPduPortsMock):
    dummyPduPortsMock.side_effect = ValueError("Custom error")

    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})

    pdu.stop_event = MagicMock(is_set=MagicMock(side_effect=[False, False, True]))

    pdu.start()
    pdu.join()

    assert not pdu.started_event.is_set()
    assert pdu.stop_event.wait.mock_calls == [call(15), call(15)]
    assert pdu.error == "Custom error"


@patch('server.pdu.drivers.dummy.DummyPDU.ports', new_callable=PropertyMock)
def test_AsyncPDU__run_recreate_driver_after_multiple_poll_fails(dummyPduPortsMock):
    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})

    expected_count = 10
    dummyPduPortsMock.side_effect = [[]] + expected_count * [ValueError("poll")] + [ValueError("final crash")]
    pdu.stop_event = MagicMock(is_set=MagicMock(side_effect=(1 + expected_count + 1) * [False] + [True]))

    pdu.start()
    pdu.join()

    assert not pdu.started_event.is_set()
    assert pdu.stop_event.is_set.call_count == 1 + expected_count + 1 + 1
    assert pdu.stop_event.wait.call_count == expected_count

    assert pdu.error == "final crash"


@patch('server.pdu.drivers.dummy.DummyPDU.ports', new_callable=PropertyMock)
def test_AsyncPDU__state(dummyPduPortsMock):
    # Set up the mock PDU to wait for a signal before returning the list of ports
    init_mocked_pdu_ports(dummyPduPortsMock)

    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})

    assert pdu.state == AsyncPDUState.CREATED

    # Test that we ignore any error set until the thread starts
    pdu.error = "Hello world"
    assert pdu.state == AsyncPDUState.CREATED
    pdu.error = None

    try:
        pdu.start()
        assert pdu.state == AsyncPDUState.INITIALIZING

        # Release the dummy PDUs ports signal to let the PDU finish initialization
        dummyPduPortsMock.unlock_event.set()
        pdu.started_event.wait()
        assert pdu.state == AsyncPDUState.OK

        pdu.error = "Hello world"
        assert pdu.state == AsyncPDUState.ERROR
        pdu.error = None

        pdu.stop()
        assert pdu.state == AsyncPDUState.STOPPED

        # Test that we ignore any error set after the thread has stopped
        pdu.error = "Hello world"
        assert pdu.state == AsyncPDUState.STOPPED
        pdu.error = None
    finally:
        pdu.stop()


def test_AsyncPDU__run_until_stop_event_set():
    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})
    pdu.stop_event = MagicMock(is_set=MagicMock(side_effect=[False, False, False, True, True]))

    pdu.run()

    assert pdu.stop_event.is_set.call_count == 5
    assert pdu.stop_event.wait.call_count == 2
    pdu.stop_event.wait.assert_called_with(1)


def test_AsyncPDU__stop_sets_stop_event_and_wait():
    pdu = AsyncPDU("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})

    pdu.stop_event = MagicMock()
    pdu.join = MagicMock()

    pdu.stop()

    pdu.stop_event.set.assert_called_once_with()
    pdu.join.assert_called_once_with()


@patch('server.pdu.drivers.dummy.DummyPDU')
def test_PDUDaemon__get_or_create(dummyPDUMock):
    daemon = PDUDaemon()

    try:
        # Make sure that by default we return a previously-created PDU, without updating *any* field
        ref = daemon.get_or_create("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})
        assert ref.polling_interval == timedelta(seconds=1)
        assert daemon.get_or_create("dummy", "MyPDU", {"ports": ['P2', 'P3', 'P4']},
                                    polling_interval=timedelta(seconds=5)) == ref
        assert ref.polling_interval == timedelta(seconds=1)

        # Ensure that the polling interval gets updated when the pdu would otherwise be the same
        assert ref.polling_interval == timedelta(seconds=1)
        assert daemon.get_or_create("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']},
                                    update_if_existing=True, polling_interval=timedelta(seconds=5)) == ref
        assert ref.polling_interval == timedelta(seconds=5)

        # Make sure that updating the PDU's parameters lead to the creation of a new PDU and stops the old one
        assert ref.state == AsyncPDUState.OK
        assert daemon.get_or_create("dummy", "MyPDU", {"ports": ['P2', 'P3', 'P4']}, update_if_existing=True) != ref
        assert ref.state == AsyncPDUState.STOPPED
    finally:
        daemon.stop()


@patch('server.pdu.drivers.dummy.DummyPDU')
def test_PDUDaemon__unregister_pdu(dummyPDUMock):
    daemon = PDUDaemon()

    try:
        # Make sure that we can remove an existing PDU
        daemon.get_or_create("dummy", "MyPDU", {"ports": ['P1', 'P2', 'P3']})
        daemon.unregister_pdu("MyPDU")

        # Make sure that removing unknown PDUs doesn't raise
        daemon.unregister_pdu("MyPDU")
    finally:
        daemon.stop()


def test_PDUDaemon__stop():
    daemon = PDUDaemon()

    pdus = {"pdu1": MagicMock(), "pdu2": MagicMock()}
    daemon.pdus = copy(pdus)

    daemon.stop(wait=False)

    assert len(daemon.pdus) == 0
    pdus["pdu1"].stop.assert_called_once_with(wait=False)
    pdus["pdu2"].stop.assert_called_once_with(wait=False)
