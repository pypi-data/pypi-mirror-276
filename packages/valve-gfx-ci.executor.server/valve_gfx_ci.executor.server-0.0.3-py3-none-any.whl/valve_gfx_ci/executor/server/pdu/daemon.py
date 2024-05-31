from datetime import timedelta
from enum import IntEnum, auto
from threading import Thread, Event, Lock

import traceback

from . import PDU, logger


class AsyncPDUState(IntEnum):
    CREATED = auto()
    INITIALIZING = auto()
    ERROR = auto()
    STOPPED = auto()
    OK = auto()


class AsyncPDU(Thread):
    def __init__(self, model_name, pdu_name, config, reserved_port_ids=[], polling_interval=timedelta(seconds=1)):
        super().__init__(name=f'AsyncPDU-{pdu_name}')

        self.model_name = model_name
        self.pdu_name = pdu_name
        self.config = config
        self.reserved_port_ids = set(reserved_port_ids)
        self.polling_interval = polling_interval

        self.driver = None
        self.ports = []
        self.error = None
        self.port_polling_failure_count = 0

        self.started_event = Event()
        self.stop_event = Event()

    def __eq__(self, other):
        for field in ["model_name", "pdu_name", "config", "reserved_port_ids"]:
            if getattr(self, field) != getattr(other, field):
                return False
        return True

    def __hash__(self):
        return hash(id(self))

    def get_port_by_id(self, port_id, timeout=None):
        if not self.started_event.is_set():
            logger.info("Waiting for the PDU initialization to complete!")

        self.started_event.wait(timeout)

        for port in self.ports:
            if str(port.port_id) == str(port_id):
                return port

    @property
    def state(self):
        if self.native_id is None:
            return AsyncPDUState.CREATED

        if not self.is_alive():
            return AsyncPDUState.STOPPED

        if self.error:
            return AsyncPDUState.ERROR

        if not self.started_event.is_set():
            return AsyncPDUState.INITIALIZING

        return AsyncPDUState.OK

    def stop(self, wait=True):
        self.stop_event.set()

        if wait:
            self.join()

    def run(self):
        while not self.stop_event.is_set():
            self.started_event.clear()

            try:
                self.driver = PDU.create(model_name=self.model_name, pdu_name=self.pdu_name,
                                         config=self.config, reserved_port_ids=self.reserved_port_ids)
                self.ports = self.driver.ports
            except Exception as e:
                # We failed to initialize the driver, retry after a small delay
                traceback.print_exc()
                self.error = str(e)
                self.stop_event.wait(15)
                continue

            # We successfully instantiated the driver
            self.port_polling_failure_count = 0
            self.error = None
            self.started_event.set()

            while not self.stop_event.is_set():
                try:
                    self.ports = self.driver.ports
                    for port in self.ports:
                        # Update the port
                        port.state

                    # Reset the error counter
                    self.port_polling_failure_count = 0
                except Exception:  # pragma: nocover
                    # If we had 10 consecutive polling errors, try reinitializing the driver
                    self.port_polling_failure_count += 1
                    if self.port_polling_failure_count == 10:
                        break

                    traceback.print_exc()

                self.stop_event.wait(self.polling_interval.total_seconds())


class PDUDaemon:
    def __init__(self):
        self.pdus_lck = Lock()
        self.pdus = dict()

    def stop(self, wait=True):
        with self.pdus_lck:
            while len(self.pdus) > 0:
                _, pdu = self.pdus.popitem()
                pdu.stop(wait=wait)

    def get_or_create(self, *args, update_if_existing=False, **kwargs):
        new_pdu = AsyncPDU(*args, **kwargs)

        with self.pdus_lck:
            cur_pdu = self.pdus.get(new_pdu.pdu_name)

            if cur_pdu:
                if not update_if_existing:
                    # We have found a PDU which has the right name, and we don't care
                    # about updating its configuration, so let's just return it
                    return cur_pdu
                elif cur_pdu == new_pdu:
                    # We have found a PDU which has the right name, we want to update,
                    # but the config has not changed, so let's return the existing pdu
                    # after making sure that we use the expected polling interval
                    cur_pdu.polling_interval = new_pdu.polling_interval
                    return cur_pdu
                else:
                    # We have found a PDU which has the right name, but the
                    # configuration has changed so we need to delete the existing one
                    # and re-create it
                    cur_pdu.stop(wait=False)
                    del self.pdus[cur_pdu.pdu_name]

            # Start polling on the new_pdu, and add it to the list of registered PDUs
            new_pdu.start()
            self.pdus[new_pdu.pdu_name] = new_pdu

            return new_pdu

    def unregister_pdu(self, name):
        with self.pdus_lck:
            if pdu := self.pdus.pop(name, None):
                pdu.stop()
