from threading import Thread, Event
from dataclasses import asdict, field
from datetime import datetime, timedelta
from ipaddress import IPv4Address
from pathlib import Path
from pprint import pprint
from typing import Optional, Literal

from deepdiff import DeepDiff
from pydantic.dataclasses import dataclass
from pydantic import field_validator, PositiveInt
from inotify_simple import INotify, flags
import errno
import fcntl
import threading
import traceback
import time
import yaml
import os

from .dhcpd import MacAddress
from .logger import logger
from .dut import DUT
from . import config
from . import gitlab


@dataclass
class ConfigPDU:
    driver: str
    config: dict
    reserved_port_ids: list[str] = field(default_factory=list)


@dataclass
class ConfigGitlabRunner:
    token: str = "<invalid default>"
    exposed: bool = True
    runner_id: int = -1

    def verify_or_renew_token(self, gl, description, tags):
        def remove_and_register():
            logger.warning(f"{log_prefix}: Starting the renewal process...")

            if not self.remove(gl):
                logger.error(f"{log_prefix}: Could not unregister the runner on {gl.name}")
                return

            if gl.has_valid_looking_registration_token:
                runner = gitlab.register_runner(gitlab_url=gl.url,
                                                registration_token=gl.registration_token,
                                                description=description,
                                                tag_list=tags,
                                                maximum_timeout=gl.maximum_timeout,
                                                runner_type=gl.runner_type,
                                                group_id=gl.group_id,
                                                project_id=gl.project_id)
                if runner:
                    self.token = runner.token
                    self.runner_id = runner.id
                    logger.info(f"{log_prefix}: Got assigned a token")
                else:
                    logger.error(f"{log_prefix}: Could not register the runner on {gl.name}")
            else:
                logger.error(f"{log_prefix}: No registration tokens specified. Aborting...")

        log_prefix = f"{description}'s {gl.name} runner"

        logger.debug(f"{log_prefix}: Verifying the token")
        if not gitlab.verify_runner_token(gitlab_url=gl.url,
                                          token=self.token) or self.runner_id < 0:
            logger.warning(f"{log_prefix}: The token {self.token} is invalid.")
            remove_and_register()
        else:
            # The runner token is valid, let's check that the tags and description match!
            if gl.has_valid_looking_access_token:
                runner = gitlab.runner_details(gitlab_url=gl.url, private_token=gl.access_token,
                                               runner_id=self.runner_id)

                if runner is not None:
                    needs_re_registering = False
                    if runner.description != description:
                        logger.warning(f"{log_prefix}: The runner's description does not match the local value.")
                        needs_re_registering = True
                    elif set(runner.tag_list) != set(tags):
                        logger.warning(f"{log_prefix}: The runner tags list does not match the local database.")
                        needs_re_registering = True
                    elif runner.maximum_timeout != gl.maximum_timeout:
                        logger.warning(f"{log_prefix}: The runner's maximum timeout does not match the local value.")
                        needs_re_registering = True

                    if needs_re_registering:
                        remove_and_register()
            else:
                logger.warning(f"{log_prefix}: No access token specified, skipping tags verification")

    def remove(self, gl):
        if self.token == "<invalid default>":
            return True

        print(f"Unregister {gl.name}'s runner token")
        if not gitlab.unregister_runner(gitlab_url=gl.url, token=self.token):
            # We failed to remove the runner, make sure the token is still valid
            if gitlab.verify_runner_token(gitlab_url=gl.url, token=self.token):
                return False

        self.token = "<invalid default>"

        return True


@dataclass
class ConfigDUT:
    base_name: str
    ip_address: str  # TODO: Make sure all machines have a unique IP
    tags: list[str]
    manual_tags: list[str] = field(default_factory=list)
    local_tty_device: Optional[str] = None
    gitlab: dict[str, ConfigGitlabRunner] = field(default_factory=dict)
    pdu: Optional[str] = None
    pdu_port_id: Optional[str | int] = None
    pdu_off_delay: float = 30
    ready_for_service: bool = False
    is_retired: bool = False
    first_seen: datetime = field(default_factory=lambda: datetime.now())
    comment: Optional[str] = None

    mac_address: Optional[str] = None

    @field_validator('pdu_port_id')
    @classmethod
    def convert_pdu_port_id_to_str(cls, v):
        return str(v)

    @field_validator('mac_address')
    @classmethod
    def mac_address_is_understood_by_boots(cls, v):
        MacAddress(v)
        return v

    @field_validator('ip_address')
    @classmethod
    def ip_address_is_valid(cls, v):
        IPv4Address(v)
        return str(v)

    @property
    def full_name(self):
        # Get the index of the dut by looking at how many duts with
        # the same base name were registered *before* us.
        idx = 1
        for dut in self.mars_db.duts.values():
            if dut.base_name == self.base_name and dut.first_seen < self.first_seen:
                idx += 1

        return f"{config.FARM_NAME}-{self.base_name}-{idx}"

    # List of attributes that are safe to expose publicly
    @property
    def safe_attributes(self):
        return {
            "id": self.id,
            "base_name": self.base_name,
            "full_name": self.full_name,
            "tags": self.tags,
            "manual_tags": self.manual_tags,
            "mac_address": self.mac_address,
            "ip_address": self.ip_address,
            "local_tty_device": self.local_tty_device,
            "ready_for_service": self.ready_for_service,
            "comment": self.comment
        }

    @property
    def all_tags(self):
        farm_tags = [f"farm:{config.FARM_NAME}"]
        return sorted(set(self.tags + self.manual_tags + farm_tags))

    @property
    def available(self):
        return self.ready_for_service and not self.is_retired

    def expose_on_forges(self):
        # Make sure every gitlab instance is represented in the DUT's config
        for gl in self.mars_db.gitlab.values():
            if self.gitlab.get(gl.name) is None:
                self.gitlab[gl.name] = ConfigGitlabRunner()

        if self.available:
            for gl in self.mars_db.gitlab.values():
                local_cfg = self.gitlab.get(gl.name)
                if gl.expose_runners and local_cfg.exposed:
                    local_cfg.verify_or_renew_token(gl, description=self.full_name, tags=self.all_tags)

    def remove_from_forges(self):
        # Un-register every associated runner
        for gl_name, local_cfg in self.gitlab.items():
            if gl := self.mars_db.gitlab.get(gl_name):
                local_cfg.remove(gl)


@dataclass
class ConfigGitlab:
    url: str
    registration_token: Optional[str] = None
    runner_type: Optional[Literal["instance_type", "group_type", "project_type"]] = "instance_type"
    group_id: Optional[PositiveInt] = None
    project_id: Optional[PositiveInt] = None
    access_token: Optional[str] = None
    expose_runners: bool = True
    maximum_timeout: PositiveInt = 21600
    gateway_runner: Optional[ConfigGitlabRunner] = None

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent
    def __post_init__(self):
        if self.gateway_runner is not None:
            self.gateway_runner.mars_db = self

    @field_validator("url")
    @classmethod
    def url_is_valid(cls, v):
        assert v.startswith("https://")
        return v

    def has_valid_looking_token(self, token):
        return isinstance(token, str) and len(token) >= 8

    @property
    def has_valid_looking_registration_token(self):
        return self.has_valid_looking_token(self.registration_token)

    @property
    def has_valid_looking_access_token(self):
        return self.has_valid_looking_token(self.access_token)

    @property
    def should_expose_gateway_runner(self):
        if not self.expose_runners or self.gateway_runner is None:
            return False

        return self.gateway_runner.exposed


@dataclass
class MarsDB:
    pdus: dict[str, ConfigPDU] = field(default_factory=dict)
    duts: dict[str, ConfigDUT] = field(default_factory=dict)
    gitlab: dict[str, ConfigGitlab] = field(default_factory=dict)

    def reset_taint(self):
        self._disk_state = asdict(self)

    @property
    def diff_from_disk_state(self):
        return DeepDiff(self._disk_state, asdict(self), ignore_order=True)

    @property
    def is_tainted(self):
        return len(self.diff_from_disk_state) > 0

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent
    def __post_init__(self):

        # Always ensure that the VPDU config is in the mars db if the config
        # param is set. This protects against other things that might
        # externally modify (or generate) the mars db (e.g. vivian from the
        # ci-tron project.)
        if config.EXECUTOR_VPDU_ENDPOINT:
            vpdu_config = {"hostname": config.EXECUTOR_VPDU_ENDPOINT}
            if "VPDU" in self.pdus:
                self.pdus["VPDU"].driver = "vpdu"
                self.pdus["VPDU"].config = vpdu_config
            else:
                self.pdus["VPDU"] = ConfigPDU(driver="vpdu", config=vpdu_config)

        # Since we do not want to repeat ourselves in the config file, the name
        # of objects is set in the parent dict. However, it is quite useful for
        # objects to know their names and have access to the DB. This function
        # adds it back!
        for name, pdu in self.pdus.items():
            pdu.name = name
            pdu.mars_db = self

        for dut_id, dut in self.duts.items():
            dut.id = dut_id
            dut.mars_db = self

        for name, gitlab_instance in self.gitlab.items():
            gitlab_instance.name = name
            gitlab_instance.mars_db = self

        self.reset_taint()

        # Perform migrations after resetting the taint so that if the content
        # is modified by any migration, we will end up writing it back to disk

        # 2024/03/21 Migration: If the MAC Address is not set but the dut ID
        # looks like one, make it the mac address too.
        for dut_id, dut in self.duts.items():
            if dut.mac_address is None:
                try:
                    MacAddress(dut_id)
                    dut.mac_address = dut_id
                except Exception:
                    pass

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, 'r') as f:
            cls.__dbLock(f)
            data = yaml.safe_load(f)
            return cls(**data if data else {})

    def save(self, file_path):
        with open(file_path, 'w') as f:
            self.__dbLock(f)
            yaml.dump(asdict(self), f, sort_keys=False)
            f.flush()
            os.fsync(f.fileno())
        self.reset_taint()

    # __dbLock returns as soon as an exclusive lock is acquired, else will
    # retry 5 times over 5 seconds, and raise a RuntimeError if unable to
    # acquire the lock after that period.
    @staticmethod
    def __dbLock(file):
        for tries in range(5):
            try:
                fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as e:
                if e.errno in [errno.EACCES, errno.EAGAIN]:
                    time.sleep(1)
                    continue
                raise RuntimeError(f"unable to lock file: {file.filename}")

            # lock successfully acquired
            return

        raise RuntimeError(f"timed out trying to lock file: {file.filename}")


class MarsDBAccess:
    def __init__(self, mars):
        self._mars = mars
        self.entered_at = None

    def __enter__(self):
        self._mars._db_lock.acquire()
        self.entered_at = time.monotonic()
        return self._mars._db

    def __exit__(self, *args):
        self._mars.save_db_if_needed()
        self._mars._db_lock.release()

        held_time = (time.monotonic() - self.entered_at) * 1000.0
        if held_time > 100:
            logger.warning(f"MaRS DB lock held for an unusually long time: {held_time:.1f} ms")


class Mars(Thread):
    def __init__(self, pdu_daemon):
        super().__init__(name='MarsClient')

        self.pdu_daemon = pdu_daemon

        self._db = None
        self._db_lock = threading.RLock()  # Reentrant lock

        self._duts = {}
        self._discover_data = {}

        self.stop_event = Event()

    @property
    def discover_data(self):
        if self._discover_data:
            delta = time.monotonic() - self._discover_data.get('started_at')
            if delta >= self._discover_data.get('timeout'):
                self._discover_data = {}

        return self._discover_data

    @discover_data.setter
    def discover_data(self, value):
        self._discover_data = value

    def machine_discovered(self, dut_data, update_if_already_exists=False):
        machine = self.get_machine_by_id(dut_data.get('id'), raise_if_missing=False)

        if machine is None and self.discover_data:
            with self.db:
                # A new machine is about to be added through the discovery process

                pdu_port_id = self.discover_data.get('port_id')
                pdu_name = self.discover_data.get('pdu')

                machine = None
                if pdu_port := self.get_pdu_port_by_name(pdu_name, pdu_port_id):
                    dut_data["pdu_port_id"] = pdu_port_id
                    dut_data["pdu"] = pdu_name
                    dut_data["pdu_off_delay"] = pdu_port.pdu.default_min_off_time
                else:
                    logger.error(f"Discovery failed: The PDU port {pdu_name}/{pdu_port_id} doesn't exist in our DB")
                    # NOTE: We still want to create the DUT

                # We used the discovery data, so let's remove all of it
                self.discover_data = {}

                return self.add_or_update_machine(dut_data)
        elif machine is None:
            logger.warning("New machine found, despite no discovery process being in progress")

        if update_if_already_exists:
            return self.add_or_update_machine(dut_data)

    @property
    def db(self):
        return MarsDBAccess(self)

    @property
    def known_machines(self):
        with self._db_lock:
            return list(self._duts.values())

    def get_machine_by_id(self, machine_id, raise_if_missing=False):
        with self._db_lock:
            machine = self._duts.get(machine_id)
            if machine is None:
                # We could not find the machine by its actual ID, try finding it by full_name instead!
                for dut in self._duts.values():
                    if dut.full_name == machine_id:
                        machine = dut
                        break

            if machine is None and raise_if_missing:
                raise ValueError(f"Unknown machine ID '{machine_id}'")
            return machine

    def _machine_update_or_create(self, db_dut):
        with self._db_lock:
            dut = self._duts.get(db_dut.id)
            if dut is None:
                dut = DUT(mars=self, db_dut=db_dut)
                self._duts[dut.id] = dut
            else:
                dut.config_changed(db_dut=db_dut)

            self._db.duts[dut.id] = db_dut

            return dut

    def get_pdu_by_name(self, pdu_name, raise_if_missing=False):
        with self.db as mars_db:
            for name, pdu_cfg in mars_db.pdus.items():
                if name == pdu_name:
                    return self.pdu_daemon.get_or_create(pdu_cfg.driver, pdu_cfg.name,
                                                         pdu_cfg.config, pdu_cfg.reserved_port_ids,
                                                         update_if_existing=True)

        if raise_if_missing:
            raise ValueError(f'PDU "{pdu_name}" does not exist')

    def get_pdu_port_by_name(self, pdu_name, pdu_port_id, raise_if_missing=False, timeout=None):
        with self.db:
            pdu = self.get_pdu_by_name(pdu_name, raise_if_missing)

            if port := pdu.get_port_by_id(pdu_port_id, timeout=timeout):
                return port

        if raise_if_missing:
            raise ValueError(f'PDU "{pdu_name}" does not have a port ID named {pdu_port_id}')

    def save_db_if_needed(self):
        # TODO: Raise here if the lock is not currently held (no idea how to do that with an RLock)

        with self._db_lock:
            if self._db.is_tainted:
                print("Write-back the MarsDB to disk, after some local changes:")
                pprint(self._db.diff_from_disk_state, indent=2)
                print()

                self._db.save(config.MARS_DB_FILE)

    def add_or_update_machine(self, fields: dict):
        with self._db_lock:
            dut_id = fields.pop("id")

            if db_dut := self._db.duts.get(dut_id):
                cur_state = asdict(db_dut)
                db_dut = ConfigDUT(**(cur_state | fields))
            else:
                db_dut = ConfigDUT(**fields)

            # TODO: Try to find a way not to have to add these fields
            db_dut.id = dut_id
            db_dut.mars_db = self._db

            machine = self._machine_update_or_create(db_dut)
            self.save_db_if_needed()

        return machine

    def remove_machine(self, machine_id):
        with self._db_lock:
            machine = self._duts.pop(machine_id, None)
            if machine:
                # Stop thread
                machine.stop_machine()

                # Remove the associated DUT in MaRS DB
                self._db.duts.pop(machine_id, None)

                # Kill the gitlab runner token
                machine.remove_from_forges()

                # Save any change that may have happened after reloading
                self.save_db_if_needed()

                return True

            return False

    def sync_machines(self):
        with self.db:
            self._db = MarsDB.from_file(config.MARS_DB_FILE)

            local_only_machines = set(self.known_machines)
            for m in self._db.duts.values():

                machine = self._machine_update_or_create(m)

                # Remove the machine from the list of local-only machines
                local_only_machines.discard(machine)

            # Delete all the machines that are not found in MaRS
            for machine in local_only_machines:
                self._duts[machine.id].stop_machine()
                del self._duts[machine.id]

        # NOTE: Release the lock before checking doing any sort of IO

        # Expose the gateway runners
        for gl in self._db.gitlab.values():
            if gl.should_expose_gateway_runner:
                gl.gateway_runner.verify_or_renew_token(gl,
                                                        description=f"{config.FARM_NAME}-gateway",
                                                        tags=gitlab.generate_gateway_runner_tags())

        # Configure the DUTs
        for m in self._db.duts.values():
            # Expose the DUTs on all the forges
            m.expose_on_forges()

        # Update the gitlab runner configuration
        gitlab.generate_runner_config(self._db)

        # Save any change that may have happened after reloading
        self.save_db_if_needed()

    def stop(self, wait=True):
        self.stop_event.set()

        # Signal all the executors we want to stop
        for machine in self.known_machines:
            machine.stop_event.set()

        if wait:
            self.join()

    def join(self):
        for machine in self.known_machines:
            machine.join()
        super().join()

    def run(self):
        # Make sure the config file exists
        Path(config.MARS_DB_FILE).touch(exist_ok=True)

        # Set up a watch
        inotify = INotify()
        watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
        inotify.add_watch(config.MARS_DB_FILE, watch_flags)

        # Now wait for changes to the file
        last_sync = None
        while not self.stop_event.is_set():
            try:
                reason = None
                if last_sync is None:
                    reason = "Initial boot"
                elif len(inotify.read(timeout=1000)) > 0:
                    reason = "Got updated on disk"
                elif datetime.now() - last_sync > timedelta(minutes=30):
                    reason = "Periodic check"

                if reason:
                    logger.info(f"Syncing the MaRS DB. Reason: {reason}")

                    self.sync_machines()
                    last_sync = datetime.now()
            except Exception:
                traceback.print_exc()
                logger.info("Trying again in 60 seconds")
                time.sleep(60)
