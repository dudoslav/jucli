from dataclasses import dataclass, field, asdict
from typing import TypeAlias, Optional, Any
import logging


@dataclass
class Options:
    jupyterhub_endpoint: Optional[str] = field(default=None)
    jupyterserver_endpoint: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)
    log_level: Optional[Any] = field(default=None)  # How to type this?
    commands: Optional[list[str]] = field(default=None)
    user_id: Optional[str] = field(default=None)

    @staticmethod
    def default():
        return Options(
            jupyterhub_endpoint="https://localhost",
            jupyterserver_endpoint="https://localhost",
            log_level=logging.INFO,
        )

    # TODO: Somehow figure out how to type this
    def __lshift__(self, other):
        result = asdict(self)

        for key, value in asdict(other).items():
            if value is not None:
                result[key] = value

        return self.__class__(**result)
