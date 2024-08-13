from pathlib import Path
import rich_click as click
from rich import print
import logging
import jucli.cli.utils as utils
import aiohttp


@click.group()
def cli():
    pass

@cli.group()
def hub():
    pass

@cli.command()
@utils.option_verbose
@utils.option_jupyterhub_endpoint
@utils.option_token
@utils.async_command
async def info(verbose: bool, endpoint: str, token: str):
    logging.debug("Command 'info' invoked")

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{endpoint}/info",
                headers={ "Authorization": f"token {token}" }) as response:
            print(response)

@hub.command()
@utils.option_verbose
@utils.option_jupyterhub_endpoint
@utils.option_token
@utils.async_command
async def version(verbose: bool, endpoint: str, token: str):
    logging.debug("Command 'version' invoked")

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{endpoint}/version",
                headers={ "Authorization": f"token {token}" }) as response:
            print(response)

@cli.command()
@utils.option_verbose
@utils.option_jupyterhub_endpoint
@utils.option_token
@utils.async_command
async def test(verbose: bool, endpoint: str, token, str):
    logging.debug("Command 'test' invoked")

    notebooks = Path(".").rglob("*.ipynb")
