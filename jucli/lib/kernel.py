from jucli.lib import JupyterServerClient
from jucli.lib.kernel_connection import KernelConnection
import logging


class Kernel:
    def __init__(self, client: JupyterServerClient):
        self.client = client

    async def __aenter__(self):
        res = await self.client.kernel_start(None, None)
        self.id = res['id']
        logging.debug(f"Kernel '{self.id}' started")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.kernel_stop(self.id)
        logging.debug(f"Kernel '{self.id}' stopped")

    def connect(self) -> KernelConnection:
        return KernelConnection(self, self)
