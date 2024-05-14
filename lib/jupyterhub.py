import aiohttp
from lib.options import Options, Url


class JupyterHubClient:
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
            f"{self.options.endpoint.geturl()}/",
            headers = self.headers,
        ) as res:
            return await res.json()


    async def info(self):
        assert self.options.endpoint

        async with self.session.get(
            f"{self.options.endpoint.geturl()}/info",
            headers = self.headers,
        ) as res:
            return await res.json()


    async def start_server(self, user_name: str, data: str):
        assert self.options.endpoint

        async with self.session.post(
            f"{self.options.endpoint.geturl()}/users/{user_name}/server",
            headers = self.headers,
            data = data,
        ) as res:
            pass


    async def stop_server(self, user_name: str):
        assert self.options.endpoint

        async with self.session.delete(
            f"{self.options.endpoint.geturl()}/users/{user_name}/server",
            headers = self.headers,
        ) as res:
            pass
