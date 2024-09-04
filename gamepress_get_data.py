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
	pokemon_filename = Path(f'{data_root}/pokemons.json')
	if pokemon_filename.exists():
		print('Loading pokemon from file')
		return pd.read_json(pokemon_filename)

	params = { '_data': '_custom/routes/_site.c.pokemon+/_index' }
	res = requests.get(f'{gamepress_root}/c/pokemon?{urlencode(params)}', headers=headers)

	data_df = pd.DataFrame(res.json()['list']['listData']['docs'])
	data_df.to_json(pokemon_filename, orient='records', indent=4)
	return data_df

@ray.remote
def get_pokemon_data(gamepass_pokemon_id):
	json_filename = Path(f'{data_root}/pokemon/{gamepass_pokemon_id}.json')
	if json_filename.exists():
		print(f'Loading pokemon data from file')
		json_file = open(json_filename)
		data = json.load(json_file)
		json_file.close()
		return data

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
		'id': soup.select_one('#main>div>section>div>div>div>span:nth-child(2)').text,
    	'name': soup.find('h1').text,
		'gamepass_pokemon_id': gamepass_pokemon_id,
		'evolutions': [],
		'fast_moves': [],
		'charge_moves': [],
		'weaknesses': [],
		'resistances': []
	}

	pokemon_stats = soup.select_one('#main>div>section').find_all('div')[6].select('div')
	attack, defense, stamina = pokemon_stats[1].text, pokemon_stats[4].text, pokemon_stats[7].text

	try:
		attack = int(attack)
	except ValueError:
		pass
	try:
		defense = int(defense)
	except ValueError:
		pass
	try:
		stamina = int(stamina)
	except ValueError:
		pass

	data['attack'] = attack
	data['defense'] = defense
	data['stamina'] = stamina

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

				cooldown = cd_info.text.replace('CD', '')
				damage_per_second = dps_info.text.replace('DPS', '')
				energy_per_second = eps_info.text.replace('EPS', '')
				power = move.find_all('button')[4].text

				try:
					cooldown = float(cooldown)
				except ValueError:
					pass
				try:
					damage_per_second = float(damage_per_second)
				except ValueError:
					pass
				try:
					energy_per_second = float(energy_per_second)
				except ValueError:
					pass
				try:
					power = int(power)
				except ValueError:
					pass

				data['fast_moves'].append({
					'name': move.select_one('div:nth-child(2)').text,
					'url': move.select_one('a')['href'],
					'cool_down': cooldown,
					'damage_per_second': damage_per_second,
					'energy_per_second': energy_per_second,
					'power': power
				})

			for move in moves[1]:
				test = move.find_all('button')[1:5]
				cd_info, dps_info, dpe_info, dw_info = move.find_all('button')[1:5]

				cooldown = cd_info.text.replace('CD', '')
				damage_per_second = dps_info.text.replace('DPS', '')
				damage_per_energy = dpe_info.text.replace('DPE', '')
				dodge_window = dw_info.text.replace('DW', '')
				power = move.find_all('div')[-1].text

				try:
					cooldown = float(cooldown)
				except ValueError:
					pass
				try:
					damage_per_second = float(damage_per_second)
				except ValueError:
					pass
				try:
					damage_per_energy = float(damage_per_energy)
				except ValueError:
					pass
				try:
					dodge_window = float(dodge_window)
				except ValueError:
					pass
				try:
					power = int(power)
				except ValueError:
					pass

				data['charge_moves'].append({
					'name': move.select_one('div:nth-child(2)').text,
					'url': move.select_one('a')['href'],
					'cool_down': cooldown,
					'damage_per_second': damage_per_second,
					'damage_per_energy': damage_per_energy,
					'dodge_window': dodge_window,
					'power': power
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

		with open(json_filename, 'w') as json_file:
			json.dump(data, json_file, indent=4)

	except Exception as e:
		print(f'{gamepass_pokemon_id}: {e}')

	return data

pokemons = get_pokemons()
pokemon_ids = pokemons['id'].to_list()
results = ray.get([get_pokemon_data.remote(pokemon_id) for pokemon_id in pokemon_ids])
print(f'Completed, found {len(results)} data')
