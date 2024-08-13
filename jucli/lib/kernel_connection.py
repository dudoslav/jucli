from jucli.lib.kernel import Kernel
import logging


class KernelConnection:
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        logging.debug("Kernel connection created")

    async def __aenter__(self):
        self.conn = await self.kernel.client.session.ws_connect(
            f"{self.kernel.client.endpoint}/kernels/{self.kernel.id}/channels",
            headers=self.client.headers
        )
        logging.debug(f"Connection with kernel '{self.kernel.id}' started")
        return self

    async def __aexit__(self, *err):
        await self.conn.close()
        self.conn = None
        logging.debug(f"Connection with kernel '{self.kernel.id}' stopped")
