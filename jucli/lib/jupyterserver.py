from __future__ import annotations
import aiohttp
from typing import Optional
import logging

from jucli.lib.options import Options


class JupyterServerClient:
    class Kernel:
        class Connection:
            def __init__(self, kernel: JupyterServerClient.Kernel, client: JupyterServerClient):
                self.kernel = kernel
                self.client = client
                logging.debug(f"Connection initialized")

            async def __aenter__(self):
                self.conn = await self.client.session.ws_connect(
                    f"{self.client.options.jupyterserver_endpoint}/kernels/{self.kernel.id}/channels",
                    headers=self.client.headers
                )
                logging.debug(f"Connection with kernel \"{self.kernel.id}\" established")
                return self

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                await self.conn.close()
                self.conn = None
                logging.debug(f"Connection with kernel \"{self.kernel.id}\" closed")

        def __init__(self, client: JupyterServerClient):
            self.client = client
            logging.debug("Kernel initialized")

        async def __aenter__(self):
            res = await self.client.kernel_start(None, None)
            self.id = res['id']
            logging.debug(f"Kernel \"{self.id}\" created")
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            await self.client.kernel_stop(self.id)
            logging.debug(f"Kernel \"{self.id}\" stopped")

        def connect(self) -> JupyterServerClient.Kernel.Connection:
            return JupyterServerClient.Kernel.Connection(self, self.client)


    def __init__(self, options: Options):
        self.options = options
        self.headers = {
            "Authorization": f"token {self.options.token}"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    async def version(self):
        assert self.options.jupyterserver_endpoint

        async with self.session.get(
                f"{self.options.jupyterserver_endpoint}",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def kernel_start(self, name: Optional[str], path: Optional[str]) -> dict:
        assert self.options.jupyterserver_endpoint

        data = {}
        if name is not None:
            data['name'] = name

        if path is not None:
            data['path'] = path

        async with self.session.post(
                f"{self.options.jupyterserver_endpoint}/kernels",
                headers=self.headers,
                data=data
        ) as res:
            return await res.json()

    async def kernel_stop(self, id: str):
        assert self.options.jupyterserver_endpoint

        async with self.session.delete(
                f"{self.options.jupyterserver_endpoint}/kernels/{id}",
                headers=self.headers,
        ) as _:
            pass

    async def kernel_connect(self, id: str):
        assert self.options.jupyterserver_endpoint

        # return JupyterServerClient.Kernel()
