from typing import TypeAlias, Optional, Any, Self, Literal, TypeVar
import click
from lib.options import Options, Url
from lib.jupyterhub import JupyterHubClient
from lib.jupyterserver import JupyterServerClient
import logging


@click.group()
@click.option(
    "--verbose",
    "-v",
    is_flag = True,
    envvar = "JUCLI_VERBOSE",
    default = False
)
@click.option(
    "--token",
    "-t",
    envvar = "JUCLI_JUPYTERHUB_TOKEN"
)
@click.pass_context
def cli(ctx, verbose: bool, token: str) -> None:
    """
    Set common options for the whole CLI
    """
    if (verbose):
        logging.basicConfig(level = logging.DEBUG)

    ctx.obj["options"] <<= Options(
        token = token
    )


@cli.group()
@click.option(
    "--endpoint",
    "-e",
    type = click.UNPROCESSED,
    callback = validate_url,
    envvar = "JUCLI_ENDPOINT",
)
@click.pass_context
def server(ctx, **kwargs):
    ctx.obj["options"] <<= Options(
        **kwargs,
    )


@server.command()
@click.pass_context
@make_async
async def sversion(ctx, endpoint) -> None:
    async with JupyterServerClient(ctx.obj["options"]) as client:
        click.echo(await client.version())
