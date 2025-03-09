
import asyncio
from collections.abc import Sequence
from csv import DictWriter
from pathlib import Path

from pokeapi.v2.base import PokeApiBaseType
from pokeapi.v2.client import PokeApiClient
from pokeapi_csv.specification import CsvSpecification

class PokeApiCsvWriter:

    def __init__(self, client: PokeApiClient, specification_types: Sequence[type[CsvSpecification[PokeApiBaseType]]]):
        self.client = client
        self.specification_types = specification_types

    async def write_to(self, path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        async with asyncio.TaskGroup() as tg:
            for specification_type in self.specification_types:
                specification = specification_type(self.client)
                tg.create_task(self._write_specification(specification, path))


    async def _write_specification[T: PokeApiBaseType](self, specification: CsvSpecification[T], path: Path) -> None:
        csv_path = path / f'{specification.name}.csv'
        with csv_path.open('w') as file:
            writer = DictWriter(file, fieldnames=specification.header_names)
            writer.writeheader()

            resource_list = await specification.resource_list(limit=10000)
            resource_tasks = [asyncio.create_task(resource.get(self.client))
                              for resource in resource_list.results]
            async with asyncio.TaskGroup() as tg:
                for task in resource_tasks:
                    resource = await task
                    row = await specification.to_row(resource)
                    writer.writerow(row)
                    tg.create_task(specification.process(path, resource))
