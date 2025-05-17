import json
import requests

from pathlib import Path
from datetime import datetime
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor

headers = { 'User-Agent': 'Mozilla/5.0' }
Path('data/gamepress/pokemons').mkdir(parents=True, exist_ok=True)
gamepress_root = 'https://pokemongo.gamepress.gg'

def get_pokemons():
	pokemon_filename = Path(f'data/gamepress/pokemons.json')
	params = { '_data': '_custom/routes/_site.c.pokemon+/_index' }
	res = requests.get(f'{gamepress_root}/c/pokemon?{urlencode(params)}', headers=headers)

	if res.status_code != 200:
		return res

	data = res.json().get('list', {}).get('listData', {}).get('docs')
	with open(pokemon_filename, 'w') as json_file:
		json.dump(data, json_file)

	return data

def get_pokemon_data(gamepass_pokemon_id):
	pokemon_dir = Path(f'data/gamepress/pokemons/')
	pokemon_dir.mkdir(parents=True, exist_ok=True)
	json_filename = pokemon_dir / f'{gamepass_pokemon_id}.json'

	url = f'https://pokemongo.gamepress.gg/c/pokemon/{gamepass_pokemon_id}?_data=_custom%2Froutes%2F_site.c.pokemon%2B%2F%24entryId'
	res = requests.get(url)

	if res.status_code != 200:
		return res

	data = res.json()
	with open(json_filename, 'w') as json_file:
		json.dump(data, json_file)

	return data

start = datetime.now()
pokemons = get_pokemons()

pokemon_details = []
with ThreadPoolExecutor() as executor:
	for pokemon in pokemons:
		pokemon_id = pokemon.get('id')
		if pokemon_id is None:
			print(f'id not found. {pokemon}')
			continue

		pokemon_details.append(executor.submit(get_pokemon_data, pokemon_id))

print(f'Process started: {start:%d %b %Y %H:%M:%S}, took {datetime.now() - start}. found {len(pokemon_details)} records')