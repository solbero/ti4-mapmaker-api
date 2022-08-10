import contextlib

from deta import Deta


@contextlib.asynccontextmanager
async def AsyncBase(engine: Deta, document: str):
    """Context manager for Deta Base Async."""
    async_base = engine.AsyncBase(document)
    try:
        yield async_base
    finally:
        await async_base.close()
