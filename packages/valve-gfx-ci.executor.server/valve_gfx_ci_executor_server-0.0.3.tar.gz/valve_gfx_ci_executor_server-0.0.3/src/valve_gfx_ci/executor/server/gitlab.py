from dataclasses import dataclass
from jinja2 import Template
from typing import List
import requests
import math
import platform
import psutil

from .logger import logger
from . import config


class SanitizedFieldsMixin:
    @classmethod
    def from_api(cls, fields, **kwargs):
        valid_fields = {f.name for f in cls.__dataclass_fields__.values()}

        sanitized_kwargs = dict(fields)
        for arg in fields:
            if arg not in valid_fields:
                sanitized_kwargs.pop(arg)

        return cls(**sanitized_kwargs, **kwargs)


@dataclass
class GitlabRunnerRegistration(SanitizedFieldsMixin):
    id: int
    token: str


@dataclass
class Runner(SanitizedFieldsMixin):
    id: int
    description: str
    active: bool
    paused: bool
    online: bool
    tag_list: List[str]
    maximum_timeout: int


def register_runner(gitlab_url: str, registration_token: str,
                    description: str, tag_list: list[str],
                    run_untagged: bool = False, maximum_timeout: int = 3600,
                    runner_type: str = "instance_type",
                    group_id: int = None, project_id: int = None):
    # Make sure the group or project id is set when needed by the runner type
    assert runner_type in {"instance_type", "group_type", "project_type"}
    assert runner_type != "group_type" or group_id is not None
    assert runner_type != "project_type" or project_id is not None

    params = {
        "description": description,
        "tag_list": ",".join(tag_list),
        "run_untagged": run_untagged,
        "maximum_timeout": maximum_timeout,
        "runner_type": runner_type,
    }

    if group_id:
        params["group_id"] = group_id
    if project_id:
        params["project_id"] = project_id

    r = requests.post(f"{gitlab_url}/api/v4/user/runners",
                      headers={"PRIVATE-TOKEN": registration_token}, params=params)
    if r.status_code == 201:
        return GitlabRunnerRegistration.from_api(r.json())
    else:
        return None


def unregister_runner(gitlab_url: str, token: str):
    r = requests.delete(f"{gitlab_url}/api/v4/runners", params={"token": token})
    return r.status_code == 204


def verify_runner_token(gitlab_url: str, token: str):
    # WARNING: The interface for this function is so that we will return
    # False *ONLY* when Gitlab tells us the token is invalid.
    # If Gitlab is unreachable, we will return True.
    #
    # This is a conscious decision, as we never want to throw away a perfectly-good
    # token, just because of a network outtage.

    r = requests.post(f"{gitlab_url}/api/v4/runners/verify", params={"token": token})
    return not r.status_code == 403


def runner_details(gitlab_url: str, private_token: str, runner_id: int):
    r = requests.get(f"{gitlab_url}/api/v4/runners/{runner_id}",
                     headers={"PRIVATE-TOKEN": private_token})
    if r.status_code == 200:
        return Runner.from_api(r.json())
    else:
        return None


def generate_gateway_runner_tags():
    def next_power_of_2(x):
        return 1 if x == 0 else 2**math.ceil(math.log2(x))

    tags = {f"{config.FARM_NAME}-gateway", 'CI-gateway', f"cpu:arch:{platform.machine()}"}

    cpu_count = psutil.cpu_count(logical=False)
    tags.add(f"cpu:cores:{cpu_count}")
    if cpu_count >= 8:
        tags.add("cpu:cores:8+")
    if cpu_count >= 16:
        tags.add("cpu:cores:16+")
    if cpu_count >= 32:
        tags.add("cpu:cores:32+")

    mem_gib = next_power_of_2(psutil.virtual_memory().total / 1024 / 1024 / 1024)
    tags.add(f"mem:size:{mem_gib}GiB")
    if mem_gib >= 8:
        tags.add("mem:size:8+GiB")
    if mem_gib >= 32:
        tags.add("mem:size:32+GiB")

    return tags


def generate_runner_config(mars_db):
    logger.info("Generate the GitLab runner configuration")
    with open(config.GITLAB_CONF_TEMPLATE_FILE) as f:
        params = {
            "config": config,
            "mars_db": mars_db,
            "cpu_count": psutil.cpu_count(),
            "ram_total_MB": psutil.virtual_memory().total / 1e6
        }
        config_toml = Template(f.read()).render(**params)

    with open(config.GITLAB_CONF_FILE, 'w') as f:
        f.write(config_toml)
