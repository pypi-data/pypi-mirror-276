import time

import click

from komo import printing
from komo.cli.utils import exit_on_http_error
from komo.core import get_machine, print_machine_setup_logs
from komo.types import JobStatus


@click.command("setup-logs")
@click.option("--follow", "-f", is_flag=True, default=False)
@click.argument(
    "machine_name",
    type=str,
)
@exit_on_http_error
def cmd_setup_logs(
    follow: bool,
    machine_name: str,
):
    print_machine_setup_logs(machine_name, follow)
