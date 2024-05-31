from datetime import datetime, timedelta
from freezegun import freeze_time
from unittest import mock
from unittest.mock import patch, MagicMock
import os

import pytest
from pydantic import ValidationError

import server
from server.job import Target, Timeout, Timeouts, ConsoleState, Job, Pattern, CollectionOfLists
from server.job import Watchdog, KernelDeployment, DeploymentState, FastbootDeployment
import server.config as config

# Target


def test_Target_from_job__no_id_nor_tags():
    with pytest.raises(ValueError) as exc:
        Target()

    msg = "The target is neither identified by tags or id. Use empty tags to mean 'any machines'."
    assert msg in str(exc.value)


def test_Target_from_job__id_only():
    target_job = {
        "id": "MyID",
    }

    target = Target(**target_job)
    assert target.id == target_job['id']
    assert target.tags == []
    assert str(target) == f"<Target: id={target.id}, tags={target.tags}>"


def test_Target_from_job__tags_only():
    target_job = {
        "tags": ['tag 1', 'tag 2']
    }

    target = Target(**target_job)
    assert target.id is None
    assert target.tags == target_job['tags']
    assert str(target) == f"<Target: id={target.id}, tags={target.tags}>"


def test_Target_from_job__both_id_and_tags():
    target_job = {
        "id": "MyID",
        "tags": ['tag 1', 'tag 2']
    }

    target = Target(**target_job)
    assert target.id == target_job['id']
    assert target.tags == target_job['tags']
    assert str(target) == f"<Target: id={target.id}, tags={target.tags}>"


# Timeout


def test_Timeout__expiration_test():
    start_time = datetime(2021, 1, 1, 12, 0, 0)
    with freeze_time(start_time.isoformat()):
        timeout = Timeout(minutes=1, retries=0)
        assert timeout.started_at is None
        assert not timeout.is_started
        assert timeout.active_for is None

        # Start the timeout and check the state
        timeout.start()
        assert timeout.started_at == start_time
        assert timeout.is_started
        assert timeout.active_for == timedelta()
        assert not timeout.has_expired

        # Go right to the limit of the timeout
        delta = timedelta(seconds=60)
        with freeze_time((start_time + delta).isoformat()):
            assert timeout.started_at == start_time
            assert timeout.active_for == delta
            assert timeout.is_started
            assert not timeout.has_expired

        # And check that an extra millisecond trip it
        delta = timedelta(seconds=60, milliseconds=1)
        with freeze_time((start_time + delta).isoformat()):
            assert timeout.started_at == start_time
            assert timeout.active_for == delta
            assert timeout.is_started
            assert timeout.has_expired

        # Stop the timeout and check the state
        timeout.stop()
        assert timeout.started_at is None
        assert not timeout.is_started
        assert timeout.active_for is None


def test_Timeout__retry_lifecycle():
    timeout = Timeout(seconds=42, retries=1)

    # Check the default state
    assert timeout.started_at is None
    assert timeout.active_for is None
    assert timeout.retried == 0

    # Start the timeout
    start_time = datetime(2021, 1, 1, 12, 0, 0)
    with freeze_time(start_time.isoformat()):
        timeout.start()
        assert timeout.started_at == start_time
        assert timeout.retried == 0
        assert timeout.active_for == timedelta()
        assert not timeout.has_expired

    # Check that the default reset sets started_at to now()
    start_time = datetime(2021, 1, 1, 12, 0, 1)
    with freeze_time(start_time.isoformat()):
        timeout.reset()
        assert timeout.started_at == start_time

        # Check that a resetting to a certain time does as it should
        new_start = start_time - timedelta(seconds=1)
        timeout.reset(new_start)
        assert timeout.started_at == new_start

    # Do the first retry
    assert timeout.retry()
    assert timeout.started_at is None
    assert timeout.retried == 1

    # Second retry should fail
    assert not timeout.retry()


def test_Timeout_from_job():
    fields = {"days": 5, "hours": 6, "minutes": 7, "seconds": 8, "milliseconds": 9}

    delay = timedelta(**fields)
    timeout = Timeout(retries=42, **fields)
    timeout.name = "Yeeepeee"

    assert timeout.timeout == delay
    assert timeout.retries == 42
    assert str(timeout) == f"<Timeout Yeeepeee: value={delay}, retries=0/42>"


# Timeouts


def test_Timeouts__overall_with_retries():
    for t_type in ["overall", "infra_teardown"]:
        with pytest.raises(ValueError) as exc:
            Timeouts(**{t_type: Timeout(retries=1)})
        assert "Neither the overall nor the teardown timeout can have retries" in str(exc.value)


def test_Timeouts__default():
    timeouts = Timeouts()

    for timeout in timeouts:
        if timeout.name not in ["overall", "infra_teardown"]:
            assert timeout.timeout == timedelta.max
            assert timeout.retries == 0

    assert timeouts.expired_list == []
    assert not timeouts.has_expired
    assert timeouts.watchdogs == {}


def test_Timeouts__expired():
    overall = Timeout(days=1, retries=0)
    boot_cycle = Timeout(seconds=0, retries=0)
    wd1 = Timeout(seconds=0, retries=0)

    overall.start()
    boot_cycle.start()

    timeouts = Timeouts(overall=overall, boot_cycle=boot_cycle, watchdogs={"wd1": wd1})
    assert timeouts.has_expired
    assert timeouts.expired_list == [boot_cycle]

    boot_cycle.stop()
    assert not timeouts.has_expired
    assert timeouts.expired_list == []

    wd1.start()
    assert timeouts.has_expired
    assert timeouts.expired_list == [wd1]


def test_Timeouts__from_job():
    job_timeouts = {
        "first_console_activity": {
            "seconds": 45
        },
        "console_activity": {
            "seconds": 13
        },
        "watchdogs": {
            "custom1": {
                "seconds": 42
            }
        }
    }

    timeouts = Timeouts(**job_timeouts)

    assert timeouts.first_console_activity.timeout == timedelta(seconds=45)
    assert timeouts.console_activity.timeout == timedelta(seconds=13)
    assert timeouts.watchdogs.get("custom1").timeout == timedelta(seconds=42)
    assert timeouts.watchdogs["custom1"] in timeouts


# Pattern


def test_Pattern_from_job__invalid_regex():
    with pytest.raises(ValueError) as excinfo:
        Pattern(**{"regex": "BOOM\\"})

    error_msg = "Console pattern 'BOOM\\' is not a valid regular expression: bad escape (end of pattern)"
    assert error_msg in str(excinfo.value)


# Watchdogs


def test_Watchdog__process_line():
    wd = Watchdog(**{
        "start": {"regex": "start"},
        "reset": {"regex": "reset"},
        "stop": {"regex": "stop"},
    })

    # Check that nothing explodes if we have no timeouts set
    assert wd.process_line(b"line") == {}

    # Set the timeout
    wd.set_timeout(MagicMock(is_started=False))
    wd.timeout.start.assert_not_called()
    wd.timeout.reset.assert_not_called()
    wd.timeout.stop.assert_not_called()

    # Check that sending the reset/stop patterns before starting does nothing
    assert wd.process_line(b"line reset line") == {}
    assert wd.process_line(b"line stop line") == {}
    wd.timeout.start.assert_not_called()
    wd.timeout.reset.assert_not_called()
    wd.timeout.stop.assert_not_called()

    # Check that the start pattern starts the timeout
    assert wd.process_line(b"line start line") == {"start"}
    wd.timeout.start.assert_called_once()
    wd.timeout.reset.assert_not_called()
    wd.timeout.stop.assert_not_called()

    # Emulate the behaviour of the timeout
    wd.timeout.is_started = True

    # Check that the start pattern does not restart the timeout
    assert wd.process_line(b"line start line") == {}
    wd.timeout.start.assert_called_once()
    wd.timeout.reset.assert_not_called()
    wd.timeout.stop.assert_not_called()

    # Check that the reset pattern works
    assert wd.process_line(b"line reset line") == {"reset"}
    wd.timeout.start.assert_called_once()
    wd.timeout.reset.assert_called_once()
    wd.timeout.stop.assert_not_called()

    # Check that the stop pattern works
    assert wd.process_line(b"line stop line") == {"stop"}
    wd.timeout.start.assert_called_once()
    wd.timeout.reset.assert_called_once()
    wd.timeout.stop.assert_called_once()


def test_Watchdog__stop():
    wd = Watchdog(**{
        "start": {"regex": "start"},
        "reset": {"regex": "reset"},
        "stop": {"regex": "stop"},
    })

    # Check that nothing explodes if we have no timeouts set
    wd.cancel()

    # Set the timeout
    wd.set_timeout(MagicMock(is_started=False))
    wd.timeout.stop.assert_not_called()

    # Check that sending the reset/stop patterns before starting does nothing
    wd.cancel()
    wd.timeout.stop.assert_called_once()


# ConsoleState


def test_ConsoleState__missing_session_end():
    with pytest.raises(ValidationError):
        ConsoleState(session_end=None, session_reboot=None, job_success=None, job_warn=None,
                     machine_unfit_for_service=None)


def test_ConsoleState__simple_lifecycle():
    state = ConsoleState(session_end=Pattern("session_end"), session_reboot=None, job_success=None, job_warn=None,
                         machine_unfit_for_service=None)

    assert state.job_status == "INCOMPLETE"
    assert not state.session_has_ended
    assert not state.needs_reboot

    state.process_line(b"oh oh oh")
    assert state.job_status == "INCOMPLETE"
    assert not state.session_has_ended
    assert not state.needs_reboot

    state.process_line(b"blabla session_end blaba\n")
    assert state.job_status == "COMPLETE"
    assert state.session_has_ended
    assert not state.needs_reboot


def test_ConsoleState__lifecycle_with_extended_support():
    state = ConsoleState(session_end=Pattern("session_end"), session_reboot=Pattern("session_reboot"),
                         job_success=Pattern("job_success"), job_warn=Pattern("job_warn"),
                         machine_unfit_for_service=Pattern("machine_unfit_for_service"),
                         watchdogs={"wd1": Watchdog(start=Pattern(r"wd1_start"),
                                                    reset=Pattern(r"wd1_reset"),
                                                    stop=Pattern(r"wd1_stop"))})

    assert state.job_status == "INCOMPLETE"
    assert not state.session_has_ended
    assert not state.needs_reboot
    assert not state.machine_is_unfit_for_service

    assert state.process_line(b"oh oh oh") == set()
    assert state.job_status == "INCOMPLETE"
    assert not state.session_has_ended
    assert not state.needs_reboot
    assert not state.machine_is_unfit_for_service

    assert state.process_line(b"blabla session_reboot blabla") == {"session_reboot"}
    assert state.job_status == "INCOMPLETE"
    assert not state.session_has_ended
    assert state.needs_reboot
    assert not state.machine_is_unfit_for_service

    state.reset_per_boot_state()
    assert not state.session_has_ended
    assert not state.needs_reboot

    assert state.process_line(b"blabla session_end blaba\n") == {"session_end"}
    assert state.job_status == "FAIL"
    assert state.session_has_ended
    assert not state.needs_reboot
    assert not state.machine_is_unfit_for_service

    assert state.process_line(b"blabla job_success blaba\n") == {"job_success"}
    assert state.job_status == "PASS"
    assert state.session_has_ended
    assert not state.needs_reboot
    assert not state.machine_is_unfit_for_service

    assert state.process_line(b"blabla job_warn blaba\n") == {"job_warn"}
    assert state.job_status == "WARN"
    assert state.session_has_ended
    assert not state.needs_reboot
    assert not state.machine_is_unfit_for_service

    assert state.process_line(b"blabla machine_unfit_for_service blaba\n") == {"machine_unfit_for_service"}
    assert state.job_status == "WARN"
    assert state.session_has_ended
    assert not state.needs_reboot
    assert state.machine_is_unfit_for_service

    state.watchdogs.get("wd1").set_timeout(Timeout.create(name="wd1", seconds=1, retries=1))
    assert state.process_line(b"blabla wd1_start blaba\n") == {"wd1.start"}
    assert state.job_status == "WARN"
    assert state.session_has_ended
    assert not state.needs_reboot
    assert state.machine_is_unfit_for_service


def test_ConsoleState__default():
    console_state = ConsoleState()

    print(console_state.session_end.regex.pattern)
    assert console_state.session_end.regex.pattern == b"^\\[[\\d \\.]{12}\\] reboot: Power Down$"
    assert console_state.session_reboot is None
    assert console_state.job_success is None
    assert console_state.job_warn is None
    assert console_state.machine_unfit_for_service is None

    config.CONSOLE_PATTERN_DEFAULT_MACHINE_UNFIT_FOR_SERVICE_REGEX = "TEST"
    console_state = ConsoleState()
    assert console_state.machine_unfit_for_service.regex.pattern == b"TEST"


def test_ConsoleState_from_job__full():
    console_state = ConsoleState(**{
        "session_end": {
            "regex": "session_end"
        }, "session_reboot": {
            "regex": "session_reboot"
        }, "job_success": {
            "regex": "job_success"
        }, "job_warn": {
            "regex": "job_warn"
        }, "machine_unfit_for_service": {
            "regex": "unfit_for_service"
        }, "watchdogs": {
            "mywatchdog": {
                "start": {"regex": "start"},
                "reset": {"regex": "reset"},
                "stop": {"regex": "stop"},
            }
        }
    })

    assert console_state.session_end.regex.pattern == b"session_end"
    assert console_state.session_reboot.regex.pattern == b"session_reboot"
    assert console_state.job_success.regex.pattern == b"job_success"
    assert console_state.job_warn.regex.pattern == b"job_warn"
    assert console_state.machine_unfit_for_service.regex.pattern == b"unfit_for_service"


# CollectionOfLists


def test_CollectionOfLists__invalid_collection_name():
    # Can't use a keyword as category
    with pytest.raises(ValidationError):
        CollectionOfLists[str]({":uncategorised": ["Hello"]})


def test_CollectionOfLists__from_job():
    # CollectionOfLists
    val = CollectionOfLists[str]()
    assert CollectionOfLists[str].from_job(val) == val

    # Single value
    assert CollectionOfLists[str].from_job("hello").as_list == ["hello"]

    # List of values
    assert CollectionOfLists[int].from_job([1, 2]).as_list == [1, 2]

    # Categories
    cl = CollectionOfLists[str].from_job({"01-cat1": "Neo!",
                                          "00-cat2": ["Wake", "up,"],
                                          ":uncategorised": ["Don't", "be", "lazy!"]})
    assert cl.uncategorised == ["Don't", "be", "lazy!"]
    assert cl.as_list == ["Wake", "up,", "Neo!", "Don't", "be", "lazy!"]
    assert list(cl) == cl.as_list

    # Invalid collection name
    with pytest.raises(ValidationError):
        CollectionOfLists[str].from_job({":cat": ["Hello"]})


def test_CollectionOfLists__str():
    assert str(CollectionOfLists[str](uncategorised=["Wake", "up,", "Neo!"])) == "Wake up, Neo!"


def test_CollectionOfLists__equality():
    categories = {
        "cat1": ["Hello"],
        "cat2": ["World"]
    }
    uncategorised = ["Wake", "up,", "Neo!"]

    # Make sure that 2 objects constructed with the same values are equal
    assert CollectionOfLists[str](categories, uncategorised) == CollectionOfLists[str](categories, uncategorised)

    # Make sure all combinaisons of missing inputs don't result in a match
    assert CollectionOfLists[str](categories) != CollectionOfLists[str](categories, uncategorised)
    assert CollectionOfLists[str](uncategorised=uncategorised) != CollectionOfLists[str](categories, uncategorised)
    assert CollectionOfLists[str](categories, uncategorised) != CollectionOfLists[str](categories)
    assert CollectionOfLists[str](categories, uncategorised) != CollectionOfLists[str](uncategorised=uncategorised)

    # Comparison to a string
    assert CollectionOfLists[str](categories, uncategorised) == "Hello World Wake up, Neo!"


def test_CollectionOfLists__update():
    categories = {
        "greeting": ["Hello"],
        "who": ["World"],
    }
    uncategorised = ["and", "the", "universe!"]

    c = CollectionOfLists[str](categories=categories, uncategorised=uncategorised)
    assert c == "Hello World and the universe!"

    # Replacing a category also keeps the uncategorised
    c.update(CollectionOfLists[str](categories={"greeting": ["Bye Bye"]}))
    assert c == "Bye Bye World and the universe!"

    # Get rid of a complete category, add another one, and replace the uncategorised list
    c.update(CollectionOfLists[str](categories={"greeting": ["Welcome"], "who": []},
                                    uncategorised=["my", "son", "to", "the", "machine"]))
    assert c == "Welcome my son to the machine"


# Deployment

def test_KernelDeployment_multiline_string():
    assert KernelDeployment(cmdline="toto").cmdline == "toto"
    assert KernelDeployment(cmdline=["tag1", "tag2"]).cmdline == "tag1 tag2"
    assert KernelDeployment().cmdline is None


def test_FastbootDeployment():
    assert str(FastbootDeployment()) == "<Fastboot: >"

    fb = str(FastbootDeployment(header_version=4, dtb_offset=0x123456))
    assert fb == "<Fastboot: header_version=4, dtb_offset=0x123456>"


def test_DeploymentState():
    deployment = DeploymentState()

    assert deployment.kernel_url is None
    assert deployment.initramfs_url is None
    assert deployment.kernel_cmdline is None

    deployment.update({})

    assert deployment.kernel_url is None
    assert deployment.initramfs_url is None
    assert deployment.kernel_cmdline is None

    deployment.update({"kernel": {"url": "https://host.tld/kernel_url", "cmdline": "cmdline"},
                       "initramfs": {"url": "https://host.tld/initramfs_url"},
                       "dtb": {"url": "https://host.tld/dtb_url"}})

    assert deployment.kernel_url == "https://host.tld/kernel_url"
    assert deployment.initramfs_url == "https://host.tld/initramfs_url"
    assert deployment.kernel_cmdline == "cmdline"

    assert str(deployment) == """<Deployment:
    kernel_url: https://host.tld/kernel_url
    initramfs_url: https://host.tld/initramfs_url
    kernel_cmdline: cmdline
    dtb_url: https://host.tld/dtb_url>
"""

    # Update only one kernel field
    deployment.update({"kernel": {"cmdline": "cmdline2"}})
    assert deployment.kernel_url == "https://host.tld/kernel_url"
    assert deployment.initramfs_url == "https://host.tld/initramfs_url"
    assert deployment.kernel_cmdline == "cmdline2"


# Job


def test_Job__simple():
    simple_job = """
version: 1
target:
  id: "b4:2e:99:f0:76:c5"
console_patterns:
  session_end:
    regex: "session_end"
deployment:
  start:
    kernel:
      url: "https://host.tld/kernel_url"
      cmdline:
        - my
        - start cmdline
    initramfs:
      url: "https://host.tld/initramfs_url"
"""
    job = Job.render_with_resources(simple_job)

    assert job.version == 1
    assert job.deadline == datetime.max

    assert job.target.id == "b4:2e:99:f0:76:c5"
    assert job.target.tags == []

    assert job.deployment_start.kernel_url == "https://host.tld/kernel_url"
    assert job.deployment_start.initramfs_url == "https://host.tld/initramfs_url"
    assert job.deployment_start.kernel_cmdline == "my start cmdline"
    assert job.deployment_start.fastboot is None
    assert job.deployment_start.artifacts == {
        "https://host.tld/kernel_url": {("kernel", ): job.deployment_start.kernel},
        "https://host.tld/initramfs_url": {("initramfs", ): job.deployment_start.initramfs},
    }

    assert job.deployment_continue.kernel_url == job.deployment_start.kernel_url
    assert job.deployment_continue.initramfs_url == job.deployment_start.initramfs_url
    assert job.deployment_continue.kernel_cmdline == job.deployment_start.kernel_cmdline
    assert job.deployment_continue.fastboot == job.deployment_start.fastboot
    assert job.deployment_continue.artifacts == job.deployment_start.artifacts

    assert job.deployment.artifacts == {
        "https://host.tld/kernel_url": {
            ("start", "kernel", ): job.deployment_start.kernel,
            ("continue", "kernel", ): job.deployment_continue.kernel
        },
        "https://host.tld/initramfs_url": {
            ("start", "initramfs", ): job.deployment_start.initramfs,
            ("continue", "initramfs", ): job.deployment_continue.initramfs
        },
    }

    # Make sure the job's __str__ method does not crash
    str(job)


def test_Job__override_continue():
    override_job = """
version: 1
deadline: "2021-03-31 00:00:00"
target:
  id: "b4:2e:99:f0:76:c6"
  tags: ["amdgpu:gfxversion::gfx10"]
console_patterns:
  session_end:
    regex: "session_end"
deployment:
  start:
    kernel:
      url: "https://host.tld/kernel_url"
      cmdline:
        defaults:
          - my
          - default cmdline
    initramfs:
      url: "https://host.tld/initramfs_url"
  continue:
    kernel:
      url: "https://host.tld/kernel_url_2"
      cmdline: "my continue cmdline"
    initramfs:
      url: "https://host.tld/initramfs_url_2"
    dtb:
      url: "https://host.tld/dtb_url_2"
    fastboot:
      header_version: 42
      base: 0x123456789
      kernel_offset: 0xcafe
      ramdisk_offset: 0xc0de
      dtb_offset: 0xbeef
      tags_offset: 0xdead
      board: "myboard"
      pagesize: 16384
"""
    job = Job.render_with_resources(override_job)

    assert job.version == 1
    assert job.deadline == datetime.fromisoformat("2021-03-31 00:00:00")

    assert job.target.id == "b4:2e:99:f0:76:c6"
    assert job.target.tags == ["amdgpu:gfxversion::gfx10"]

    assert job.deployment_start.kernel_url == "https://host.tld/kernel_url"
    assert job.deployment_start.initramfs_url == "https://host.tld/initramfs_url"
    assert job.deployment_start.kernel_cmdline == "my default cmdline"
    assert job.deployment_start.dtb_url is None
    assert job.deployment_start.artifacts == {
        "https://host.tld/kernel_url": {("kernel", ): job.deployment_start.kernel},
        "https://host.tld/initramfs_url": {("initramfs", ): job.deployment_start.initramfs},
    }

    assert job.deployment_continue.kernel_url == "https://host.tld/kernel_url_2"
    assert job.deployment_continue.initramfs_url == "https://host.tld/initramfs_url_2"
    assert job.deployment_continue.kernel_cmdline == "my default cmdline my continue cmdline"
    assert job.deployment_continue.dtb_url == "https://host.tld/dtb_url_2"
    assert job.deployment_continue.artifacts == {
        "https://host.tld/kernel_url_2": {("kernel", ): job.deployment_continue.kernel},
        "https://host.tld/initramfs_url_2": {("initramfs", ): job.deployment_continue.initramfs},
        "https://host.tld/dtb_url_2": {("dtb", ): job.deployment_continue.dtb},
    }

    assert str(job.deployment_continue.fastboot) == ("<Fastboot: header_version=42, base=0x123456789, "
                                                     "kernel_offset=0xcafe, ramdisk_offset=0xc0de, dtb_offset=0xbeef, "
                                                     "tags_offset=0xdead, board=myboard, pagesize=16384>")

    assert job.deployment.artifacts == {
        "https://host.tld/kernel_url": {("start", "kernel", ): job.deployment_start.kernel},
        "https://host.tld/initramfs_url": {("start", "initramfs", ): job.deployment_start.initramfs},
        "https://host.tld/kernel_url_2": {("continue", "kernel", ): job.deployment_continue.kernel},
        "https://host.tld/initramfs_url_2": {("continue", "initramfs", ): job.deployment_continue.initramfs},
        "https://host.tld/dtb_url_2": {("continue", "dtb", ): job.deployment_continue.dtb},
    }


class MockMachine:
    @property
    def ready_for_service(self):
        return True

    @property
    def id(self):
        return "b4:2e:99:f0:76:c5"

    @property
    def tags(self):
        return ["some", "tags"]

    @property
    def local_tty_device(self):
        return "ttyS0"

    @property
    def ip_address(self):
        return "10.42.0.123"

    @property
    def safe_attributes(self):
        return {
            "base_name": "base_name",
            "full_name": "full_name",
            "tags": self.tags,
            "ip_address": self.ip_address,
            "local_tty_device": self.local_tty_device,
            "ready_for_service": self.ready_for_service,
        }


class MockBucket:
    @property
    def name(self):
        return "bucket_name"

    @property
    def minio(self):
        return MagicMock(url="minio_url")

    @property
    def credentials(self):
        return MagicMock(dut=("access", "secret"))


@patch('server.config.job_environment_vars')
def test_Job__sample(job_env):
    job_env.return_value = {'MINIO_URL': 'http://localhost:9000/testing-url',
                            'NTP_PEER': '10.42.0.1',
                            'PULL_THRU_REGISTRY': '10.42.0.1:8001'}

    m = MockMachine()
    job = Job.from_path("src/valve_gfx_ci/executor/server/tests/sample_job.yml", m)

    assert job.version == 1
    assert job.deadline == datetime.fromisoformat("2021-03-31 00:00:00")

    assert job.target.id == m.id
    assert job.target.tags == m.tags

    assert job.deployment_start.kernel_url == "http://localhost:9000/testing-url/test-kernel"
    assert job.deployment_start.initramfs_url == "http://localhost:9000/testing-url/test-initramfs"

    assert job.deployment_start.kernel_cmdline == 'b2c.container="docker://10.42.0.1:8001/infra/machine-registration:latest check" b2c.ntp_peer="10.42.0.1" b2c.pipefail b2c.cache_device=auto b2c.container="-v /container/tmp:/storage docker://10.42.0.1:8002/tests/mesa:12345" console=ttyS0,115200 earlyprintk=vga,keep SALAD.machine_id=b4:2e:99:f0:76:c5 extra=""'  # noqa: E501

    assert job.deployment_continue.kernel_url == "http://localhost:9000/testing-url/test-kernel"
    assert job.deployment_continue.initramfs_url == "http://localhost:9000/testing-url/test-initramfs"
    assert job.deployment_continue.kernel_cmdline == 'b2c.container="docker://10.42.0.1:8001/infra/machine-registration:latest check" b2c.ntp_peer=10.42.0.1 b2c.pipefail b2c.cache_device=auto b2c.container="-v /container/tmp:/storage docker://10.42.0.1:8002/tests/mesa:12345 resume"'  # noqa: E501


def test_Job__invalid_format():
    job = """
version: 1
target:
  id: "b4:2e:99:f0:76:c6"
console_patterns:
  session_end:
    regex: "session_end"
  reboot:
    regex: "toto"
deployment:
  start:
    kernel:
      url: "https://host.tld/kernel_url"
      cmdline:
        - my
        - start cmdline
    initramfs:
      url: "https://host.tld/initramfs_url"
"""

    with pytest.raises(ValueError) as exc:
        Job.render_with_resources(job)

    assert "console_patterns.reboot\n  Unexpected keyword argument" in str(exc.value)


@patch('server.config.job_environment_vars')
def test_Job__from_machine(job_env):
    job_env.return_value = {'NTP_PEER': '10.42.0.1'}

    simple_job = """
version: 1
target:
  id: {{ machine_id }}
console_patterns:
  session_end:
    regex: "session_end"
deployment:
  start:
    kernel:
      url: "https://host.tld/kernel_url"
      cmdline:
        - my {{ minio_url }}
        - start cmdline {{ ntp_peer }}
        - hostname {{ machine.full_name }}
        - extra {{ extra }}
    initramfs:
      url: "https://host.tld/initramfs_url"
"""
    job = Job.render_with_resources(simple_job, MockMachine(), MockBucket(), extra="parameter")

    assert job.version == 1
    assert job.deadline == datetime.max

    assert job.target.id == "b4:2e:99:f0:76:c5"
    assert job.target.tags == []

    assert job.deployment_start.kernel_url == "https://host.tld/kernel_url"
    assert job.deployment_start.initramfs_url == "https://host.tld/initramfs_url"
    assert (job.deployment_start.kernel_cmdline == "my minio_url start cmdline 10.42.0.1 hostname full_name "
                                                   "extra parameter")

    assert job.deployment_continue.kernel_url == job.deployment_start.kernel_url
    assert job.deployment_continue.initramfs_url == job.deployment_start.initramfs_url
    assert job.deployment_continue.kernel_cmdline == job.deployment_start.kernel_cmdline


def test_Job__watchdogs():
    override_job = """
version: 1
target:
  id: "b4:2e:99:f0:76:c6"
timeouts:
  watchdogs:
    wd1:
      minutes: 1
console_patterns:
  session_end:
    regex: "session_end"
  watchdogs:
    wd1:
      start:
        regex: "start"
      reset:
        regex: "reset"
      stop:
        regex: "stop"
deployment:
  start:
    kernel:
      url: "https://host.tld/kernel_url"
      cmdline: "cmdline"
    initramfs:
      url: "https://host.tld/initramfs_url"
"""
    job = Job.render_with_resources(override_job)
    assert job.console_patterns.watchdogs["wd1"].timeout == job.timeouts.watchdogs["wd1"]

    # Test that getting the string does not explode
    str(job)


# Job vars

@mock.patch.dict(os.environ, {"EXECUTOR_JOB__FDO_PROXY_REGISTRY": "10.10.10.1:1234"})
def test_server_config_job_environment_vars():
    ret = server.config.job_environment_vars()

    assert "MINIO_URL" in ret

    assert "FDO_PROXY_REGISTRY" in ret
    assert ret["FDO_PROXY_REGISTRY"] == "10.10.10.1:1234"
