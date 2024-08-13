import aiohttp
import logging
from jucli.lib.kernel import Kernel


class JupyterServerClient:
    """
    Class wrapping Jupyter Server functionality
    """
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"token {token}"
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    async def version(self) -> dict:
        async with self.session.get(
                f"{self.endpoint}",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def kernel_start(self, name: Optional[str], path: Optional[str]) -> dict:
        data = {}
        if name is not None:
            data['name'] = name

        if path is not None:
            data['path'] = path

        async with self.session.post(
                f"{self.endpoint}/kernels",
                headers=self.headers,
                data=data
        ) as res:
            return await res.json()

    async def kernel_stop(self, id: str):
        async with self.session.delete(
                f"{self.endpoint}/kernels/{id}",
                headers=self.headers,
        ) as _:
            pass

    async def kernel_connect(self):
        return Kernel(self)
