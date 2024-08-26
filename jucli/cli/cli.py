from pathlib import Path
import rich_click as click
from rich import print
from rich.console import Console
from rich.syntax import Syntax
import logging
import jucli.cli.utils as utils
import aiohttp
import json

from jucli.lib.jupyter import create_server, create_kernel, make_execute_request

@click.group()
def cli():
    pass

@cli.group()
def hub():
    pass

@hub.command()
@utils.option_verbose
@utils.option_jupyterhub_endpoint
@utils.option_token
@utils.async_command
async def info(verbose: bool, endpoint: str, token: str):
    logging.debug("Command 'info' invoked")

    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{endpoint}/hub/api/info",
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
                f"{endpoint}/hub/api/version",
                headers={ "Authorization": f"token {token}" }) as response:
            print(response)

async def on_request_start(session, context, params):
    logging.getLogger('aiohttp.client').debug(f'Starting request <{params}>')

@cli.command()
@utils.option_verbose
@utils.option_jupyterhub_endpoint
@utils.option_jupyterhub_user_id
@utils.option_jupyterhub_data
@utils.option_token
@utils.argument_path
@utils.async_command
async def test(
        verbose: bool, endpoint: str, token: str,
        user_id: str, data: str, path: Path):
    console = Console()
    logging.debug("Command 'test' invoked")

    # TODO: Implement jucli.json/yaml that specifies servers and notebooks

    # Search for runnable notebooks
    notebooks = list(Path(path).rglob("*.ipynb"))
    if len(notebooks) == 0:
        console.log("No notebooks found, exiting")
        return

    # TODO: Generate test plan
    # > Select kernel type
    # > Select server type (optional)

    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)

    async with aiohttp.ClientSession(
            trace_configs=[trace_config],
            # raise_for_status=True,
            headers={ "Authorization": f"token {token}" }) as session:
        async with create_server(session, endpoint, user_id, data):
            with console.status("[bold green]Running notebooks...") as status:
                for notebook in notebooks:
                    console.log(f"Running notebook: {notebook}")
                    with open(notebook, "r") as file:
                        notebook_json = json.loads(file.read())

                    kernelspec = notebook_json["metadata"]["kernelspec"]
                    console.log(f"Requested kernel: {kernelspec['name']}")
                    async with create_kernel(session, endpoint, user_id, { "name": kernelspec["name"] }) as kernel_json:
                        kernel_id = kernel_json["id"]
                        async with session.ws_connect(
                                f"{endpoint}/user/{user_id}/api/kernels/{kernel_id}/channels",
                        ) as connection:
                            for cell in notebook_json["cells"]:
                                match cell["cell_type"]:
                                    case "code":
                                        if len(cell["source"]) == 0:
                                            logging.warning(f"Notebook '{notebook}' has empty source cell")
                                            continue
                                        console.log(Syntax("".join(cell["source"]), kernelspec["language"]))
                                        await connection.send_str(json.dumps(make_execute_request(cell["source"])))
                                        # TODO: Move this to function
                                        stop = False
                                        async for response in connection:
                                            response_json = response.json()
                                            logging.debug(f"Incoming kernel message: {response_json}")
                                            match response_json["msg_type"]:
                                                case "error":
                                                    logging.error(response_json["content"])
                                                    stop = True
                                                    break
                                                case "execute_result":
                                                    console.log(response_json["content"])
                                                case "execute_reply":
                                                    stop = True
                                                    break
                                                case _:
                                                    logging.warning(f"Unhandled response message type '{response_json['msg_type']}'")
                                        if stop:
                                            break
                                    case _:
                                        continue