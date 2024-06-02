import click

from komo.cli.utils import exit_on_http_error
from komo.lambda_labs.connect import connect


@click.command("connect")
@exit_on_http_error
def cmd_connect():
    api_key = click.prompt("Please enter your Lambda Labs API Key")
    connect(api_key)
