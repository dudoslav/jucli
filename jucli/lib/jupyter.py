import logging
from contextlib import asynccontextmanager
import datetime
import uuid
import json

@asynccontextmanager
async def create_server(session, endpoint, user_id, data):
    logging.debug("Starting jupyter server")
    await session.post(
        f"{endpoint}/hub/api/users/{user_id}/server",
        data=data,
    )
    logging.debug("Jupyter server started")

    try:
        yield
    finally:
        logging.debug("Stopping jupyter server")
        await session.delete(f"{endpoint}/hub/api/users/{user_id}/server")
        logging.debug("Jupyter server stopped")


@asynccontextmanager
async def create_kernel(session, endpoint, user_id, data):
    logging.debug("Creating jupyter kernel")
    async with session.post(
            f"{endpoint}/user/{user_id}/api/kernels",
            data=json.dumps(data),
    ) as response:
        response_json = await response.json()
        kernel_id = response_json["id"]
    logging.debug("Jupyter kernel created")

    try:
        yield response_json
    finally:
        logging.debug("Deleting jupyter kernel")
        await session.delete(f"{endpoint}/user/{user_id}/api/kernels/{kernel_id}")
        logging.debug("Jupyter kernel deleted")


def make_execute_request(code: str) -> dict:
    return {
        "header": {
            "msg_id": uuid.uuid1().hex,
            "username": "jucli",
            "session": uuid.uuid1().hex,
            "data": datetime.datetime.now().isoformat(),
            "msg_type": "execute_request",
            "version": "5.0",
        },
        "metadata": {
        },
        "content": {
            "code": code,
            "silent": False,
        }
    }
