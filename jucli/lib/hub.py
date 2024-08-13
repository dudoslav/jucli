import aiohttp
from jucli.lib import JupyterServerClient


class JupyterHubClient:
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"token {token}"
        }

    async def __aenter__(self):
        # TODO: Raise but also parse body if possible!
        self.session = aiohttp.ClientSession(
            raise_for_status=True,
        )
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    async def version(self) -> dict:
        async with self.session.get(
                f"{self.endpoint}/",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def info(self) -> dict:
        async with self.session.get(
                f"{self.endpoint}/info",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def server_info(self, user_id: str) -> dict:
        async with self.session.get(
                f"{self.endpoint}/users/{user_id}",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def server_start(self, user_id: str, data: str) -> None:
        async with self.session.post(
                f"{self.endpoint}/users/{user_id}/server",
                headers=self.headers,
                data=data,
        ) as _:
            pass

    async def server_stop(self, user_id: str) -> None:
        async with self.session.delete(
                f"{self.endpoint}/users/{user_id}/server",
                headers=self.headers,
        ) as _:
            pass