
import argparse
import asyncio
from pathlib import Path

from pokeapi.v2.client import PokeApiClient
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

from pokeapi_csv.specifications.pokemon import PokemonCsvSpecification
from pokeapi_csv.specifications.pokemon_species import PokemonSpeciesCsvSpecification
from pokeapi_csv.specifications.pokemon_sprites import PokemonSpritesCsvSpecification
from pokeapi_csv.writer import PokeApiCsvWriter


IMAGE = 'docker.io/alexandrecarlton/pokeapi-dump:sha-aff23d7'

SPECIFICATION_TYPES = (
    PokemonCsvSpecification,
    PokemonSpeciesCsvSpecification,
    PokemonSpritesCsvSpecification
)


async def _main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, type=Path)
    parser.add_argument('--port', default=8080, type=int)
    args = parser.parse_args()

    endpoint = f'http://localhost:{args.port}'
    pokeapi_container = (DockerContainer(IMAGE)
                         .with_env('ENDPOINT', endpoint)
                         .with_bind_ports(80, args.port))

    with pokeapi_container as pokeapi:
        wait_for_logs(pokeapi, 'Configuration complete; ready for start up')

        async with PokeApiClient(endpoint=endpoint) as pokeapi_client:
            writer = PokeApiCsvWriter(pokeapi_client, SPECIFICATION_TYPES)
            await writer.write_to(args.path)

def main() -> None:
    asyncio.run(_main())
