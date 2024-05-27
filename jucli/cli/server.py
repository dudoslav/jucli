import click

from lib.cli_utils import make_async, validate_url
from lib.jupyterserver import JupyterServerClient
from lib.options import Options


@click.group()
@click.option(
    "--endpoint",
    "-e",
    type=click.UNPROCESSED,
    callback=validate_url,
    envvar="JUCLI_ENDPOINT",
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
