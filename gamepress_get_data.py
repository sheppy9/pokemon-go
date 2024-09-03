import ray
import json
import requests
import pandas as pd

from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlencode

data_root = 'data/gamepress'

headers = { 'User-Agent': 'Mozilla/5.0' }
Path(data_root).mkdir(parents=True, exist_ok=True)
gamepress_root = 'https://pokemongo.gamepress.gg'

def get_pokemons():
	params = { '_data': '_custom/routes/_site.c.pokemon+/_index' }
	res = requests.get(f'{gamepress_root}/c/pokemon?{urlencode(params)}', headers=headers)

	data_df = pd.DataFrame(res.json()['list']['listData']['docs'])
	data_df.to_json(f'{data_root}/pokemons.json', orient='records', indent=4)
	return data_df

@ray.remote
def get_pokemon_data(gamepass_pokemon_id):
	url = f'https://pokemongo.gamepress.gg/c/pokemon/{gamepass_pokemon_id}'

	headers = {
		'User-Agent': 'Mozilla/5.0',
		'Cookie': 'CH-prefers-color-scheme=dark; CH-time-zone=Asia%2FSingapore; toast-session=e30%3D.'
	}

	res = requests.get(url, headers=headers)
	if res.status_code != 200:
		return

	soup = BeautifulSoup(res.text)

	data = {
		'id': gamepass_pokemon_id,
		'evolutions': [],
		'fast_moves': [],
		'charge_moves': [],
		'weaknesses': [],
		'resistances': []
	}

	try:
		evolutions = soup.select('#family>div>div')
		for evolution in evolutions:
			data['evolutions'].append({
				'name': evolution.select_one('a>div:nth-child(1)>div>span').text,
				'url': evolution.select('a')[0]['href']
			})

		moves = soup.select('#moves:nth-child(1)>div')
		if len(moves) == 2:
			for move in moves[0]:
				cd_info, dps_info, eps_info = move.find_all('div')[3].find_all('button')
				data['fast_moves'].append({
					'name': move.select_one('div:nth-child(2)').text,
					'url': move.select_one('a')['href'],
					'cool_down': float(cd_info.text.replace('CD', '')),
					'damage_per_second': float(dps_info.text.replace('DPS', '')),
					'energy_per_second': float(eps_info.text.replace('EPS', '')),
					'power': int(move.find_all('button')[4].text)
				})

			for move in moves[1]:
				test = move.find_all('button')[1:5]
				cd_info, dps_info, dpe_info, dw_info = move.find_all('button')[1:5]
				data['charge_moves'].append({
					'name': move.select_one('div:nth-child(2)').text,
					'url': move.select_one('a')['href'],
					'cool_down': float(cd_info.text.replace('CD', '')),
					'damage_per_second': float(dps_info.text.replace('DPS', '')),
					'damage_per_energy': float(dpe_info.text.replace('DPE', '')),
					'dodge_window': float(dw_info.text.replace('DW', '')),
					'power': int(move.find_all('div')[-1].text)
				})

		tables = soup.find('div', { 'id': 'type-chart' }).find_all('table')
		if len(tables) == 2:
			types = ['weaknesses', 'resistances']

			for i, typee in enumerate(types):
				for entry in tables[i].find_all('td'):
					span_pair = entry.find_all('span')
					if len(span_pair) == 2:
						data[typee].append({
							'type': span_pair[0].text,
							'value': span_pair[1].text
						})

		with open(f'{data_root}/{gamepass_pokemon_id}.json', 'w') as json_file:
			json.dump(data, json_file, indent=4)

	except Exception as e:
		print(f'{gamepass_pokemon_id}: {e}')

	return data

pokemons = get_pokemons()
pokemon_ids = pokemons['id'].to_list()
results = ray.get([get_pokemon_data.remote(pokemon_id) for pokemon_id in pokemon_ids])
print(f'Completed, found {len(results)} data')
