
from collections.abc import Sequence
from pathlib import Path

from pokeapi.v2.models import Pokemon

from pokeapi_csv.specification import CsvSpecification, ResourceListCallable

class PokemonSpritesCsvSpecification(CsvSpecification[Pokemon]):

    @property
    def name(self) -> str:
        return "pokemon-sprites"

    @property
    def header_names(self) -> Sequence[str]:
        return ['pokemon_id', 'front_default']

    @property
    def resource_list(self) -> ResourceListCallable[Pokemon]:
        return self.client.pokemon_list

    async def to_row(self, pokemon: Pokemon) -> dict[str, str | int]:
        return {'pokemon_id': pokemon.id,
                'front_default': f'front_default/{pokemon.id}.png'}

    async def process(self, path: Path, pokemon: Pokemon) -> None:
        """Side-effectful processing for downloading other resources"""
        sprite_url = pokemon.sprites.front_default
        if not sprite_url:
            return
        png = path / 'front_default' / f'{pokemon.id}.png'
        png.parent.mkdir(parents=True, exist_ok=True)

        # TODO: Provide a way for pokeclient to get arbitrary content.
        async with self.client._session.get(sprite_url) as response:
            content = await response.read()
            with png.open('wb') as png_file:
                png_file.write(content)

