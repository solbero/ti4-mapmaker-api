import asyncio
import itertools
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any, Optional, Union

import deta

Data = Union[Mapping, Sequence, str, int, float, bool, None]
Record = Mapping[str, Data]


class AsyncBase:
    """Facade class for Deta.AsyncBase."""

    def __init__(self, engine: deta.Deta, document: str) -> None:
        self.db = engine.AsyncBase(document)
        self._batch_size = 25

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def put(self, data: Record, key: Optional[str] = None) -> Union[Record, None]:
        """Put a record into the database document."""
        return await self.db.put(data, key)  # type: ignore comment

    async def put_many(self, items: Sequence[Record]) -> defaultdict[str, list[Record]]:
        """Put many records into the database document."""
        results = defaultdict(list)
        slices = (slice(index, index + self._batch_size) for index in range(0, len(items), self._batch_size))

        tasks = (self.db.put_many(items[slice]) for slice in slices)  # type: ignore comment
        responses = await asyncio.gather(*tasks)

        for response in responses:
            if "processed" in response:
                results["processed"] += response["processed"]["items"]
            if "failed" in response:
                results["failed"] += response["failed"]["items"]

        return results

    async def get(self, key: str) -> Union[Record, None]:
        """Get a record by its key from the database document."""
        return await self.db.get(key)

    async def fetch(self, query: Optional[Sequence[Record]] = None) -> list[Record]:
        response = await self.db.fetch(query)  # type: ignore comment
        records: list[Record] = response.items

        while response.last:
            response = await self.db.fetch(last=response.last)
            records += response.items

        return records

    async def delete(self, key: str) -> None:
        """Delete a record by its key from the database document."""
        return await self.db.delete(key)

    async def delete_all(self) -> None:
        """Delete all records in the database document."""

        response = await self.fetch()
        tasks = (self.delete(record["key"]) for record in response)  # type: ignore comment

        await asyncio.gather(*tasks)

    async def close(self):
        """Close the connection to the database."""
        await self.db.close()


def create_query(**kwargs: Union[Sequence[Any], None]) -> list[dict[str, Any]]:
    """Creates a Data Base query object from query parameters."""
    args = [[{key: value} for value in values] for key, values in kwargs.items() if values]
    products = itertools.product(*args)
    query = [{key: value for dict_ in product for key, value in dict_.items()} for product in products]
    return query
