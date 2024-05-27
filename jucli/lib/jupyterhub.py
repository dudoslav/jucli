import aiohttp

from jucli.lib.options import Options


# ENTER/EXIT start and stop server
class JupyterServerGuard:
    pass


class JupyterHubClient:
    def __init__(self, options: Options):
        self.options = options
        self.headers = {
            "Authorization": f"token {self.options.token}"
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
        assert self.options.jupyterhub_endpoint

        async with self.session.get(
                f"{self.options.jupyterhub_endpoint}/",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def info(self) -> dict:
        assert self.options.jupyterhub_endpoint

        async with self.session.get(
                f"{self.options.jupyterhub_endpoint}/info",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def server_info(self) -> dict:
        assert self.options.jupyterhub_endpoint
        assert self.options.user_id

        async with self.session.get(
                f"{self.options.jupyterhub_endpoint}/users/{self.options.user_id}",
                headers=self.headers,
        ) as res:
            return await res.json()

    async def server_start(self, data: str) -> None:
        assert self.options.jupyterhub_endpoint
        assert self.options.user_id

        async with self.session.post(
                f"{self.options.jupyterhub_endpoint}/users/{self.options.user_id}/server",
                headers=self.headers,
                data=data,
        ) as _:
            pass

    async def server_stop(self) -> None:
        assert self.options.jupyterhub_endpoint
        assert self.options.user_id

        async with self.session.delete(
                f"{self.options.jupyterhub_endpoint}/users/{self.options.user_id}/server",
                headers=self.headers,
        ) as _:
            pass
