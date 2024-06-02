import click

from komo.aws.connect import connect
from komo.cli.utils import exit_on_http_error


@click.command("connect")
@exit_on_http_error
def cmd_connect():
    connect()
