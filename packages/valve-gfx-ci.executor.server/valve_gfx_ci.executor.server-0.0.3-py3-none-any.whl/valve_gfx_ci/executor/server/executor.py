#!/usr/bin/env python3

from dataclasses import asdict, fields
from datetime import datetime
from functools import cached_property
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from threading import Thread, Event
from collections import namedtuple
from urllib.parse import urlsplit, urlparse
from enum import IntEnum

from cachecontrol import CacheControl
from cachecontrol.caches.file_cache import FileCache
from pydantic import field_validator
from pydantic.dataclasses import dataclass

from .android.fastbootd import FastbootDevice
from .dut import JobRequest, DUTState, lock_fd, PduPortStats
from .mars import MarsDB
from .message import LogLevel, JobIOMessage, ControlMessage, SessionEndMessage, Message, MessageType
from .pdu import PDUState, PDU
from .message import JobStatus
from .job import Job
from .logger import logger
from .minioclient import MinioClient, MinIOPolicyStatement, generate_policy
from . import config
from .boots import BootConfig
from .boots_db import BootsDB

import subprocess
import traceback
import threading
import requests
import tempfile
import logging
import secrets
import random
import select
import string
import shutil
import socket
import struct
import fcntl
import flask
import json
import time
import yaml
import sys
import os


# Constants
CONSOLE_DRAINING_DELAY = 1


def str_to_int(string, default):
    try:
        return int(string)
    except Exception:
        return default


class JobConsoleState(IntEnum):
    CREATED = 0
    ACTIVE = 1
    DUT_DONE = 2
    TEAR_DOWN = 3
    OVER = 4


class JobConsole(Thread):
    def __init__(self, machine_id, client_endpoint,
                 client_version=None, log_level=LogLevel.INFO):
        super().__init__(name='ConsoleThread')

        self.dut_id = machine_id

        self.client_endpoint = client_endpoint
        self.console_patterns = None
        self.client_version = client_version
        self.log_level = log_level

        # Sockets
        if self.client_version:
            logger.info(f"Connecting to the client endpoint {self.client_endpoint}")
            self.client_sock = socket.create_connection((self.client_endpoint.host, self.client_endpoint.port))
        else:
            self.client_sock = None
        self.salad_sock = None

        # Job-long state
        self._state = JobConsoleState.CREATED
        self.start_time = None
        self.line_buffer = bytearray()
        self._user_session_state = dict()

        self.reset_per_boot_state()

    @property
    def machine_is_unfit_for_service(self):
        return self.console_patterns and self.console_patterns.machine_is_unfit_for_service

    @classmethod
    def salad_request(cls, dut_id):
        salad_url = f"{config.SALAD_URL}/api/v1/machine/{dut_id}"
        r = requests.get(salad_url)
        r.raise_for_status()
        return r.json()

    def connect_to_salad(self):
        parsed_url = urlsplit(config.SALAD_URL)
        machine = self.salad_request(self.dut_id)
        port = machine.get("tcp_port")

        return socket.create_connection((parsed_url.hostname, port))

    def reset_per_boot_state(self):
        self.last_activity_from_machine = None
        self.last_activity_from_client = None

        if self.console_patterns:
            self.console_patterns.reset_per_boot_state()
            self.needs_reboot = self.console_patterns.needs_reboot

    def close_salad(self):
        try:
            self.salad_sock.shutdown(socket.SHUT_RDWR)
            self.salad_sock.close()
        except OSError:
            pass

    def close_client(self):
        if self.client_version:
            try:
                self.client_sock.shutdown(socket.SHUT_RDWR)
                self.client_sock.close()
            except OSError:
                pass

    def close(self):
        self.set_state(JobConsoleState.OVER)

    @property
    def state(self):
        if self._state == JobConsoleState.ACTIVE:
            return self._state if self.is_alive() else JobConsoleState.OVER

        return self._state

    def set_state(self, state, **kwargs):
        prev_state = self._state
        if state < prev_state:
            raise ValueError("The state can only move forward")
        elif state == prev_state:
            return
        else:
            self._state = state

        self.log(f"Job console state changed from {prev_state.name} -> {state.name}\n")

        if state == JobConsoleState.ACTIVE:
            self.start_time = datetime.now()

        elif state == JobConsoleState.DUT_DONE:
            # Skip the entire tear-down if we do not have a client
            if not self.client_version:
                self.set_state(JobConsoleState.OVER)

        elif state == JobConsoleState.TEAR_DOWN:
            # Kill the connection to SALAD
            self.close_salad()

            # Notify the client
            if self.client_version:
                if self.client_version == 0:
                    self.log(f"<-- End of the session: {self.console_patterns.job_status} -->\n")
                elif self.client_version == 1:
                    try:
                        status = JobStatus.from_str(self.console_patterns.job_status)
                        SessionEndMessage.create(job_bucket=kwargs.get('job_bucket'),
                                                 status=status).send(self.client_sock)
                    except (ConnectionResetError, BrokenPipeError, OSError):
                        traceback.print_exc()
                try:
                    self.client_sock.shutdown(socket.SHUT_WR)
                except (ConnectionResetError, BrokenPipeError, OSError):
                    pass

        elif state == JobConsoleState.OVER:
            # Make sure the connections to SALAD and the client are killed
            self.close_salad()
            self.close_client()

    def start(self, console_patterns):
        self.console_patterns = console_patterns
        super().start()

    def match_console_patterns(self, buf):
        patterns_matched = set()

        # Process the buffer, line by line
        to_process = self.line_buffer + buf
        cur = 0
        while True:
            idx = to_process.find(b'\n', cur)
            if idx >= 0:
                line = to_process[cur:idx+1]
                logger.info(f"{self.dut_id} -> {bytes(line)}")
                patterns_matched |= self.console_patterns.process_line(line)
                cur = idx + 1
            else:
                break
        self.line_buffer = to_process[cur:]

        # Tell the user what happened
        if len(patterns_matched) > 0:
            self.log(f"Matched the following patterns: {', '.join(patterns_matched)}\n")

        # Check if the state changed
        self.needs_reboot = self.console_patterns.needs_reboot

    def log(self, msg, log_level=LogLevel.INFO):
        # Ignore messages with a log level lower than the minimum set
        if log_level < self.log_level:
            return

        if self.start_time is not None:
            relative_time = (datetime.now() - self.start_time).total_seconds()
        else:
            relative_time = 0.0

        log_msg = f"+{relative_time:.3f}s: {msg}"
        logger.info(log_msg.rstrip("\r\n"))

        if self.client_version:
            try:
                if self.client_version == 0:
                    self.client_sock.send(log_msg.encode())
                elif self.client_version == 1:
                    ControlMessage.create(log_msg, severity=log_level).send(self.client_sock)
            except OSError:
                pass

    def stop(self):
        self.set_state(JobConsoleState.OVER)
        self.join()

    def run(self):
        try:
            self.salad_sock = self.connect_to_salad()
            self.set_state(JobConsoleState.ACTIVE)
        except Exception:
            self.log(f"ERROR: Failed to connect to the SALAD server:\n{traceback.format_exc()}")
            self.close()

        while self.state < JobConsoleState.OVER:
            fds = []
            if self.state < JobConsoleState.TEAR_DOWN:
                fds.extend([self.salad_sock.fileno()])
            if self.client_version:
                fds.extend([self.client_sock.fileno()])

            # Make sure all the FDs are valid, or exit!
            if any([fd < 0 for fd in fds]):
                self.log("Found a negative fd, aborting!")
                self.close()

            rlist, _, _ = select.select(fds, [], [], 1.0)

            for fd in rlist:
                try:
                    if fd == self.salad_sock.fileno():
                        # DUT's stdout/err: Salad -> Client
                        buf = self.salad_sock.recv(8192)
                        if len(buf) == 0:
                            self.set_state(JobConsoleState.DUT_DONE)

                        # Match the console patterns
                        try:
                            self.match_console_patterns(buf)
                        except Exception:
                            self.log(traceback.format_exc())

                        # Update the last console activity if we already had activity,
                        # or when we get the first newline character as serial
                        # consoles may sometimes send unwanted characters at power up
                        if self.last_activity_from_machine is not None or b'\n' in buf:
                            self.last_activity_from_machine = datetime.now()

                        # Forward to the client
                        if self.client_version:
                            if self.client_version == 0:
                                self.client_sock.send(buf)
                            elif self.client_version == 1:
                                JobIOMessage.create(buf).send(self.client_sock)

                        # The message got forwarded, close the session if it ended
                        if self.console_patterns.session_has_ended:
                            self.set_state(JobConsoleState.DUT_DONE)

                    elif self.client_sock and fd == self.client_sock.fileno():
                        # DUT's stdin: Client -> Salad
                        if self.client_version == 0:
                            buf = self.client_sock.recv(8192)
                            if len(buf) == 0:
                                self.close()

                            # Forward to the salad
                            self.salad_sock.send(buf)
                        elif self.client_version == 1:
                            try:
                                msg = Message.next_message(self.client_sock)
                                if msg.msg_type == MessageType.JOB_IO:
                                    self.salad_sock.send(msg.buffer)
                            except EOFError:
                                # Do not warn when we are expecting the client to close its socket
                                if self.state < JobConsoleState.TEAR_DOWN:
                                    self.log(traceback.format_exc())

                                self.log("The client closed its connection")

                                # Clean up everything on our side
                                self.close()

                        self.last_activity_from_client = datetime.now()
                except (ConnectionResetError, BrokenPipeError, OSError):
                    self.log(traceback.format_exc())
                    self.close()
                except Exception:
                    logger.error(traceback.format_exc())


class JobBucket:
    Credentials = namedtuple('Credentials', ['username', 'password', 'policy_name'])

    def __init__(self, minio, bucket_name, initial_state_tarball_file=None,
                 hostname_by_role={}):
        self.minio = minio
        self.name = bucket_name
        self.hostname_by_role = hostname_by_role

        self._credentials = dict()

        if initial_state_tarball_file:
            self.initial_state_tarball_file = tempfile.NamedTemporaryFile("w+b")
            shutil.copyfileobj(initial_state_tarball_file, self.initial_state_tarball_file)
            self.initial_state_tarball_file.seek(0)
        else:
            self.initial_state_tarball_file = None

        # Ensure the bucket doesn't already exist
        if not self.minio.bucket_exists(bucket_name):
            self.minio.make_bucket(bucket_name)
        else:
            raise ValueError("The bucket already exists")

    def remove(self):
        if self.minio.bucket_exists(self.name):
            self.minio.remove_bucket(self.name)

        for credentials in self._credentials.values():
            self.minio.remove_user_policy(credentials.policy_name, credentials.username)
            self.minio.remove_user(credentials.username)
        self._credentials = {}

    def __del__(self):
        try:
            self.remove()
        except Exception:
            traceback.print_exc()

    def credentials(self, role):
        return self._credentials.get(role)

    def create_owner_credentials(self, role, user_name=None, password=None,
                                 groups=None, whitelisted_ips=None):
        if user_name is None:
            user_name = f"{self.name}-{role}"

        if password is None:
            password = secrets.token_hex(16)

        if groups is None:
            groups = []

        if whitelisted_ips is None:
            whitelisted_ips = []

        policy_name = f"policy_{user_name}"

        self.minio.add_user(user_name, password)

        policy_statements = [
            MinIOPolicyStatement(buckets=[self.name], source_ips=whitelisted_ips)
        ]
        if len(whitelisted_ips) > 0:
            restrict_to_whitelisted_ips = MinIOPolicyStatement(allow=False, not_source_ips=whitelisted_ips)
            policy_statements.append(restrict_to_whitelisted_ips)
        policy = json.dumps(generate_policy(policy_statements))
        logger.debug(f"Applying the MinIO policy: {policy}")

        try:
            self.minio.apply_user_policy(policy_name, user_name, policy_statements)
        except Exception as e:
            self.minio.remove_user(user_name)
            raise e from None

        # Add the user to the wanted list of groups
        for group_name in groups:
            self.minio.add_user_to_group(user_name, group_name)

        credentials = self.Credentials(user_name, password, policy_name)
        self._credentials[role] = credentials

        return credentials

    def setup(self):
        if self.initial_state_tarball_file:
            self.minio.extract_archive(self.initial_state_tarball_file, self.name)
            self.initial_state_tarball_file.close()

    def access_url(self, role=None):
        endpoint = urlparse(self.minio.url)

        role_creds = self.credentials(role)
        if role_creds:
            credentials = f"{role_creds[0]}:{role_creds[1]}@"
        else:
            credentials = ""

        hostname = self.hostname_by_role.get(role, endpoint.hostname)
        return f'{endpoint.scheme}://{credentials}{hostname}:{endpoint.port}'

    @classmethod
    def from_job_request(cls, minio, request, machine):
        # Look for the HOST header, to get the hostname used by the client to connect to
        # the executor, so that we can use the same host when telling the client how to
        # download shared folder
        hostname_by_role = {}
        for name, value in request.http_headers.items():
            if name.lower() == "host":
                if len(value) > 0:
                    hostname_by_role["client"] = value.split(":")[0]

        # Convert the job_bucket_initial_state_tarball_file_fd to a file-like object
        if request.job_bucket_initial_state_tarball_file_fd > 0:
            initial_state_tarball_file = os.fdopen(request.job_bucket_initial_state_tarball_file_fd, "rb")
        else:
            initial_state_tarball_file = None

        last_exception = None
        for i in range(5):
            # Make sure the fixed part of the bucket name isn't filling up the whole bucket name (64 chars max)
            base_bucket_name = f"job-{machine.id}-{request.job_id}"[0:56]

            # Append up to 32 characters of entropy within the bucket name limits of minio:
            # Bucket names can consist only of lowercase letters, numbers, dots (.), and hyphens (-)
            # We however do not allow dots, as the following sequence is not allowed: .., .-, and -.
            rnd = ''.join(random.choice(string.ascii_lowercase + string.digits + '-') for i in range(32))

            try:
                bucket_name = MinioClient.create_valid_bucket_name(f"{base_bucket_name}-{rnd}")

                return cls(minio, bucket_name=bucket_name,
                           initial_state_tarball_file=initial_state_tarball_file,
                           hostname_by_role=hostname_by_role)
            except ValueError as e:
                last_exception = e

        raise last_exception from None


class JobHTTPServerRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        self.server.executor.log(fmt % args)

    @property
    def artifacts(self):
        if deployment := self.server.executor.cur_deployment:
            if deployment.storage:
                return deployment.storage.http

        return []

    def get_artifact(self):
        path = self.path.split('?')[0]
        for artifact in self.artifacts:
            if path == artifact.path:
                return artifact

    def handle_request(self, headers_only=False):
        # Let's close the connection after every transaction
        self.close_connection = True

        # Restrict access to the job's artifacts to the DUT that is supposed to access them
        # While restricting access by IP isn't foolproof, it makes it harder for potential
        # attackers to figure out if they are talking to the right HTTP server. To this end,
        # we also do not use the error code 403 so as to make it less clear what is going on
        dut_ip_address = self.server.executor.db_dut.ip_address
        if self.client_address[0] != dut_ip_address:
            self.log_message("WARNING: Got an HTTP query from an unexpected IP address "
                             f"({self.client_address[0]} instead of {dut_ip_address})")
            self.send_error(404)

        if artifact := self.get_artifact():
            # TODO: Add other ways of providing the data
            data = artifact.data

            data_buf = data.encode()

            self.send_response(200)
            self.send_header("Content-Type", "text/plain;charset=UTF-8")  # TODO: Get the mime type from the job?
            self.send_header("Content-Length", f"{len(data_buf)}")
            self.end_headers()

            if not headers_only:
                self.wfile.write(data_buf)
        else:
            self.send_error(404)

    def do_GET(self):
        self.handle_request(headers_only=False)

    def do_HEAD(self):
        self.handle_request(headers_only=True)


class JobHTTPServer(ThreadingHTTPServer):
    @classmethod
    def __iface_query_param(cls, iface, param):
        # Implementation from:
        # https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                return socket.inet_ntop(socket.AF_INET,
                                        fcntl.ioctl(s.fileno(), param,
                                                    struct.pack('256s',
                                                                iface.encode('utf8'))
                                                    )[20:24])
            except OSError:
                # Iface doesn't exist, or no IP assigned
                raise ValueError(f"The interface {iface} has no IP assigned") from None

    def __init__(self, executor):
        self.executor = executor

        # Only expose the server to private interface, if set
        host = ""
        if config.PRIVATE_INTERFACE:
            try:
                host = self.__iface_query_param(config.PRIVATE_INTERFACE, 0x8915)  # SIOCGIFADDR
            except Exception:
                self.executor.log(("WARNING: Failed to get the IP address of the private interface:\n"
                                   f"{traceback.format_exc()}"))

        super().__init__((host, 0), JobHTTPServerRequestHandler)
        threading.Thread(target=self.serve_forever, name="HTTP", daemon=True).start()

    @property
    def url(self):
        host, port = self.server_address
        return f"http://{host}:{port}"


class Executor(Thread):
    def __init__(self, mars_db, db_dut, job_request):
        self.mars_db = mars_db
        self.db_dut = db_dut
        self.job_request = job_request

        self.state = DUTState.QUEUED
        self.job_console = None
        self.cur_deployment = None
        self.stop_event = Event()

        # Remote artifacts (typically over HTTPS) are stored in our
        # local minio instance which is exposed over HTTP to the
        # private LAN. This makes such artifacts amenable to PXE
        # booting, for which HTTPS clients are not available.  Less
        # critically, it makes access easier for the boards in our
        # private LAN, for which HTTPS offers no advantage.
        self.remote_url_to_local_cache_mapping = {}

    @cached_property
    def minio(self):
        return MinioClient()

    @cached_property
    def job_bucket(self):
        job_bucket = JobBucket.from_job_request(self.minio, self.job_request, self.db_dut)
        if job_bucket:
            job_bucket.create_owner_credentials("dut", groups=self.job_request.minio_groups,
                                                whitelisted_ips=[f'{self.db_dut.ip_address}/32'])
        return job_bucket

    @cached_property
    def job_httpd(self):
        return JobHTTPServer(self)

    @cached_property
    def job_config(self):
        # Bit nasty to render twice, but better than duplicating
        # template render in the various call-sites within
        # executor. Rendering it up front reduces the chances for
        # mistakes. (Meta-point: using an HTTP query to specify the
        # "target" could avoid this duplication of work, and might
        # actually make more sense)
        job = Job.render_with_resources(self.job_request.raw_job, self.db_dut, self.job_bucket,
                                        job={"http": {"url": self.job_httpd.url}})
        logger.debug("rendered job:\n%s", job)

        return job

    @cached_property
    def pdu_port(self):
        start = time.monotonic()

        config_pdu = self.mars_db.pdus.get(self.db_dut.pdu)
        if config_pdu is None:
            return None

        if pdu := PDU.create(config_pdu.driver, config_pdu.name, config_pdu.config, config_pdu.reserved_port_ids):
            for port in pdu.ports:
                if str(port.port_id) == str(self.db_dut.pdu_port_id):
                    port.min_off_time = self.db_dut.pdu_off_delay

                    exec_time = (time.monotonic() - start) * 1000
                    self.log(f"Initialized the PDU port in {exec_time:.1f} ms\n")

                    return port

            raise ValueError('Could not find a matching port for %s on %s' % (self.db_dut.pdu_port_id, pdu))

        raise ValueError("Could not create the PDU")

    def cancel_job(self):
        self.log("WARNING: The job got cancelled at the infra admin's request\n")
        self.stop_event.set()

    def log(self, msg, log_level=LogLevel.INFO):
        if not msg.endswith("\n"):
            msg += "\n"

        if self.job_console is not None:
            self.job_console.log(msg, log_level=log_level)

    def gen_job_boot_config(self, deployment):
        cache_mapping = self.remote_url_to_local_cache_mapping

        # Use the cached artifacts when possible, otherwise directly use the URL
        return BootConfig(kernel=cache_mapping.get(deployment.kernel_url, deployment.kernel_url),
                          initrd=cache_mapping.get(deployment.initramfs_url, deployment.initramfs_url),
                          dtb=cache_mapping.get(deployment.dtb_url, deployment.dtb_url),
                          cmdline=deployment.kernel_cmdline)

    def download_and_cache(self, url, output):
        attempts = 6
        tries = 0
        for i in range(attempts):
            try:
                tries += 1
                start_time = time.time()

                has_cache = config.EXECUTOR_ARTIFACT_CACHE_ROOT is not None
                if has_cache:
                    try:
                        os.makedirs(config.EXECUTOR_ARTIFACT_CACHE_ROOT, exist_ok=True)
                    except PermissionError:  # pragma: no cover
                        self.log(f"Unable to create \"{config.EXECUTOR_ARTIFACT_CACHE_ROOT}\", "
                                 "permission denied.  Disabling caching of artifacts...")
                        has_cache = False

                if has_cache:
                    session = CacheControl(requests.Session(), cache=FileCache(config.EXECUTOR_ARTIFACT_CACHE_ROOT))
                else:
                    session = requests.Session()

                resp = session.get(url)
                resp.raise_for_status()

                # Write the data to the output file
                output.seek(0, os.SEEK_SET)
                output.write(resp.content)
                output.flush()

                # Get the file size before resetting it to the beginning
                size_mb = output.tell() / 1024**2
                output.seek(0, os.SEEK_SET)

                # print some additional statistics when the fetch was with caching
                # disabled or was a cache miss
                if not has_cache or not resp.from_cache:
                    # note: don't round total_time here else it might cause a #DE when
                    # calculating avg speed
                    total_time = time.time() - start_time
                    avg_speed = size_mb / total_time
                    self.log(f"Downloaded {'and cached ' if has_cache else ''}"
                             f"the {url} in {round(total_time, 1)}s "
                             f"({round(size_mb, 2)} MB, at {round(avg_speed, 2)} MB/s)")
                else:
                    self.log(f"Fetched {url} from cache ({round(size_mb, 2)} MB)")

                return
            except Exception:
                self.log(traceback.format_exc())
                if i < attempts - 1:
                    self.log("Retrying to cache the artifact after a 10s delay\n")
                    time.sleep(10)
                else:
                    self.log("Failed too many times, aborting!\n")
                    self.job_console.set_state(JobConsoleState.OVER)

    def __fastboot_dut(self):
        def find_bootsdb_fastbootdevice():
            for path in [config.BOOTS_DB_USER_FILE, config.BOOTS_DB_FILE]:
                self.log(f"Trying to open the BootsDB {path}")
                if path and os.path.isfile(path):
                    try:
                        db = BootsDB.from_path(path, machine=self.db_dut)
                    except Exception:
                        self.log(f"WARNING: Could not parse the BOOTS DB file '{path}':\n{traceback.format_exc()}")
                        continue

                    for name, device in db.fastboot.items():
                        if device.match.matches(fbdev):
                            device.name = name
                            return device

        if self.cur_deployment:
            fbdev = FastbootDevice.from_serial(self.db_dut.id)
            if not fbdev:
                raise ValueError(f"Could not find the Fastboot device with serial {self.db_dut.id}")

            # If we found a device a matching fastboot device in boots db, enhance
            if db_fbdev := find_bootsdb_fastbootdevice():
                self.log(f"The Fastboot device matches BootsDB's {db_fbdev.name}: Applying defaults!")
                deployment = db_fbdev.defaults
                deployment.update(self.cur_deployment)
            else:
                deployment = self.cur_deployment

            # Ensure the boot configuration is valid
            cfg = self.gen_job_boot_config(deployment)
            if not cfg.kernel or not cfg.initrd or not cfg.dtb:
                self.log("ERROR: The generated boot configuration is missing a kernel, initrd, and/or an dtb")
                self.job_console.set_state(JobConsoleState.OVER)
                return cfg

            with tempfile.NamedTemporaryFile() as output:
                with tempfile.NamedTemporaryFile() as kernel:
                    with tempfile.NamedTemporaryFile() as initrd:
                        with tempfile.NamedTemporaryFile() as dtb:
                            args = [sys.executable, "-m", "valve_gfx_ci.executor.server.android.mkbootimg"]

                            if cfg.kernel:
                                self.download_and_cache(cfg.kernel, kernel)
                                args += ["--kernel", kernel.name, "--cmdline", cfg.cmdline]

                            if cfg.initrd:
                                self.download_and_cache(cfg.initrd, initrd)
                                args += ["--ramdisk", initrd.name]

                            if cfg.dtb:
                                self.download_and_cache(cfg.dtb, dtb)
                                args += ["--dtb", dtb.name]

                                # Append the DTB to the kernel image, as is expected by up to Android 9
                                # Source: https://source.android.com/docs/core/architecture/bootloader/dtb-images
                                with open(kernel.name, "ab") as f:
                                    f.write(dtb.read())
                                    f.flush()

                            if fastboot_cfg := deployment.fastboot:
                                for field, value in fastboot_cfg.fields_set.items():
                                    args += [f"--{field}", str(value)]

                            args += ["--output", output.name]

                            self.log(f"Generating a boot image using the following parameters: {args}")

                            subprocess.check_call(args, stdout=sys.stderr, stderr=sys.stderr)

                # Upload the generated boot image and run it
                self.log("Uploading the boot image")
                output.seek(0, os.SEEK_SET)
                fbdev.upload(output)

                # Booting the image
                self.log("Booting the image")
                fbdev.boot()

            return cfg
        else:
            return BootConfig()

    def boot_config_query(self, platform=None, buildarch=None, bootloader=None):
        self.log(f"The DUT queried its boot configuration as {bootloader} / {buildarch} / {platform}\n")

        if bootloader == "fastboot":
            return self.__fastboot_dut()
        elif self.cur_deployment:
            cfg = self.gen_job_boot_config(self.cur_deployment)
            cfg.fixup_missing_fields_with_defaults(platform=platform, buildarch=buildarch, bootloader=bootloader)

            if cfg.dtb and bootloader and bootloader not in ["uboot"]:
                self.log(f"WARNING: The `dtb` parameter is unsupported by {bootloader} and was thus ignored")

            return cfg

        return BootConfig()

    def _cache_remote_artifacts(self):
        def cache_it(url, cache_artifact_name):
            # If the URL is missing, don't try to cache it, we'll pick a default kernel/initrd based on the boot request
            if not url:
                self.remote_url_to_local_cache_mapping[url] = None
                return

            # Do not cache the URL if it is already found in our cache
            if url in self.remote_url_to_local_cache_mapping:
                return

            if self.minio.is_local_url(url):
                logger.debug(f"Ignore caching {url} as it is already hosted by our minio cache")
                return
            self.remote_url_to_local_cache_mapping[url] = f"{config.MINIO_URL}/boot/{cache_artifact_name}"

            self.log(f'Caching {url} into minio...\n')
            attempts = 6
            tries = 0
            for i in range(attempts):
                try:
                    tries += 1
                    self.minio.save_boot_artifact(url, f"{cache_artifact_name}", log_callback=self.log)
                    break
                except Exception:
                    self.log(traceback.format_exc())
                    if i < attempts - 1:
                        self.log("Retrying to cache the artifact after a 10s delay\n")
                        time.sleep(10)
                    else:
                        self.log("Failed too many times, aborting!\n")
                        self.job_console.set_state(JobConsoleState.OVER)
            self.log(f"Artifact fetched after {tries} attempt(s)\n")

        for url, paths in self.job_config.deployment.artifacts.items():
            for path, artifact in paths.items():
                path_str = "-".join((self.db_dut.id, ) + path)
                cache_it(url, path_str)

        if self.job_bucket:
            logger.info("Initializing the job bucket with the client's data")
            self.job_bucket.setup()

    def update_mars_fields(self, **fields):
        server_url = f"http://localhost:{config.EXECUTOR_PORT}/api/v1/dut/{self.db_dut.id}"
        r = requests.patch(server_url, json=fields)

        if r.status_code != 200:
            logger.error(f"ERROR: Failed to update the MaRS fields associated to this DUT. Reason: {r.text}")

    def run(self):
        def session_init():
            self.state = DUTState.RUNNING

            # Connect to the client's endpoint, to relay the serial console
            self.job_console = JobConsole(self.db_dut.id,
                                          client_endpoint=self.job_request.callback_endpoint,
                                          client_version=self.job_request.version)
            self.job_console.start(console_patterns=self.job_config.console_patterns)

            # Cut the power to the machine as early as possible, as we want to be
            # able to guarantee the power was off for the expected `min_off_time`,
            # and we can use some of that off time to setup the infra (download
            # kernel/initramfs, then push them to minio).
            self.pdu_port.set(PDUState.OFF)

        def session_end():
            # Ensure we cut the power to the DUT
            self.pdu_port.set(PDUState.OFF)

            self.job_console.close()
            self.job_console = None
            self.cur_deployment = None
            if self.job_bucket:
                self.job_bucket.remove()
                self.job_bucket = None

        def log_exception():
            logger.debug("Exception caught:\n%s", traceback.format_exc())
            self.log(f"An exception got caught: {traceback.format_exc()}\n", LogLevel.ERROR)
            # If exceptions start firing, throttle the parent loop, since it's
            # very heavy spam if left to run at full speed.
            time.sleep(2)

        def execute_job():
            # Start the overall timeout
            timeouts = self.job_config.timeouts
            timeouts.overall.start()

            # Download the kernel/initramfs
            self.log("Setup the infrastructure\n")
            timeouts.infra_setup.start()
            self._cache_remote_artifacts()
            self.log(f"Completed setup of the infrastructure, after {timeouts.infra_setup.active_for} s\n")
            timeouts.infra_setup.stop()

            # Keep on resuming until success, timeouts' retry limits is hit, or the entire executor is going down
            self.cur_deployment = self.job_config.deployment_start
            while (not self.stop_event.is_set() and
                   not timeouts.overall.has_expired and
                   self.job_console.state < JobConsoleState.DUT_DONE):
                self.job_console.reset_per_boot_state()

                # Make sure the machine shuts down
                self.pdu_port.set(PDUState.OFF)

                self.log(f"Power up the machine, enforcing {self.pdu_port.min_off_time} seconds of down time\n")
                self.pdu_port.set(PDUState.ON)

                # Start the boot, and enable the timeouts!
                self.log("Boot the machine\n")
                timeouts.boot_cycle.start()
                timeouts.first_console_activity.start()
                timeouts.console_activity.stop()

                # Reset all the watchdogs, since they are not supposed to remain active between rounds
                for wd in timeouts.watchdogs.values():
                    wd.cancel()

                while (self.job_console.state < JobConsoleState.DUT_DONE and
                       not self.job_console.needs_reboot and
                       not self.stop_event.is_set() and
                       not timeouts.has_expired):
                    # Update the activity timeouts, based on when was the
                    # last time we sent it data
                    if self.job_console.last_activity_from_machine is not None:
                        timeouts.first_console_activity.stop()
                        timeouts.console_activity.reset(when=self.job_console.last_activity_from_machine)

                    # Wait a little bit before checking again
                    time.sleep(0.1)

                # Cut the power
                self.pdu_port.set(PDUState.OFF)

                # Increase the retry count of the timeouts that expired, and
                # abort the job if we exceeded their limits.
                abort = False
                for timeout in timeouts.expired_list:
                    retry = timeout.retry()
                    decision = "Try again!" if retry else "Abort!"
                    self.log(f"Hit the timeout {timeout} --> {decision}\n", LogLevel.ERROR)
                    abort = abort or not retry

                # Check if the DUT asked us to reboot
                if self.job_console.needs_reboot:
                    retry = timeouts.boot_cycle.retry()
                    retries_str = f"{timeouts.boot_cycle.retried}/{timeouts.boot_cycle.retries}"
                    dec = f"Boot cycle {retries_str}, go ahead!" if retry else "Exceeded boot loop count, aborting!"
                    self.log(f"The DUT asked us to reboot: {dec}\n", LogLevel.WARN)
                    abort = abort or not retry

                if abort:
                    # We have reached a timeout retry limit, time to stop!
                    self.job_console.set_state(JobConsoleState.DUT_DONE)
                else:
                    # Stop all the timeouts, except the overall
                    timeouts.first_console_activity.stop()
                    timeouts.console_activity.stop()
                    timeouts.boot_cycle.stop()

                    # We went through one boot cycle, use the "continue" deployment
                    self.cur_deployment = self.job_config.deployment_continue

            # We either reached the end of the job, or the client got disconnected
            if self.job_console.state == JobConsoleState.DUT_DONE:
                # Mark the machine as unfit for service
                if self.job_console.machine_is_unfit_for_service:
                    self.log("The machine has been marked as unfit for service\n")
                    self.update_mars_fields(ready_for_service=False)

                # Tearing down the job
                self.log("The job has finished executing, starting tearing down\n")
                timeouts.infra_teardown.start()

                # Delay to make sure messages are read before the end of the job
                time.sleep(CONSOLE_DRAINING_DELAY)

                # Start the tear down, which will create and send the credentials
                # for the job bucket to the client
                self.log("Creating credentials to the job bucket for the client\n")
                self.job_console.set_state(JobConsoleState.TEAR_DOWN, job_bucket=self.job_bucket)

                # Wait for the client to close the connection
                self.log("Waiting for the client to download the job bucket\n")
                while (self.job_console.state < JobConsoleState.OVER and
                       not self.stop_event.is_set() and
                       not timeouts.infra_teardown.has_expired):
                    # Wait a little bit before checking again
                    time.sleep(0.1)

                self.log(f"Completed the tear down procedure in {timeouts.infra_teardown.active_for} s\n")
                timeouts.infra_teardown.stop()
            else:
                self.log("The job is over, skipping sharing the job bucket with the client")

            # We are done!

        try:
            session_init()
            self.log(f"Starting the job: {self.job_config}\n\n", LogLevel.DEBUG)
            execute_job()
        except Exception:
            log_exception()
        finally:
            session_end()

    @property
    def job_status(self):
        if self.job_console is not None:
            return self.job_console.console_patterns.job_status
        else:
            return JobStatus.UNKNOWN


app = flask.Flask(__name__)


def get_executor(raise_if_missing=True):
    with app.app_context():
        if executor := flask.current_app.executor:
            return executor
        elif raise_if_missing:
            raise ValueError("The executor has not started yet")


@app.errorhandler(ValueError)
def handle_valueError_exception(error):
    traceback.print_exc()
    response = flask.jsonify({"error": str(error)})
    response.status_code = 400
    return response


@app.route('/api/v1/state', methods=['GET'])
def get_state():
    if executor := get_executor(raise_if_missing=False):
        return {
            "state": executor.state.name
        }
    else:
        return {
            "state": DUTState.QUEUED.name
        }


@app.route('/api/v1/boot/config', methods=['GET'])
def get_boot_config():
    args = flask.request.args

    executor = get_executor()
    if boot_cfg := executor.boot_config_query(platform=args.get("platform"),
                                              buildarch=args.get("buildarch"),
                                              bootloader=args.get("bootloader")):
        return asdict(boot_cfg)


@app.route('/api/v1/job/cancel', methods=['POST'])
def cancel_job():
    executor = get_executor()
    executor.cancel_job()
    return flask.make_response("The job was marked for cancellation\n", 200)


@dataclass
class JobConfig:
    executor_job_version: int

    mars_db: MarsDB
    machine_id: str

    job_request: JobRequest

    pdu_port_stats: PduPortStats

    @field_validator("executor_job_version")
    @classmethod
    def executor_job_version_is_known(cls, v):
        assert v == 1
        return v


def run(config_f, socket_path, lock_path):
    def parse_config(config_f):
        cfg = yaml.safe_load(config_f)
        return JobConfig(**cfg)

    try:
        # Create an exclusive lock
        os.makedirs(os.path.dirname(f"{socket_path}"), exist_ok=True)
        os.makedirs(os.path.dirname(f"{lock_path}"), exist_ok=True)
        socket_lock = open(lock_path, "w")
        lock_fd(socket_lock.fileno())
        socket_lock.write(f"{os.getpid()}\n")
        socket_lock.flush()

        # Parse the configuration
        cfg = parse_config(config_f)
        db_dut = cfg.mars_db.duts.get(cfg.machine_id)
        if db_dut is None:
            raise ValueError(f"The machine id '{cfg.machine_id}' can't be found in mars_db")

        # HACK: We should really find a way to get this set directly by pydantic!
        db_dut.id = cfg.machine_id

        # Create the executor
        executor = Executor(mars_db=cfg.mars_db, db_dut=db_dut, job_request=cfg.job_request)

        # Copy the pdu port stats
        for f in fields(cfg.pdu_port_stats):
            setattr(executor.pdu_port, f.name, getattr(cfg.pdu_port_stats, f.name))

        # Update the configuration
        with app.app_context():
            flask.current_app.executor = executor
            flask.current_app.db_dut = db_dut

        # Disable Flask's access logging
        logging.getLogger('werkzeug').setLevel(logging.ERROR)

        # Start Flask
        flask_thread = threading.Thread(target=app.run, daemon=True,
                                        kwargs={"host": f"unix://{socket_path}",
                                                "port": None, "debug": True, "use_reloader": False})
        flask_thread.start()

        # Start the job
        executor.run()

        # Exit using the same status code as the job
        os._exit(executor.job_status.value)
    except Exception:
        # We caught an exception when we really shouldn't have, let's print it,
        # flush our streams, then die with the status code INCOMPLETE
        traceback.print_exc(file=sys.stderr)
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(JobStatus.INCOMPLETE.value)
