from typing import TypeAlias, Optional, Any, Self
from enum import Enum
from dataclasses import dataclass, field, asdict
from urllib.parse import urlparse, ParseResult

Url: TypeAlias = ParseResult


@dataclass
class Options:
    endpoint: Optional[Url] = field(default = None)
    token: Optional[str] = field(default = None)
    
    @staticmethod
    def default():
        return Options(
            endpoint = urlparse("https://localhost"),
        )

    # TODO: Somehow figure out how to type this
    def __lshift__(self: Self, other):
        result = asdict(self)

        for key, value in asdict(other).items():
            if value is not None:
                result[key] = value

        return self.__class__(**result)
