#!/usr/bin/env python3

from datetime import datetime

import multiprocessing
import traceback
import signal
import socket
import flask
import json
import time
import sys

from waitress import serve

from .dut import DUT, JobRequest, DUTState, SergentHartman, SergentHartmanState, InvalidTarballFile
from .executor import JobConsole
from .mars import Mars
from .minioclient import MinioClient
from .boots import BootService
from .message import JobStatus
from .pdu import PDUPort, PDUState
from .pdu.daemon import PDUDaemon, AsyncPDU
from .socketactivation import get_sockets_by_name
from . import config


class CustomJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, JobStatus):
            return obj.name
        elif isinstance(obj, SergentHartmanState):
            return obj.name
        elif isinstance(obj, SergentHartman):
            return {
                "state": obj.state,
                "is_active": obj.is_active,
                "is_registered": obj.is_machine_registered,
                "boot_loop_counts": obj.boot_loop_counts,
                "qualifying_rate": obj.qualifying_rate,
                "current_loop_count": obj.cur_loop,
                "statuses": dict([(s.name, val) for s, val in obj.statuses.items()]),
            }
        elif isinstance(obj, DUTState):
            return obj.name
        elif isinstance(obj, DUT):
            dut = {
                "id": obj.id,
                "state": obj.state,
                "ready_for_service": obj.ready_for_service,
                "has_pdu_assigned": obj.pdu_port is not None,
                "local_tty_device": obj.local_tty_device,
                "tags": list(obj.tags),
                "manual_tags": list(obj.manual_tags),
                "base_name": obj.base_name,
                "full_name": obj.full_name,
                "mac_address": obj.mac_address,
                "ip_address": obj.ip_address,
                "is_retired": obj.is_retired,
                "training": obj.sergent_hartman,
                "pdu": {
                    "name": obj.pdu,
                    "port_id": obj.pdu_port_id
                },
                "pdu_off_delay": obj.pdu_off_delay,
                "comment": obj.comment
            }

            if salad := JobConsole.salad_request(obj.id):
                dut["logs_endpoint"] = {
                    "host": "ci-gateway",
                    "port": salad["tcp_port_logs"],
                }
            return dut
        elif isinstance(obj, AsyncPDU):
            return {
                "ports": {p.port_id: p for p in obj.ports},
                "state": obj.state.name,
                "error": obj.error,

            }
        elif isinstance(obj, PDUPort):
            return {
                "label": obj.label,
                "min_off_time": obj.min_off_time,
                "state": obj.last_known_state.name,
                "last_shutdown": obj.last_shutdown,
                "last_polled": obj.last_polled,
                "reserved": obj.reserved
            }

        return super().default(obj)


class CustomJSONProvider(flask.json.provider.JSONProvider):
    def dumps(self, obj, *args, **kwargs):
        return json.dumps(obj, cls=CustomJSONEncoder, *args, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s)


def find_pdu(pdu_name):
    with app.app_context():
        mars = flask.current_app.mars
    return mars.get_pdu_by_name(pdu_name, raise_if_missing=True)


def find_pdu_port(pdu_name, port_id):
    with app.app_context():
        mars = flask.current_app.mars
    return mars.get_pdu_port_by_name(pdu_name, port_id, raise_if_missing=True)


app = flask.Flask(__name__)
app.json = CustomJSONProvider(app)


@app.errorhandler(ValueError)
def handle_valueError_exception(error):
    traceback.print_exc()
    response = flask.jsonify({"error": str(error)})
    response.status_code = 400
    return response


@app.route('/api/v1/duts', methods=['GET'])
@app.route('/api/v1/machines', methods=['GET'])   # Deprecated
def get_machine_list():
    with app.app_context():
        mars = flask.current_app.mars

    return {
        "duts": dict([(m.id, m) for m in mars.known_machines])
    }


@app.route('/api/v1/dut/', methods=['POST', 'PUT'])
@app.route('/api/v1/machine/', methods=['POST', 'PUT'])   # Deprecated
def machine_add_or_update():
    with app.app_context():
        mars = flask.current_app.mars

    data = flask.request.json

    for key in data:
        if key not in {"id", "base_name", "tags", "manual_tags", "mac_address",
                       "ip_address", "local_tty_device", "ready_for_service",
                       "is_retired"}:
            raise ValueError(f"The field {key} cannot be set/modified")

    # Be backwards compatible with the older machine registration container that
    # did not specify the machine ID
    if 'id' not in data and data.get('mac_address'):
        data['id'] = data['mac_address']

    machine = mars.machine_discovered(data, update_if_already_exists=True)
    return CustomJSONEncoder().default(machine)


@app.route('/api/v1/dut/<machine_id>/', methods=['GET'])
@app.route('/api/v1/dut/<machine_id>', methods=['GET'])
@app.route('/api/v1/machine/<machine_id>/', methods=['GET'])   # Deprecated
@app.route('/api/v1/machine/<machine_id>', methods=['GET'])   # Deprecated
def machine_detail_get(machine_id):
    with app.app_context():
        mars = flask.current_app.mars

    machine = mars.get_machine_by_id(machine_id, raise_if_missing=True)
    return CustomJSONEncoder().default(machine)


@app.route('/api/v1/dut/<machine_id>/quick_check', methods=['GET', 'POST'])
@app.route('/api/v1/machine/<machine_id>/quick_check', methods=['GET', 'POST'])   # Deprecated
def machine_quick_check(machine_id):
    with app.app_context():
        mars = flask.current_app.mars

    machine = mars.get_machine_by_id(machine_id, raise_if_missing=True)

    if flask.request.method in ['GET']:
        ret = "true\n" if machine.quick_check_queued.is_set() else "false\n"
        return flask.make_response(ret, 200)
    elif flask.request.method in ['POST']:
        machine.quick_check_queued.set()
        return flask.make_response(f"Quick check queued for machine {machine.full_name}\n", 200)


@app.route('/api/v1/dut/<machine_id>', methods=['DELETE'])
@app.route('/api/v1/machine/<machine_id>', methods=['DELETE'])   # Deprecated
def machine_remove(machine_id):
    with app.app_context():
        mars = flask.current_app.mars

    machine = mars.get_machine_by_id(machine_id, raise_if_missing=True)

    if mars.remove_machine(machine_id):
        return flask.make_response(f"The machine {machine.full_name} was removed\n", 200)
    else:
        return flask.make_response(f"The machine {machine.full_name} does not exist\n", 404)


@app.route('/api/v1/dut/<machine_id>', methods=['PATCH'])
@app.route('/api/v1/machine/<machine_id>', methods=['PATCH'])   # Deprecated
def machine_update(machine_id):
    data = flask.request.get_json()

    for key in data:
        if key not in {"pdu_off_delay", "comment", "ready_for_service", "is_retired", "manual_tags"}:
            raise ValueError(f"The field {key} is invalid")

    with app.app_context():
        mars = flask.current_app.mars

    machine = mars.get_machine_by_id(machine_id, raise_if_missing=True)

    if pdu_off_delay := data.get("pdu_off_delay"):
        try:
            data["pdu_off_delay"] = float(pdu_off_delay)
        except ValueError:
            raise ValueError("Please provide the delay using a float or integer")

    machine.update_fields(data)
    return flask.make_response(f"Updated {machine.full_name}: {data}\n", 200)


@app.route('/boot/<machine_id>/boot.ipxe', methods=['GET'])
def machine_ipxe_boot_script(machine_id):
    with app.app_context():
        mars = flask.current_app.mars
        boots = flask.current_app.boots

    machine = mars.get_machine_by_id(machine_id)
    args = flask.request.args
    return boots.ipxe_boot_script(machine, platform=args.get("platform"), buildarch=args.get("buildarch"))


@app.route('/api/v1/pdus', methods=['GET'])
def get_pdus_list():
    pdus = {}

    with app.app_context():
        mars = flask.current_app.mars

    with mars.db as mars_db:
        for name in mars_db.pdus:
            pdus[name] = mars.get_pdu_by_name(name)

    return {
        "pdus": pdus
    }


@app.route('/api/v1/pdu/<pdu_name>', methods=['GET'])
def get_pdu(pdu_name):
    pdu = find_pdu(pdu_name)
    return flask.jsonify(pdu)


@app.route('/api/v1/pdu/<pdu_name>/port/<port_id>', methods=['GET', 'PATCH'])
def get_pdu_port(pdu_name, port_id):

    if flask.request.method in ['GET']:
        port = find_pdu_port(pdu_name, port_id)
        return flask.jsonify(port)

    elif flask.request.method in ['PATCH']:
        pdu_port = find_pdu_port(pdu_name, port_id)
        pdu = find_pdu(pdu_name)

        data = flask.request.get_json()

        for key in data:
            if key not in {"state", "reserved"}:
                raise ValueError(f"The field {key} is invalid")

        if (pdu_port.reserved and "reserved" not in data):
            raise ValueError(f'The port {port_id} on PDU "{pdu_name}" is reserved!')

        with app.app_context():
            mars = flask.current_app.mars
        with mars.db as mars_db:
            for machine in mars_db.duts.values():
                # port_id is a string but user could enter an integer and we can make it work
                if machine.pdu == pdu_name and str(machine.pdu_port_id) == str(port_id):
                    # If the machine is retired, it's OK to change the state
                    if (machine.is_retired and "state" in data):
                        break
                    raise ValueError(f'It\'s not possible to modify port {port_id} on PDU "{pdu_name}", '
                                     f'because it\'s already in use by machine {machine.full_name}.')

            if state := data.get("state"):
                if state.upper() in ["ON", "OFF"]:
                    new_state = PDUState[state.upper()]
                    pdu_port.set(new_state)
                    return flask.make_response(f'Turning {state} port {port_id} on PDU "{pdu_name}"\n', 200)
                else:
                    raise ValueError("Invalid state set, valid states are ON and OFF.")

            if state := data.get("reserved"):
                if state in ["false", "False"]:
                    pdu.unreserve_port(port_id)
                    return flask.make_response(f'Un-reserved port {port_id} on PDU "{pdu_name}"\n', 200)
                elif state in ["False", "True"]:
                    pdu.reserve_port(port_id)
                    return flask.make_response(f'Reserved port {port_id} on PDU "{pdu_name}"\n', 200)
                else:
                    raise ValueError("Invalid value to reserve a port, valid states are True and False.")


# When the request is made with a POST including a PDU and a port_id,
# it'll start a discovery process powering and updating the mars.discover_data
# with this information
# For request with a GET, it'll give the information in mars.discover_data
# so the user can see if there is a discovery process ongoing and since when.
# Finally if the method used is DELETE, discover_data will be deleted
@app.route('/api/v1/dut/discover', methods=['POST', 'GET', 'DELETE'])
@app.route('/api/v1/machine/discover', methods=['POST', 'GET', 'DELETE'])   # Deprecated
def discover_machine():
    with app.app_context():
        mars = flask.current_app.mars

    # show if there is a discovery in progress
    if flask.request.method in ['GET']:
        return flask.jsonify(mars.discover_data)

    # discover_data will be erased
    if flask.request.method in ['DELETE']:
        with mars.db as mars_db:
            if mars.discover_data:
                dd_pdu = mars.discover_data.get('pdu')
                dd_port_id = mars.discover_data.get('port_id')
                pdu_port = find_pdu_port(dd_pdu, dd_port_id)
                mars.discover_data = {}

                if pdu_port.reserved:
                    raise ValueError(f'Port {dd_port_id} on PDU "{dd_pdu}" is reserved!')

                # Be 100% sure we're not stopping any device!
                for machine in mars_db.duts.values():
                    # dd_port_id is a string but user could enter an integer and we can make it work
                    if machine.pdu == dd_pdu and str(machine.pdu_port_id) == str(dd_port_id):
                        raise ValueError(f'Port {dd_port_id} on PDU "{dd_pdu}" is already assigned.')

                pdu_port.set(PDUState.OFF)

                return flask.make_response("Discovery process canceled and port turned OFF.", 200)
            else:
                raise ValueError("There are no discovery processes in progress.")

    # The following code is only run when method is POST
    if mars.discover_data:
        raise ValueError("There is a discovery process running already.")

    data = flask.request.get_json()

    for key in data:
        if key not in {"pdu", "port_id", "timeout"}:
            raise ValueError(f"The field {key} is invalid")

    if not all(['port_id' in data, 'pdu' in data]):
        raise ValueError("You're missing at least one of the two required fields: pdu and port_id")

    dd_pdu = data.get('pdu')
    dd_port_id = data.get('port_id')

    with mars.db as mars_db:
        pdu_port = find_pdu_port(dd_pdu, dd_port_id)

        for machine in mars_db.duts.values():
            # port_id is a string but user could enter an integer and we can make it work
            if machine.pdu == dd_pdu and str(machine.pdu_port_id) == str(dd_port_id):
                raise ValueError(f'Port {dd_port_id} on PDU "{dd_pdu}" is already assigned.')

    if pdu_port.state == PDUState.ON:
        raise ValueError(f'Port {dd_port_id} on PDU "{dd_pdu} is already in use!')

    if pdu_port.reserved:
        raise ValueError(f'Port {dd_port_id} on PDU "{dd_pdu} is reserved!')

    # Launch discovery... the machine behind the PDU port should start
    pdu_port.set(PDUState.ON)

    if pdu_port.state == PDUState.ON:
        if data.get('timeout'):
            sec = int(data.get('timeout'))
        else:
            sec = 150

        mars.discover_data = {
            "pdu": dd_pdu,
            "port_id": dd_port_id,
            "date": datetime.now(),
            "timeout": int(sec),
            "started_at": time.monotonic(),
        }

        return flask.make_response(f'Booting machine behind port {dd_port_id} on PDU "{dd_pdu}".'
                                   f'Discovery will time out after {sec} seconds.\n', 200)
    else:
        raise ValueError(f'Failed to turn ON the port {dd_port_id} on PDU "{dd_pdu}"')


@app.route('/api/v1/dut/<machine_id>/cancel_job', methods=['POST'])
@app.route('/api/v1/machine/<machine_id>/cancel_job', methods=['POST'])   # Deprecated
def cancel_job_machine(machine_id):

    with app.app_context():
        mars = flask.current_app.mars

    m = mars.get_machine_by_id(machine_id, raise_if_missing=True)

    if m.state != DUTState.RUNNING:
        raise ValueError(f"Machine {m.full_name} isn't running a job. "
                         f"Current state is {m.state.name}")
    else:
        m.cancel_job()
        return flask.make_response(f"Canceling current job in machine {m.full_name}\n", 200)


@app.route('/api/v1/full-state', methods=['GET'])
def full_state():
    fs = {}

    with app.app_context():
        mars = flask.current_app.mars

    # Collect from the MarsDB all the information we need to generate the full state, then free the lock
    with mars.db as mars_db:
        fs['pdus'] = {p: mars.get_pdu_by_name(p) for p in mars_db.pdus}
        fs['duts'] = {m.id: m for m in mars.known_machines}
        fs['discover'] = mars.discover_data

    # Add a a field to show what is the current time on the server
    fs['now'] = datetime.now()

    return flask.jsonify(fs)


@app.route('/api/v1/jobs', methods=['POST'])
def post_job():
    def find_suitable_machine(target):
        with app.app_context():
            mars = flask.current_app.mars

        wanted_tags = set(target.tags)

        # If the target id is specified, check the tags
        if target.id is not None:
            machine = mars.get_machine_by_id(target.id)
            if machine is None:
                return None, 404, f"Unknown machine with ID {target.id}"
            elif not wanted_tags.issubset(machine.all_tags):
                return None, 406, (f"The machine {target.id} does not matching tags "
                                   f"(asked: {wanted_tags}, actual: {machine.all_tags})")
            elif machine.state != DUTState.IDLE:
                return None, 409, (f"The machine {target.id} is unavailable: "
                                   f"Current state is {machine.state.name}")
            elif machine.is_retired:
                return None, 409, (f"The machine {target.id} is retired.")
            return machine, 200, None
        else:
            found_a_candidate_machine = False
            for machine in mars.known_machines:
                if not wanted_tags.issubset(machine.all_tags):
                    continue
                if machine.is_retired:
                    continue

                found_a_candidate_machine = True
                if machine.state == DUTState.IDLE:
                    return machine, 200, "success"

            if found_a_candidate_machine:
                return None, 409, f"All machines matching the tags {wanted_tags} are busy"
            else:
                return None, 406, f"No active machines found matching the tags {wanted_tags}."

    def check_minio_credentials(job_request):
        credentials = job_request.minio_credentials

        # If no groups are requested, then exit directly
        if job_request.minio_groups is None or len(job_request.minio_groups) == 0:
            return True, ""

        # Some groups are requested, make sure some credentials have been set
        if credentials is None:
            return False, "Requested access to some groups, but the credentials are missing"

        # Make sure all the requested groups are in the list of groups the
        # provided-credentials have access to
        try:
            timestamp = int(datetime.now().timestamp())
            client = MinioClient(user=credentials.access_key,
                                 secret_key=credentials.secret_key,
                                 alias=f"a_{job_request.job_id}-{timestamp}")

            user_groups = set(client.groups_user_is_in())
            for group in job_request.minio_groups:
                if group not in user_groups:
                    return False, (f"The provided MinIO credentials do not belong to the group {group}")

            return True, ""
        except ValueError as e:
            return False, str(e)
        finally:
            try:
                client.remove_alias()
            except UnboundLocalError:
                pass

    # Grab the post_job lock, to prevent allocating two jobs for the same machine
    with app.app_context():
        with flask.current_app.post_job_lock:
            try:
                parsed = JobRequest.parse(flask.request)
            except InvalidTarballFile:
                return flask.make_response("Invalid tarball file", 420)

            try:
                ok, error_msg = check_minio_credentials(parsed)
                if ok:
                    machine, error_code, error_msg = find_suitable_machine(parsed.target)
                    if machine is not None:
                        if machine.state != DUTState.IDLE:
                            raise ValueError(f"The machine isn't idle: Current state is {machine.state.name}")

                        try:
                            machine.start_job(parsed)
                        except Exception as e:
                            error_code = 500
                            error_msg = str(e)
                else:
                    error_code = 403

                if parsed.version == 0:
                    response = {
                        "reason": error_msg
                    }
                elif parsed.version == 1:
                    response = {
                        # protocol version
                        "version": 1,
                        "error_msg": error_msg

                        # TODO: Store the job in memory, and show the ID here
                    }
                return flask.make_response(flask.jsonify(response), error_code)
            finally:
                # Make sure not to leak any ressource
                parsed.cleanup()


def sigterm_handler(_signo, _stack_frame):
    # Raises SystemExit(0):
    sys.exit(0)


def run():  # pragma: nocover
    # Make sure the farm name has been set
    if config.FARM_NAME is None:
        raise ValueError("Please set the FARM_NAME environment variable")

    # Check the Minio credentials: This will set up an alias, which fails if
    # the credentials are invalid and a ValueError will be raised, thus exiting
    # the process.
    MinioClient()

    pdu_daemon = PDUDaemon()

    # Create all the workers based on the machines found in MaRS
    mars = Mars(pdu_daemon)
    mars.start()

    # Start the network boot service
    # FIXME: Tidy this stuff up! Just give a boots root and descend from there.
    boots = BootService(mars=mars, config_paths={
        'TFTP_DIR': config.BOOTS_TFTP_ROOT,
    })

    # Start flask
    try:
        signal.signal(signal.SIGTERM, sigterm_handler)

        with app.app_context():
            flask.current_app.mars = mars
            flask.current_app.boots = boots
            flask.current_app.post_job_lock = multiprocessing.Lock()

        common_flags = {
            'asyncore_use_poll': True,
        }

        if http_sockets := get_sockets_by_name(config.EXECUTOR_HTTP_IPv4_SOCKET_NAME,
                                               socket.AF_INET, socket.SOCK_STREAM):
            serve(app, sockets=http_sockets, **common_flags)
        else:
            serve(app, host=config.EXECUTOR_HOST, port=config.EXECUTOR_PORT, **common_flags)
    finally:
        # Shutdown
        mars.stop(wait=True)
        pdu_daemon.stop()


if __name__ == '__main__':  # pragma: nocover
    run()
