from dataclasses import fields, field, asdict
from datetime import datetime, timedelta
from collections import defaultdict
from pydantic.dataclasses import dataclass
from pydantic.functional_validators import AfterValidator
from pydantic import field_validator, PositiveInt, NonNegativeInt, BaseModel, Field, HttpUrl
from typing import Annotated, Any, Dict, Generic, List, Union, Optional, TypeVar
from jinja2 import Template, ChainableUndefined
import yaml
import re

from . import config


@dataclass(config=dict(extra="forbid"))
class Target:
    id: Optional[str] = None
    tags: list[str] = None

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        if not self.id and self.tags is None:
            raise ValueError("The target is neither identified by tags or id. "
                             "Use empty tags to mean 'any machines'.")

        if self.tags is None:
            self.tags = []

    def __str__(self):
        return f"<Target: id={self.id}, tags={self.tags}>"


@dataclass(config=dict(extra="forbid"))
class Timeout:
    days: Optional[float] = None
    hours: Optional[float] = None
    minutes: Optional[float] = None
    seconds: Optional[float] = None
    milliseconds: Optional[float] = None
    retries: NonNegativeInt = 0

    @classmethod
    def create(cls, name, *args, **kwargs):
        timeout = cls(*args, **kwargs)
        timeout.name = name
        return timeout

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        days = self.days or 0
        hours = self.hours or 0
        minutes = self.minutes or 0
        seconds = self.seconds or 0
        milliseconds = self.milliseconds or 0

        self.timeout = timedelta(days=days, hours=hours,
                                 minutes=minutes, seconds=seconds,
                                 milliseconds=milliseconds)

        if (self.days is None and self.hours is None and self.minutes is None and
                self.seconds is None and self.milliseconds is None):
            self.timeout = timedelta.max

        self.started_at = None
        self.retried = 0

    @property
    def active_for(self):
        if self.started_at is not None:
            return datetime.now() - self.started_at
        else:
            return None

    @property
    def is_started(self):
        return self.started_at is not None

    @property
    def has_expired(self):
        active_for = self.active_for
        return active_for is not None and active_for > self.timeout

    def start(self):
        self.started_at = datetime.now()

    def reset(self, when=None):
        if when is None:
            when = datetime.now()
        self.started_at = when

    def retry(self):
        self.stop()
        self.retried += 1

        return self.retried <= self.retries

    def stop(self):
        self.started_at = None

    def __str__(self):
        return f"<Timeout {self.name}: value={self.timeout}, retries={self.retried}/{self.retries}>"


@dataclass(config=dict(extra="forbid"))
class Timeouts:
    overall: Timeout = field(default_factory=lambda: Timeout(hours=6))
    infra_setup: Timeout = field(default_factory=Timeout)
    infra_teardown: Timeout = field(default_factory=lambda: Timeout(minutes=10))
    boot_cycle: Timeout = field(default_factory=Timeout)
    console_activity: Timeout = field(default_factory=Timeout)
    first_console_activity: Timeout = field(default_factory=Timeout)
    watchdogs: dict[str, Timeout] = field(default_factory=dict)

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        # Make sure to add the name to every field
        for f in fields(self):
            if f.type is Timeout:
                getattr(self, f.name).name = f.name

        # Add the watchdogs' names
        for name, wd in self.watchdogs.items():
            wd.name = name

        # Ensure that the overall and tear-down timeouts have retries=0
        for timeout in [self.overall, self.infra_teardown]:
            if timeout.retries != 0:
                raise ValueError("Neither the overall nor the teardown timeout can have retries")

    def __iter__(self):
        for f in fields(self):
            if f.type is Timeout:
                yield getattr(self, f.name)

        for wd in self.watchdogs.values():
            yield wd

    @property
    def expired_list(self):
        expired = []
        for timeout in self:
            if timeout.has_expired:
                expired.append(timeout)
        return expired

    @property
    def has_expired(self):
        return len(self.expired_list) > 0


@dataclass(config=dict(extra="forbid"))
class Pattern:
    regex: str

    @field_validator("regex")
    @classmethod
    def convert_to_regex(cls, v):
        try:
            return re.compile(v.encode())
        except re.error as e:
            raise ValueError(f"Console pattern '{v}' is not a valid regular expression: {e.msg}")

    def __str__(self):
        return f"{self.regex.pattern}"


@dataclass(config=dict(extra="forbid"))
class Watchdog:
    start: Pattern
    reset: Pattern
    stop: Pattern

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        self.timeout = None

    def set_timeout(self, timeout):
        self.timeout = timeout

    def process_line(self, line):
        # Do not parse lines if no timeout is associated
        if self.timeout is None:
            return {}

        if not self.timeout.is_started:
            if self.start.regex.search(line):
                self.timeout.start()
                return {"start"}
        else:
            if self.reset.regex.search(line):
                self.timeout.reset()
                return {"reset"}
            elif self.stop.regex.search(line):
                self.timeout.stop()
                return {"stop"}

        return {}

    # I would have loved to re-use `stop()` here, but it collides with the stop pattern
    def cancel(self):
        if self.timeout is not None:
            self.timeout.stop()


@dataclass(config=dict(extra="forbid"))
class ConsoleState:
    session_end: Pattern = field(default_factory=lambda: Pattern(regex=r"^\[[\d \.]{12}\] reboot: Power Down$"))
    session_reboot: Optional[Pattern] = None
    job_success: Optional[Pattern] = None
    job_warn: Optional[Pattern] = None
    machine_unfit_for_service: Optional[Pattern] = None
    watchdogs: dict[str, Watchdog] = field(default_factory=dict)

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        self._patterns = dict()
        self._matched = set()

        if self.machine_unfit_for_service is None and config.CONSOLE_PATTERN_DEFAULT_MACHINE_UNFIT_FOR_SERVICE_REGEX:
            self.machine_unfit_for_service = Pattern(config.CONSOLE_PATTERN_DEFAULT_MACHINE_UNFIT_FOR_SERVICE_REGEX)

        # Generate the list of patterns to match
        for f in fields(self):
            if f.type in [Pattern, Optional[Pattern]]:
                pattern = getattr(self, f.name, None)
                if pattern:
                    pattern.name = f.name
                    self._patterns[f.name] = pattern

    def process_line(self, line):
        # Try matching all the patterns
        matched = set()
        for name, pattern in self._patterns.items():
            if pattern.regex.search(line):
                matched.add(name)
        self._matched.update(matched)

        # Try matching the watchdogs
        for name, wd in self.watchdogs.items():
            _matched = wd.process_line(line)
            matched.update({f"{name}.{m}" for m in _matched})

        return matched

    def reset_per_boot_state(self):
        self._matched.discard("session_reboot")

    @property
    def session_has_ended(self):
        return "session_end" in self._matched or "unfit_for_service" in self._matched

    @property
    def needs_reboot(self):
        return "session_reboot" in self._matched

    @property
    def machine_is_unfit_for_service(self):
        return "machine_unfit_for_service" in self._matched

    @property
    def job_status(self):
        if "session_end" not in self._matched:
            return "INCOMPLETE"

        if "job_success" in self._patterns:
            if "job_success" in self._matched:
                if "job_warn" in self._matched:
                    return "WARN"
                else:
                    return "PASS"
            else:
                return "FAIL"
        else:
            return "COMPLETE"


class DeploymentMixin:
    def update(self, d):
        # Nothing to do if `d` is empty
        if not d:
            return

        # Convert `d` from dict to the proper instance if needed
        if type(d) is dict:
            d = type(self)(**d)

        # Assert that both `self` and `d` share the same type
        assert type(d) is type(self)

        # Check every field
        for f in fields(self):
            if new := getattr(d, f.name, None):
                # If the value was already set and the new value is a DeploymentMixin, call `update()` rather than
                # simply copying
                if cur := getattr(self, f.name):
                    if isinstance(cur, DeploymentMixin):
                        cur.update(new)
                        continue

                setattr(self, f.name, new)

    @classmethod
    def _add_artifacts_from_object(cls, artifacts, obj_name, obj):
        for url, paths in obj.artifacts.items():
            for path, artifact in paths.items():
                artifacts[url][(obj_name, ) + path] = artifact

    @property
    def artifacts(self):
        artifacts = defaultdict(dict)

        for f in fields(self):
            if f_value := getattr(self, f.name, None):
                if isinstance(f_value, DeploymentMixin):
                    self._add_artifacts_from_object(artifacts, f.name, f_value)
                elif f.name == "url":
                    artifacts[str(self.url)][()] = self

        return artifacts


T = TypeVar("T")


SingleItemOrList = T | List[T]


def is_valid_category_name(v: str, allow_keywords=False) -> str:
    if v[0] == ":":
        if not allow_keywords or v not in [":uncategorised"]:
            raise ValueError("User-defined category names cannot start with ':'")
    return v


Category = Annotated[str, AfterValidator(lambda v: is_valid_category_name(v, allow_keywords=False))]


CategoryOrKeyword = Annotated[str, AfterValidator(lambda v: is_valid_category_name(v, allow_keywords=True))]


JobCollectionOfLists = SingleItemOrList | Dict[CategoryOrKeyword, SingleItemOrList]


@dataclass(config=dict(extra="forbid"))
class CollectionOfLists(Generic[T], DeploymentMixin):
    categories: Optional[Dict[Category, List[T]]] = field(default_factory=dict)
    uncategorised: Optional[List[T]] = field(default_factory=list)

    @property
    def as_list(self) -> List[T]:
        # NOTE: We are sorting the categories by names to let users order how elements are staged
        cl = []
        for k in sorted(self.categories.keys()):
            cl.extend(self.categories[k])
        return cl + self.uncategorised

    def update(self, d: "CollectionOfLists"):
        assert isinstance(d, CollectionOfLists)

        self.categories.update(d.categories)

        if len(d.uncategorised) > 0:
            self.uncategorised = d.uncategorised

    def __str__(self):
        return " ".join([str(v) for v in self.as_list])

    def __eq__(self, other: "CollectionOfLists"):
        if isinstance(other, str):
            return str(self) == other
        else:
            for f in fields(self):
                if getattr(self, f.name, None) != getattr(other, f.name, None):
                    return False

            return True

    def __iter__(self):
        return iter(self.as_list)

    @classmethod
    def from_job(cls, v: "CollectionOfLists" | JobCollectionOfLists):
        def to_list(value: SingleItemOrList):
            if isinstance(value, list):
                return value
            else:
                return [value]

        categories = dict()
        uncategorised = []
        if isinstance(v, cls):
            return v
        elif isinstance(v, dict):
            uncategorised = v.pop(":uncategorised", [])
            for key, value in v.items():
                categories[key] = to_list(value)
        else:
            uncategorised = to_list(v)

        return cls(categories=categories, uncategorised=uncategorised)


ComplexList = Union[Annotated[JobCollectionOfLists, AfterValidator(lambda v: CollectionOfLists.from_job(v))],
                    CollectionOfLists[T]]


@dataclass(config=dict(extra="forbid"))
class FileHttpUrl(DeploymentMixin):
    url: Optional[HttpUrl] = None


@dataclass(config=dict(extra="forbid"))
class KernelDeployment(FileHttpUrl, DeploymentMixin):
    cmdline: ComplexList[str] = None


@dataclass(config=dict(extra="forbid"))
class StorageHttpArtifactDeployment(DeploymentMixin):
    path: str
    data: Optional[str | bytes] = None

    # Proposals:
    # args: Optional[Dict[str, str]] = None  # Only match when the following GET params are set


@dataclass(config=dict(extra="forbid"))
class StorageDeployment(DeploymentMixin):
    http: Optional[ComplexList[StorageHttpArtifactDeployment]] = field(default_factory=list)


@dataclass(config=dict(extra="forbid"))
class FastbootDeployment(DeploymentMixin):
    header_version: Optional[int] = None
    base: Optional[int] = None
    kernel_offset: Optional[int] = None
    ramdisk_offset: Optional[int] = None
    dtb_offset: Optional[int] = None
    tags_offset: Optional[int] = None
    board: Optional[str] = None
    pagesize: Optional[int] = None

    @property
    def fields_set(self):
        return {k: v for k, v in asdict(self).items() if v}

    def __str__(self):
        non_empty_fields = list()
        for key, value in self.fields_set.items():
            # Show some of the fields as hex values, since it is likely what people used
            if key in ["base"] or "_offset" in key:
                value = hex(value)
            non_empty_fields.append(f"{key}={value}")

        s = ", ".join(non_empty_fields)
        return f"<Fastboot: {s}>"


@dataclass(config=dict(extra="forbid"))
class DeploymentState(DeploymentMixin):
    kernel: Optional[KernelDeployment] = None
    initramfs: Optional[FileHttpUrl] = None
    dtb: Optional[FileHttpUrl] = None
    storage: Optional[StorageDeployment] = None
    fastboot: Optional[FastbootDeployment] = None

    @classmethod
    def object_url(cls, obj):
        if obj and obj.url:
            return str(obj.url)

    # NOTE: For backwards compatibility
    @property
    def kernel_url(self):
        return self.object_url(self.kernel)

    # NOTE: For backwards compatibility
    @property
    def kernel_cmdline(self):
        return str(self.kernel.cmdline) if self.kernel else None

    # NOTE: For backwards compatibility
    @property
    def initramfs_url(self):
        return self.object_url(self.initramfs)

    # NOTE: For backwards compatibility
    @property
    def dtb_url(self):
        return self.object_url(self.dtb)

    def __str__(self):
        str_fields = [
            f"kernel_url: {self.kernel_url}",
            f"initramfs_url: {self.initramfs_url}",
            f"kernel_cmdline: {self.kernel_cmdline}"
        ]

        # Do not print these parameters if their value is None
        for optional_field in ["dtb_url", "fastboot"]:
            if f_value := getattr(self, optional_field, None):
                str_fields.append(f"{optional_field}: {f_value}")

        str_fields = "\n    ".join(str_fields)
        return f"""<Deployment:
    {str_fields}>
"""


# NOTE: Because the "continue" field in deployment cannot be used as a dataclass variable,
# we have to open code it using a pydantic BaseModel. Fortunately, pydantic is happy to
# allow us to use an alias for the field.
class Deployment(BaseModel):
    model_config = dict(populate_by_name=True, extra="forbid")

    start: DeploymentState
    continue_: DeploymentState = Field(default=None, alias='continue')

    def __init__(self, /, **data: Any):
        super().__init__(**data)

        continue_ = DeploymentState(**asdict(self.start))
        if self.continue_:
            continue_.update(self.continue_)
        self.continue_ = continue_

    @property
    def artifacts(self):
        artifacts = defaultdict(dict)

        DeploymentMixin._add_artifacts_from_object(artifacts, "start", self.start)
        DeploymentMixin._add_artifacts_from_object(artifacts, "continue", self.continue_)

        return artifacts


@dataclass(config=dict(extra="forbid"))
class Job:
    console_patterns: ConsoleState
    deployment: Deployment

    version: PositiveInt = 1
    deadline: datetime = datetime.max
    target: Target = field(default_factory=Target)
    timeouts: Timeouts = field(default_factory=Timeouts)

    # Function called once all the objects have been converted from dict
    # to their dataclass equivalent and field validation succeeded
    def __post_init__(self):
        # Associate all the timeouts to their respective watchdogs
        for name, wd in self.console_patterns.watchdogs.items():
            wd.set_timeout(self.timeouts.watchdogs.get(name))

    # NOTE: For backwards compatibility
    @property
    def deployment_start(self):
        return self.deployment.start if self.deployment else None

    # NOTE: For backwards compatibility
    @property
    def deployment_continue(self):
        return self.deployment.continue_ if self.deployment else None

    @classmethod
    def render_with_resources(cls, job_str, machine=None, bucket=None, **kwargs):
        template_params = {
            "ready_for_service": machine.ready_for_service if machine else True,
            "machine_id": machine.id if machine else "machine_id",
            "machine": machine.safe_attributes if machine else {},
            "machine_tags": machine.tags if machine else [],
            "local_tty_device": machine.local_tty_device if machine else "",
            **{k.lower(): v for k, v in config.job_environment_vars().items()},
            **kwargs,
        }

        if bucket:
            dut_creds = bucket.credentials('dut')

            template_params["minio_url"] = bucket.minio.url
            template_params["job_bucket"] = bucket.name
            template_params["job_bucket_access_key"] = dut_creds.username
            template_params["job_bucket_secret_key"] = dut_creds.password

        rendered_job_str = Template(job_str, undefined=ChainableUndefined).render(**template_params)
        return cls(**yaml.safe_load(rendered_job_str))

    @classmethod
    def from_path(cls, job_template_path, machine=None, bucket=None):
        with open(job_template_path, "r") as f_template:
            template_str = f_template.read()
            return Job.render_with_resources(template_str, machine, bucket)

    def __str__(self):
        if len(self.timeouts.watchdogs) == 0:
            timeout_watchdogs = "None"
        else:
            timeout_watchdogs = ""
            for name, wd in self.timeouts.watchdogs.items():
                timeout_watchdogs += f"\n            {name}: {wd}"

        if len(self.console_patterns.watchdogs) == 0:
            patterns_watchdogs = "None"
        else:
            patterns_watchdogs = ""
            for name, wd in self.console_patterns.watchdogs.items():
                patterns_watchdogs += f"\n            {name}:"
                patterns_watchdogs += f"\n                start: {wd.start}"
                patterns_watchdogs += f"\n                reset: {wd.reset}"
                patterns_watchdogs += f"\n                stop:  {wd.stop}"

        return f"""<Job:
    version: {self.version}

    deadline: {self.deadline}
    target: {self.target}

    timeouts:
        overall:                {self.timeouts.overall}
        infra_setup:            {self.timeouts.infra_setup}
        boot_cycle:             {self.timeouts.boot_cycle}
        console_activity:       {self.timeouts.console_activity}
        first_console_activity: {self.timeouts.first_console_activity}
        watchdogs:              {timeout_watchdogs}

    console patterns:
        session_end:               {self.console_patterns.session_end}
        session_reboot:            {self.console_patterns.session_reboot}
        job_success:               {self.console_patterns.job_success}
        job_warn:                  {self.console_patterns.job_warn}
        machine_unfit_for_service: {self.console_patterns.machine_unfit_for_service}
        watchdogs:              {patterns_watchdogs}

    start deployment:
        kernel_url:     {self.deployment_start.kernel_url}
        initramfs_url:  {self.deployment_start.initramfs_url}
        kernel_cmdline: {self.deployment_start.kernel_cmdline}

    continue deployment:
        kernel_url:     {self.deployment_continue.kernel_url}
        initramfs_url:  {self.deployment_continue.initramfs_url}
        kernel_cmdline: {self.deployment_continue.kernel_cmdline}>"""
