import rich_click as click
from rich.logging import RichHandler
import functools as ft
import asyncio
import logging
from typing import Callable


def async_command(fn: Callable) -> Callable:
    """
    Decorator that immediately calls async function in asyncio.run
    :param fn: Callable async function
    :return: Callable
    """
    @ft.wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))
    return wrapper


def option_verbose(fn: Callable) -> Callable:
    """
    Common option enabling verbosity
    :param fn: Callable function
    :return: Callable function (decorated)
    """
    def callback(_, __: str, value: bool):
        if value:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                datefmt="[%X]",
                handlers=[RichHandler()],
            )
        return value
    return click.option(
        "-v",
        "--verbose",
        is_flag=True,
        envvar="JUCLI_VERBOSE",
        help="Enable verbosity",
        callback=callback,
    )(fn)


option_jupyterhub_endpoint = click.option(
    "-e",
    "--endpoint",
    envvar="JUCLI_JUPYTERHUB_ENDPOINT",
    help="JupyterHub API endpoint",
)


option_jupyterserver_endpoint = click.option(
    "-e",
    "--endpoint",
    envvar="JUCLI_JUPYTERSERVER_ENDPOINT",
    help="JupyterServer API endpoint",
)


option_token = click.option(
    "-t",
    "--token",
    envvar="JUCLI_TOKEN",
    help="JupyterHub/Server token",
)
