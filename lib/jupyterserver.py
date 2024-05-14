import aiohttp
from lib.options import Options, Url


class JupyterServerClient:
    def __init__(self, options: Options):
        self.options = options
        self.headers = {
            "Authorization": f"token {self.options.token}"
        }


    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            raise_for_status = True,
        )
        return self


    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None


    async def version(self):
        assert self.options.endpoint

        async with self.session.get(
            f"{self.options.endpoint.geturl()}/api/",
            headers = self.headers,
        ) as res:
            return await res.json()

