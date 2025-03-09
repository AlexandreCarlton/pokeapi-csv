from collections.abc import Sequence

from pokeapi.v2.models import PokemonSpecies

from pokeapi_csv.specification import CsvSpecification, ResourceListCallable

class PokemonSpeciesCsvSpecification(CsvSpecification[PokemonSpecies]):

    @property
    def name(self) -> str:
        return 'pokemon-species'

    @property
    def header_names(self) -> Sequence[str]:
        return ['pokemon_species_id', 'capture_rate', 'color']

    @property
    def resource_list(self) -> ResourceListCallable[PokemonSpecies]:
        return self.client.pokemon_species_list

    async def to_row(self, species: PokemonSpecies) -> dict[str, str | int]:
        species_color = await species.color.get(self.client)
        return {'pokemon_species_id': species.id,
                'capture_rate': species.capture_rate,
                'color': species_color.id}

