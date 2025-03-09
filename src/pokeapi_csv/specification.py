from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from pokeapi.v2.base import PokeApiBaseType
from pokeapi.v2.client import PokeApiClient
from pokeapi.v2.resource import NamedApiResourceList


class ResourceListCallable[T: PokeApiBaseType](Protocol):
    """
    Represents a call to a resource list.
    See PokeApiClient.pokemon_list as an example.
    """
    async def __call__(self, limit: int | None=None, offset: int | None=None) -> NamedApiResourceList[T]: ...


class CsvSpecification[T: PokeApiBaseType](ABC):
    """The base class which other "specifications" should inherit to generate
    .csv file for further analysis."""

    def __init__(self, client: PokeApiClient):
        self.client = client


    @abstractproperty
    def name(self) -> str:
        """The basename (sans .csv extension) of the CSV file."""
        pass

    @abstractproperty
    def header_names(self) -> Sequence[str]:
        """The header names of the CSV file."""
        pass

    @abstractproperty
    def resource_list(self) -> ResourceListCallable[T]:
        """A function that returns resource list that will be fed into the writer"""
        pass

    @abstractmethod
    async def to_row(self, type_: T) -> dict[str, str | int]:
        """Converts an individual model to a CSV row representation."""
        pass

    async def process(self, path: Path, type_: T) -> None:
        """Side-effectful processing for downloading other resources"""
        pass
