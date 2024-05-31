from collections import defaultdict
from dataclasses import asdict, field
from datetime import datetime
from subprocess import Popen, PIPE, DEVNULL
from enum import Enum
from typing import Dict, List, Optional
from threading import Thread, Event
import subprocess
import traceback
import tempfile
import socket
import requests
import tarfile
import fcntl
import time
import json
import dataclasses
import yaml
import sys
import os

from pydantic import field_validator
from pydantic.dataclasses import dataclass
import requests_unixsocket

from .boots import BootConfig
from .job import Job
from .logger import logger
from .message import JobStatus, MessageType, Message
from .pdu import PDUState
from . import config


@dataclass
class CallbackEndpoint:
    host: str
    port: int


@dataclass
class MinIOCredentials:
    access_key: Optional[str] = None
    secret_key: Optional[str] = None


# WARNING: This class is duplicated from job.py until marshmallow gets replaced by pydantic dataclasses
@dataclass
class Target:
    id: Optional[str] = None
    tags: Optional[List[str]] = field(default_factory=list)

    @field_validator('tags')
    @classmethod
    def tags_must_be_a_list(cls, v):
        if v is None:
            return []
        else:
            return v


class DUTState(Enum):
    WAIT_FOR_CONFIG = 0
    IDLE = 1
    TRAINING = 2
    QUEUED = 3
    RUNNING = 4
    RETIRED = 5
    UNKNOWN = 6
    QUICK_CHECK = 7
    BORKED = 8


@dataclass(kw_only=True)
class JobRequest:
    version: int
    raw_job: str
    target: Target
    callback_endpoint: CallbackEndpoint
    minio_credentials: MinIOCredentials

    job_id: Optional[str]
    http_headers: Dict[str, str] = field(default_factory=dict)
    minio_groups: List[str] = field(default_factory=list)
    job_bucket_initial_state_tarball_file_fd: int = 0

    def cleanup(self):
        if self.job_bucket_initial_state_tarball_file_fd > 0:
            try:
                os.close(self.job_bucket_initial_state_tarball_file_fd)
            except Exception:
                logger.error(f"ERROR: Failed to close the initial state tarball file fd!\n{traceback.format_exc()}")
            finally:
                # Unconditionally mark the fd as freed, even if we failed to
                # close it because it is better to leak the fd than potentially
                # closing someone else's fd later down the line when this object
                # gets garbage collected.
                self.job_bucket_initial_state_tarball_file_fd = 0

    def __del__(self):
        self.cleanup()

    @field_validator("job_id")
    @classmethod
    def job_id_isnt_empty(cls, v):
        if not v:
            now = int(datetime.utcnow().timestamp())
            v = f"untitled-{now}"
        return v

    @field_validator("callback_endpoint")
    @classmethod
    def callback_endpoint_is_set(cls, v):
        if v.host is None:
            raise ValueError("callback's host cannot be None. Leave empty to get the default value")
        if v.port is None:
            raise ValueError("callback's port cannot be None")
        return v

    @classmethod
    def parse(cls, request):
        if request.mimetype == "application/json":
            return JSONJobRequest(request)
        elif request.mimetype == "multipart/form-data":
            return MultipartJobRequest(request)
        else:
            raise ValueError("Unknown job request format")


# DEPRECATED: To be removed when we are sure all the clients out there have been updated
class JSONJobRequest(JobRequest):
    def __init__(self, request):
        job_params = request.json
        metadata = job_params["metadata"]
        job = Job.render_with_resources(job_params["job"])

        # Use the client-provided host callback if available, or default to the remote addr
        remote_addr = metadata.get("callback_host", request.remote_addr)
        endpoint = CallbackEndpoint(remote_addr, metadata.get("callback_port"))

        super().__init__(http_headers=dict(request.headers), version=0, raw_job=job_params["job"],
                         target=job.target, callback_endpoint=endpoint,
                         minio_credentials=MinIOCredentials())


class InvalidTarballFile(Exception):
    pass


class MultipartJobRequest(JobRequest):
    def __init__(self, request):
        metadata_file = request.files.get('metadata')
        if metadata_file is None:
            raise ValueError("No metadata file found")

        if metadata_file.mimetype != "application/json":
            raise ValueError("The metadata file has the wrong mimetype: "
                             "{metadata_file.mimetype}} instead of application/json")

        try:
            metadata = json.loads(metadata_file.read())
        except json.JSONDecodeError as e:
            raise ValueError(f"The metadata file is not a valid JSON file: {e.msg}")

        version = metadata.get('version')
        if version == 1:
            self.parse_v1(request, metadata)
        else:
            raise ValueError(f"Invalid request version {version}")

    def parse_v1(self, request, metadata):
        # Get the job file, and check its mimetype
        job_file = request.files['job']
        if job_file.mimetype != "application/x-yaml":
            raise ValueError("The metadata file has the wrong mimetype: "
                             "{job_file.mimetype}} instead of application/x-yaml")

        # Get the initial state tarball.
        # Since flask files can be either in memory or on the disk, let's write its content
        # to a temporary file, keep a reference open by tying it to the lifetime of this object,
        # then store the fd in job_bucket_initial_state_tarball_file_fd. This file descriptor
        # will then be passed to the executor instance that will execute the job at which point
        # the object can be deleted automatically and the filedescriptor will get closed.
        initial_state_tarball_file = request.files.get('job_bucket_initial_state_tarball_file', None)
        if initial_state_tarball_file and initial_state_tarball_file.mimetype != "application/octet-stream":
            raise ValueError("The job_bucket_initial_state_tarball file has the wrong mimetype: "
                             "{initial_state_tarball_file.mimetype}} instead of application/octet-stream")
        if initial_state_tarball_file:
            job_bucket_initial_state_tarball_file_fd, file_path = tempfile.mkstemp()

            # Make sure the file doesn't linger on the disk even if everything crashes
            os.unlink(file_path)

            with os.fdopen(job_bucket_initial_state_tarball_file_fd, 'w+b', closefd=False) as tmp_file:
                while chunk := initial_state_tarball_file.read(1000000):
                    tmp_file.write(chunk)

                # Check if the file passed is a valid tarball, or raise InvalidTarballFile
                # NOTE: We make sure to rewind the file before and after the check!
                tmp_file.seek(0)
                if not tarfile.is_tarfile(tmp_file):
                    raise InvalidTarballFile()
                tmp_file.seek(0)
        else:
            job_bucket_initial_state_tarball_file_fd = -1

        # Create a Job object
        raw_job = job_file.read().decode()
        job = Job.render_with_resources(raw_job)

        # Get the target that will run the job. Use the job's target by default,
        # but allow the client to override the target
        if "target" in metadata:
            target = metadata.get('target', {})
            job_target = Target(target.get('id'), target.get('tags', []))
        else:
            job_target = Target(id=job.target.id, tags=job.target.tags)

        # Use the client-provided host callback if available, or default to the remote addr
        callback = metadata.get('callback', {})
        remote_addr = callback.get("host", request.remote_addr)
        endpoint = CallbackEndpoint(remote_addr, callback.get("port"))

        # Parse the minio-related arguments request
        minio = metadata.get('minio', {})
        minio_credentials = minio.get('credentials', {})
        credentials = MinIOCredentials(access_key=minio_credentials.get("access_key"),
                                       secret_key=minio_credentials.get("secret_key"))

        super().__init__(http_headers=dict(request.headers), version=1, raw_job=raw_job,
                         target=job_target, callback_endpoint=endpoint,
                         job_bucket_initial_state_tarball_file_fd=job_bucket_initial_state_tarball_file_fd,
                         job_id=metadata.get('job_id'),
                         minio_credentials=credentials,
                         minio_groups=minio.get('groups', []))


class SergentHartmanState(Enum):
    IDLE = 0
    ENROLLING = 1
    QUICK_CHECK = 2
    REGISTRATION_FAILED = 3


class SergentHartman:
    def __init__(self, machine, boot_loop_counts=None, qualifying_rate=None, quick_check=None):
        super().__init__()

        if boot_loop_counts is None:
            boot_loop_counts = int(config.SERGENT_HARTMAN_BOOT_COUNT)

        if qualifying_rate is None:
            qualifying_rate = int(config.SERGENT_HARTMAN_QUALIFYING_BOOT_COUNT)

        if quick_check is None:
            quick_check = config.as_boolean("SERGENT_HARTMAN_QUICK_CHECK")

        self.machine = machine
        self.boot_loop_counts = boot_loop_counts
        self.qualifying_rate = qualifying_rate
        self.quick_check = quick_check
        self._state = None
        self.registration_failed_at = None

        # Tri-state boolean
        self.result = None

        self.set_state(SergentHartmanState.IDLE)

    @property
    def is_active(self):
        return self.state != SergentHartmanState.IDLE

    @property
    def state(self):
        def registration_failed_expiration_time():
            delay = int(config.SERGENT_HARTMAN_REGISTRATION_RETRIAL_DELAY)
            return self.registration_failed_at + delay if self.registration_failed_at is not None else 0

        if self._state == SergentHartmanState.ENROLLING and registration_failed_expiration_time() > time.monotonic():
            return SergentHartmanState.REGISTRATION_FAILED
        else:
            return self._state

    def set_state(self, state):
        def reset():
            self.is_machine_registered = False
            self.cur_loop = 0
            self.statuses = defaultdict(int)
            self.result = None
            self.registration_failed_at = None

        if self.state == state:
            return
        elif state == SergentHartmanState.IDLE:
            reset()
        elif self.state == SergentHartmanState.IDLE and state == SergentHartmanState.ENROLLING:
            pass
        elif self.state == SergentHartmanState.IDLE and state == SergentHartmanState.QUICK_CHECK:
            pass
        elif state == SergentHartmanState.REGISTRATION_FAILED:
            reset()
            self.registration_failed_at = time.monotonic()
            state = SergentHartmanState.ENROLLING
        else:
            raise ValueError(f"{self.state} -> {state} is an invalid transition")

        self._state = state

    def _next_task(self, callback_port):
        mid = self.machine.id

        if self.state == SergentHartmanState.ENROLLING:
            if not self.is_machine_registered:
                # Start by forcing the machine to register itself to make sure the
                # its configuration is up to date (especially the serial console
                # port). Loop until it succeeds!
                job_path = config.EXECUTOR_REGISTRATION_JOB

                logger.info("SergentHartman/%s - Try registering the machine", mid)
            else:
                # Check that we got the expected amount of reports
                if self.cur_loop != sum(self.statuses.values()):
                    raise ValueError("The previous next_task() call was not followed by a call to report()")

                # The registration went well, let's start the boot loop!
                self.cur_loop += 1

                statuses_str = [f"{status.name}: {values}" for status, values in self.statuses.items()]
                logger.info("SergentHartman/%s - loop %s/%s - statuses %s: "
                            "Execute one more round!",
                            mid,
                            self.cur_loop,
                            self.boot_loop_counts,
                            statuses_str)

                job_path = config.EXECUTOR_BOOTLOOP_JOB
        elif self.state == SergentHartmanState.QUICK_CHECK:
            logger.info("SergentHartman/%s - Initial check", mid)
            job_path = config.EXECUTOR_BOOTLOOP_JOB
        else:
            raise ValueError(f"There are no next tasks when the state is {self.state.name}")

        with open(job_path, "r") as f:
            raw_job = f.read()

            callback_endpoint = CallbackEndpoint(host="127.0.0.1", port=callback_port)
            return JobRequest(version=1, job_id=None, raw_job=raw_job,
                              target=Target(), callback_endpoint=callback_endpoint,
                              minio_credentials=MinIOCredentials())

    def _report(self, job_status, execution_time):
        mid = self.machine.id

        if self.state == SergentHartmanState.ENROLLING:
            if self.cur_loop == 0:
                if job_status != JobStatus.PASS:
                    delay = int(config.SERGENT_HARTMAN_REGISTRATION_RETRIAL_DELAY)
                    logger.warning((f"SergentHartman/{mid} - Registration failed with status {job_status.name}. "
                                    f"Retrying in {delay} second(s)"))
                    self.set_state(SergentHartmanState.REGISTRATION_FAILED)
                else:
                    self.is_machine_registered = True
                    if self.boot_loop_counts >= 1:
                        logger.info(f"SergentHartman/{mid} - Registration succeeded, moving on to the boot loop")
                    else:
                        logger.info(f"SergentHartman/{mid} - Registration succeeded, boot loops disabled")
                        self.result = True
            else:
                # We are in the boot loop
                self.statuses[job_status] += 1

                if self.cur_loop >= self.boot_loop_counts:
                    self.result = self.statuses[JobStatus.PASS] >= self.qualifying_rate
        elif self.state == SergentHartmanState.QUICK_CHECK:
            self.result = (job_status == JobStatus.PASS)

            if job_status == JobStatus.PASS:
                logger.info(f"SergentHartman/{mid} - Initial check successful after {execution_time:.2f} seconds")
            else:
                logger.error(f"SergentHartman/{mid} - Initial check failed after {execution_time:.2f} seconds")
        else:
            raise ValueError(f"Reporting unsupported on the state {self.state.name}")

    def execute_next_task(self, stop_event):
        if self.state in [SergentHartmanState.IDLE, SergentHartmanState.REGISTRATION_FAILED]:
            # Nothing to do here
            return

        if stop_event.is_set():
            return

        # If we are asked for fewer than 0 bootloops, consider Sergent Hartman disabled
        if self.boot_loop_counts < 0:
            self.result = True
            return

        # If we were asked to quick check but quick check was disabled, pretend we ran it
        # already
        if self.state == SergentHartmanState.QUICK_CHECK and not self.quick_check:
            self.result = True
            return

        start_time = time.monotonic()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_server:
            tcp_server.bind(('', 0))
            tcp_server.listen(1)
            local_port = tcp_server.getsockname()[1]

            # Queue the job
            status = DUTState.UNKNOWN
            try:
                proc = self.machine.start_job(self._next_task(callback_port=local_port), quiet=True)

                print(f"Waiting for the executor to connect to our local port {local_port}")
                tcp_server.settimeout(5)
                try:
                    job_socket, _ = tcp_server.accept()
                except socket.timeout:
                    proc.kill()
                    proc.wait(timeout=10)
                    raise ValueError("The server failed to initiate a connection")

                # Set the resulting socket's timeout to blocking
                job_socket.settimeout(None)

                # Wait for the end message
                status_msg = JobStatus.UNKNOWN
                try:
                    while not stop_event.is_set():
                        msg = Message.next_message(job_socket)

                        if msg.msg_type == MessageType.SESSION_END:
                            status_msg = msg.status
                            break
                except Exception:
                    traceback.print_exc()

                # Close the socket to signal we are done
                job_socket.shutdown(socket.SHUT_RDWR)
                job_socket.close()

                # Wait for the process to die
                status_exit_code = JobStatus.UNKNOWN
                try:
                    proc.wait(timeout=10)
                    status_exit_code = JobStatus(proc.returncode)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    raise ValueError("The process never finished")
                except ValueError:
                    logger.error(f"The exit status {proc.returncode} is an invalid value for JobStatus")

                # Check that the status reported by the SESSION_END message matches
                # the one we got from
                if status_msg != JobStatus.UNKNOWN and \
                   status_exit_code != JobStatus.UNKNOWN and \
                   status_msg != status_exit_code:
                    raise ValueError("Mismatch detected between the END_MESSAGE's and the exit code's status")

                # report the status
                status = status_msg if status_msg != JobStatus.UNKNOWN else status_exit_code
            finally:
                execution_time = time.monotonic() - start_time
                self._report(job_status=status, execution_time=execution_time)

    @property
    def is_available(self):
        return config.EXECUTOR_REGISTRATION_JOB or config.EXECUTOR_BOOTLOOP_JOB


def lock_fd(fd, attempts=100):
    last_exc = None

    for i in range(attempts):
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return
        except BlockingIOError as e:
            if e.errno == 11:
                last_exc = e
                time.sleep(0.01)
                continue
            else:
                raise e

    raise last_exc


@dataclass
class PduPortStats:
    last_polled: Optional[datetime] = None
    last_known_state: Optional[PDUState] = None
    last_shutdown: Optional[datetime] = None

    def serialize(self):
        fields = asdict(self)
        fields['last_known_state'] = fields['last_known_state'].value
        return fields

    @classmethod
    def from_pdu_port(cls, port):
        fields = {f.name: getattr(port, f.name) for f in dataclasses.fields(cls)}
        return cls(**fields)


class DUT(Thread):
    def __init__(self, mars, db_dut):
        self.mars = mars
        self.config_changed(db_dut)

        # Training / Qualifying process
        self.sergent_hartman = SergentHartman(self)

        # Queue a quick check
        self.quick_check_queued = Event()
        if self.ready_for_service and not self.is_retired:
            self.quick_check_queued.set()

        # Start the background thread that will manage the machine
        super().__init__(name=f'ExecutorThread-{self.id}')
        self.stop_event = Event()
        self.start()

    def stop_machine(self):
        self.stop_event.set()
        self.cancel_job()
        self.join()

    # Expose all the fields of the associated ConfigDUT object
    def __getattr__(self, attr):
        return getattr(self.db_dut, attr)

    @property
    def ready_for_service(self):
        return self.db_dut.ready_for_service

    @ready_for_service.setter
    def ready_for_service(self, val):
        self.update_fields({"ready_for_service": val})

    @property
    def is_retired(self):
        return self.db_dut.is_retired

    @is_retired.setter
    def is_retired(self, val):
        self.update_fields({"is_retired": val})

    @property
    def pdu_port(self):
        if self._pdu_port is None:
            self._pdu_port = self.mars.get_pdu_port_by_name(self.db_dut.pdu,
                                                            self.db_dut.pdu_port_id,
                                                            raise_if_missing=False,
                                                            timeout=0)
            if self._pdu_port:
                self._pdu_port.min_off_time = self.db_dut.pdu_off_delay

        return self._pdu_port

    def config_changed(self, db_dut=None):
        self.db_dut = db_dut

        # Invalidate the PDU port cache
        self._pdu_port = None

    def update_fields(self, fields):
        with self.mars.db as mars_db:
            db_dut = mars_db.duts[self.id]

            updated_fields = set()
            for k, v in fields.items():
                if getattr(self.db_dut, k, None) == v:
                    continue

                if k == 'is_retired':
                    if self.is_retired and not v:
                        self.quick_check_queued.set()

                setattr(db_dut, k, v)

                updated_fields.add(k)

            if len(updated_fields) > 0:
                self.config_changed(db_dut)

    @property
    def _executor_socket_path(self):
        dut_id = self.id.replace(":", "_")
        return f"/var/run/executor/{dut_id}.sock"

    @property
    def _executor_lock_path(self):
        return f"{self._executor_socket_path}.lock"

    def _executor_query(self, path, method="get"):
        session = requests_unixsocket.Session()
        r = getattr(session, method)(f'http+unix://{self._executor_socket_path.replace("/", "%2F")}{path}')
        return r

    @property
    def state(self):
        def job_process_state():
            try:
                r = self._executor_query("/api/v1/state")
                if r.status_code == 200:
                    q = r.json()
                    state = q.get("state")
                    try:
                        return DUTState[state]
                    except KeyError:
                        return DUTState.UNKNOWN
                else:
                    return DUTState.QUEUED
            except (requests.exceptions.ConnectionError, FileNotFoundError):
                # Verify that the lock is not held by anyone before declaring
                # the machine is IDLE
                try:
                    with open(self._executor_lock_path, "r") as f:
                        lock_fd(f, attempts=5)

                        # The lock was available, the machine can be considered IDLE
                        return DUTState.IDLE
                except BlockingIOError:
                    # The lock was not available, the machine may still be in use
                    return DUTState.BORKED
                except FileNotFoundError:
                    # The lock file does not exist, the machine must be idle
                    return DUTState.IDLE

            return DUTState.IDLE

        state = job_process_state()

        if state == DUTState.IDLE:
            # If the state is IDLE, check what state we should give it
            if self.pdu_port is None:
                return DUTState.WAIT_FOR_CONFIG
            elif self.is_retired:
                return DUTState.RETIRED
            elif not self.ready_for_service:
                return DUTState.TRAINING
            elif self.quick_check_queued.is_set():
                return DUTState.QUICK_CHECK
        elif self.sergent_hartman.state == SergentHartmanState.ENROLLING:
            return DUTState.TRAINING
        elif self.sergent_hartman.state == SergentHartmanState.QUICK_CHECK:
            return DUTState.QUICK_CHECK

        return state

    def start_job(self, job_request, quiet=False):
        if self.pdu_port is None:
            raise ValueError("Can't start a job until the PDU port is properly setup")

        # Create the configuration for the run
        config = {
            "executor_job_version": 1,
            "mars_db": asdict(self.mars_db),
            "job_request": asdict(job_request),
            "machine_id": self.id,
            "pdu_port_stats": PduPortStats.from_pdu_port(self.pdu_port).serialize()

        }

        # Compute the list of file descriptors to pass to the next client
        if job_request.job_bucket_initial_state_tarball_file_fd > 0:
            pass_fds = [job_request.job_bucket_initial_state_tarball_file_fd]
        else:
            pass_fds = []

        # Execute the job
        proc = Popen(["executor", "run-job", "-s", self._executor_socket_path,
                      "-l", self._executor_lock_path],
                     stdin=PIPE, stdout=sys.stdout if not quiet else DEVNULL,
                     stderr=sys.stderr if not quiet else DEVNULL,
                     pass_fds=pass_fds)
        yaml.dump(config, proc.stdin, sort_keys=False, encoding='utf-8')
        proc.stdin.flush()
        proc.stdin.close()

        # Wait for 15s for the unix socket to appear, or kill the process
        start = time.monotonic()
        while time.monotonic() - start < 15:
            try:
                self._executor_query("/api/v1/state")
                return proc
            except requests.exceptions.ConnectionError:
                pass

        # Seems like the start-up process did not work, kill the process!
        proc.kill()
        proc.wait()
        raise ValueError("The job process failed to start")

    def cancel_job(self):
        try:
            r = self._executor_query("/api/v1/job/cancel", method="post")
            return r.status_code == 200
        except requests.exceptions.ConnectionError:
            # Nothing to do
            return True

    def boot_config_query(self, platform=None, buildarch=None, bootloader=None):
        try:
            url = f"/api/v1/boot/config?platform={platform}&buildarch={buildarch}&bootloader={bootloader}"
            q = self._executor_query(url)
            if q.status_code == 200:
                return BootConfig(**q.json())
        except Exception:
            traceback.print_exc()
            return None

    def run(self):
        while not self.stop_event.is_set():
            try:
                if self.state == DUTState.TRAINING and self.sergent_hartman.state == SergentHartmanState.IDLE:
                    self.sergent_hartman.set_state(SergentHartmanState.ENROLLING)
                elif self.state == DUTState.QUICK_CHECK and self.sergent_hartman.state == SergentHartmanState.IDLE:
                    self.sergent_hartman.set_state(SergentHartmanState.QUICK_CHECK)
                elif self.sergent_hartman.state == SergentHartmanState.ENROLLING and (self.ready_for_service or
                                                                                      self.is_retired):
                    # Cancel enrollment
                    self.sergent_hartman.set_state(SergentHartmanState.IDLE)

                if self.sergent_hartman.is_active:
                    self.sergent_hartman.execute_next_task(stop_event=self.stop_event)

                    # Check if we are done
                    if self.sergent_hartman.result is not None and not self.stop_event.is_set():
                        if self.sergent_hartman.state == SergentHartmanState.ENROLLING:
                            self.ready_for_service = self.sergent_hartman.result
                        elif self.sergent_hartman.state == SergentHartmanState.QUICK_CHECK:
                            if not self.sergent_hartman.result:
                                self.ready_for_service = False
                            self.quick_check_queued.clear()

                        self.sergent_hartman.set_state(SergentHartmanState.IDLE)

            except Exception:
                traceback.print_exc()

            # Wait for a second before starting a new round of testing
            self.stop_event.wait(1)
