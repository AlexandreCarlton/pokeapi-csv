from collections.abc import Sequence

from pokeapi.v2.models import Pokemon

from pokeapi_csv.specification import CsvSpecification, ResourceListCallable

class PokemonCsvSpecification(CsvSpecification[Pokemon]):

    @property
    def name(self) -> str:
        return "pokemon_v2"

    @property
    def header_names(self) -> Sequence[str]:
        return ['pokemon_id', 'name', 'height', 'weight', 'pokemon_species_id']

    @property
    def resource_list(self) -> ResourceListCallable[Pokemon]:
        return self.client.pokemon_list

    async def to_row(self, pokemon: Pokemon) -> dict[str, str | int]:
        pokemon_species = await pokemon.species.get(self.client)
        return {'pokemon_id': pokemon.id,
                'pokemon_species_id': pokemon_species.id,
                'name': pokemon.name,
                'height': pokemon.height,
                'weight': pokemon.weight}
