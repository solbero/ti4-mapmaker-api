import contextlib
import itertools
from collections.abc import Sequence
from typing import Any, Union

from deta import Deta


@contextlib.asynccontextmanager
async def AsyncBase(engine: Deta, document: str):
    """Context manager for Deta Base Async."""
    async_base = engine.AsyncBase(document)
    try:
        yield async_base
    finally:
        await async_base.close()


def create_query(**kwargs: Union[Sequence[Any], None]) -> list[dict[str, Any]]:
    """Creates a Data Base query object from query parameters."""
    args = [[{key: value} for value in values] for key, values in kwargs.items() if values]
    products = itertools.product(*args)
    query = [{key: value for dict_ in product for key, value in dict_.items()} for product in products]
    return query
