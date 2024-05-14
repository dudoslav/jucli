from typing import Optional, TypeVar
from urllib.parse import urlparse, ParseResult
import asyncio
import functools as ft

def make_async(func):
    """
    Async command wrapper. Each command expects to run only once.
    """
    @ft.wraps(func)
    def _wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return _wrapper

def validate_url(ctx, param, value) -> Url:
    # TODO: Improve this validator
    return urlparse(value)


T = TypeVar('T')


def assert_value(optional: Optional[T], message: str) -> T:
    if not optional:
        raise ValueError(message)
    else:
        return optional
