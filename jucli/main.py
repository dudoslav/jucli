import logging
from pathlib import Path
import json
import asyncio
from rich.logging import RichHandler
from rich import print

import jucli.lib.cli.cli as cli
from jucli.lib.options import Options
from jucli.lib.jupyterhub import JupyterHubClient
from jucli.lib.jupyterserver import JupyterServerClient

# TODO: Move this to utils or use some kind of json pointer/path lib
from functools import reduce


def deref_multi(data, keys):
    return reduce(lambda d, key: d[key], keys, data)


# def notebook_execute(notebook: dict, connection: KernelConnection) -> bool:
#     pass


async def jucli(options: Options) -> None:
    # TODO: These commands are not in CLI help
    match options.commands:
        case ['server'] | ['server', 'version']:
            async with JupyterServerClient(options) as client:
                print(await client.version())
        case ['server', 'execute']:
            with open('/home/dudoslav/Downloads/notebook.ipynb') as file:
                notebook = json.load(file)

            async with JupyterServerClient(options) as client:
                async with JupyterServerClient.Kernel(client) as kernel:
                    async with JupyterServerClient.Kernel.Connection(kernel, client) as conn:
                        logging.debug(f"Sending: {json.dumps(notebook['cells'][0]['source'])}")
                        await conn.conn.send_str(json.dumps(notebook['cells'][0]['source']))
                        logging.debug('send')
                        result = await conn.conn.receive()
                        logging.debug('received')
                        print(result)
                print(await client.version())
        case ['hub'] | ['hub', 'info']:
            async with JupyterHubClient(options) as client:
                print(await client.info())
        case ['hub', 'version']:
            async with JupyterHubClient(options) as client:
                print(await client.version())
        case ['hub', 'server', 'query', *path_arg]:
            path = path_arg[0] if len(path_arg) > 0 else ''

            async with JupyterHubClient(options) as client:
                info = await client.server_info()
                print(deref_multi(info, path.split('.')))
        case ['hub', 'server'] | ['hub', 'server', 'info']:
            async with JupyterHubClient(options) as client:
                print(await client.server_info())
        case ['hub', 'server', 'start', *data_arg]:
            data = data_arg[0] if len(data_arg) > 0 else None
            # ^ I don't know how to make data optional here
            logging.debug(f'Start server with extra data: "{data}"')
            async with JupyterHubClient(options) as client:
                await client.server_start(data)
        case ['hub', 'server', 'poll_ready', *timeout_arg]:
            timeout = int(timeout_arg[0]) if len(timeout_arg) > 0 else 60
            # ^ Same as before but also make default configurable
            try:
                async with asyncio.timeout(timeout):
                    async with JupyterHubClient(options) as client:
                        try:
                            while not (await client.server_info())['servers']['']['ready']:
                                await asyncio.sleep(1)  # TODO: Make this interval configurable
                        except KeyError:
                            print('Cannot query ready state, is the server started?')
                            exit(1)
            except TimeoutError:
                print(f'Poll ready failed after {timeout} seconds')
                exit(1)
            print(f'Server for user "{options.user_id}" is ready')
        case ['hub', 'server', 'stop']:
            async with JupyterHubClient(options) as client:
                await client.server_stop()
            print(f'Server for user "{options.user_id}" stopped')
        case _:
            print(f'Unrecognized command/s: {options.commands}')


def main():
    options = Options.default()

    # Load config
    config_path = Path().home() / '.juclirc.json'
    if config_path.is_file():
        with open(config_path) as file:
            config = json.load(file)
            options <<= Options(**config)

    # Get from environment variables
    # TODO: ^

    # Parse command line arguments
    options <<= cli.parse()

    FORMAT = "%(message)s"
    logging.basicConfig(level=options.log_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

    logging.debug(f'Options: {options}')
    asyncio.run(jucli(options))


if __name__ == '__main__':
    main()
