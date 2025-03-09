# pokeapi-csv

A small (work-in-progress) Python library to scrape data from [PokeAPI](https://pokeapi.co/)
and persist it to `.csv` files.

These can be subsequently loaded into analytical environments like [R](https://www.r-project.org/)
or [pandas](https://pandas.pydata.org/) where we can break down and and plot
this data.

## Usage

The recommended way to install and run this is through [uv](https://docs.astral.sh/uv/):

```
uv add git+https://github.com/AlexandreCarlton/pokeapi-csv.git
uv run pokeapi-csv --path <path-to-dump>
```

This will:

 - start up [pokeapi-dump](https://github.com/AlexandreCarlton/pokeapi-dump/)
   listening by default on `:8080`.
 - scrape the data using [pokeapi-py](https://github.com/AlexandreCarlton/pokeapi-py/).
 - persist the data as `.csv` files in the provided `path-to-dump`.
