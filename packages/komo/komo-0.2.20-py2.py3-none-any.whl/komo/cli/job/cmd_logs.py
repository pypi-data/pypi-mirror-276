import time

import click

from komo import printing
from komo.cli.utils import exit_on_http_error
from komo.core import get_job, print_job_logs
from komo.types import JobStatus


@click.command("logs")
@click.option("--node-index", "-i", type=int, default=0)
@click.option("--follow", "-f", is_flag=True, default=False)
@click.argument(
    "job_id",
    type=str,
)
@exit_on_http_error
def cmd_logs(
    node_index: int,
    follow: bool,
    job_id: str,
):
    print_job_logs(job_id, node_index, follow)
