import os
import time
from typing import Optional

import click

from komo import printing
from komo.cli.utils import exit_on_http_error
from komo.core import get_service, launch_service
from komo.types import Cloud, ServiceConfig, ServiceStatus


@click.command("launch")
@click.option("--gpus", type=str, default=None)
@click.option("--cloud", "-c", type=str, default=None)
@click.option("--name", type=str, required=True)
@click.option("--detach", "-d", is_flag=True, default=False)
@click.argument("config_file", nargs=1)
@exit_on_http_error
def cmd_launch(
    gpus: Optional[str],
    cloud: Optional[str],
    name: str,
    detach: bool,
    config_file: str,
):
    if not os.path.isfile(config_file):
        printing.error(f"{config_file} does not exist")
        exit(1)

    service_config = ServiceConfig.from_yaml(config_file)
    if gpus:
        service_config.resources["gpus"] = gpus
    if cloud:
        service_config.cloud = Cloud(cloud)

    service = launch_service(
        service_config,
        name,
    )

    printing.success(f"Succesfully launched service {service.name}")

    if detach:
        return

    printing.info(f"Waiting for service {service.name} to start...")

    while True:
        service = get_service(service.name)

        if service.status in [
            ServiceStatus.CONTROLLER_INIT,
            ServiceStatus.REPLICA_INIT,
            ServiceStatus.NO_REPLICA,
        ]:
            time.sleep(5)
            continue

        break

    if service.status == ServiceStatus.READY:
        printing.success(
            f"Service {service.name} successfully started at {service.url}"
        )
    else:
        if service.status_message:
            printing.error(
                f"Service {service.name} failed with the following message:\n{service.status_message}"
            )
        else:
            printing.error(f"Service {service.name} failed to start")

        exit(1)
