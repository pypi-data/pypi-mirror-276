import click

from komo import printing
from komo.cli.utils import exit_on_http_error
from komo.core import terminate_job


@click.command("terminate")
@click.argument(
    "job_id",
    type=str,
)
@exit_on_http_error
def cmd_terminate(job_id: str):
    terminate_job(job_id)
    printing.success(f"Job {job_id} is being terminated")
