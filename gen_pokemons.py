import csv
import json
import pandas as pd

from glob import glob

def get_gamepress_pokemons():
	pokemons = {}
	for jfile in glob(f'data/gamepress/pokemons/*.json'):
		pokemon = json.loads(open(jfile).read())
		pokemon['joined_evolutions'] = ', '.join([_['name'] for _ in pokemon['evolutions']])
		pokemon['joined_weaknesses'] = ', '.join([_['type'] for _ in pokemon['weaknesses']])
		pokemon['joined_resistances'] = ', '.join([_['type'] for _ in pokemon['resistances']])
		pokemon['joined_fast_moves'] = ', '.join([_['name'] for _ in pokemon['fast_moves']])
		pokemon['joined_charge_moves'] = ', '.join([_['name'] for _ in pokemon['charge_moves']])
		pokemons[pokemon['id'].lower()] = pokemon
	return pokemons

def get_pvpoke_pokemons():
	# Downloaded CSV from https://pvpoke.com/rankings/all/10000/overall/
	pokemons = {}
	for i, pokemon in enumerate(csv.DictReader(open('data/csv/pvpoke_master_league.csv'))):
		pokemon['rank'] = i + 1
		pokemons[pokemon['Pokemon'].lower()] = pokemon
	return pokemons

def joined_data(dict_1, dict_2):
	# dict_1 should always be the one having more data
	if len(dict_1) < len(dict_2):
		dict_1, dict_2 = dict_2, dict_1

	for key, value in dict_1.items():
		dict_2_value = dict_2.get(key)
		if dict_2_value is not None:
			value.update(dict_2_value)
	return dict_1

def generate_interested_data(pokemons):
	data = []
	for name, pokemon in pokemons.items():
		data.append({
			'Rank': pokemon.get('rank'),
			'Name': name,
			# 'Types': pokemon.get('types'),
			'Evolutions': pokemon.get('joined_evolutions'),
			'Weaknesses': pokemon.get('joined_weaknesses'),
			'Resistances': pokemon.get('joined_resistances'),
			# 'Attack': pokemon.get('Attack'),
			# 'Defense': pokemon.get('Defense'),
			# 'Stamina': pokemon.get('Stamina'),
			'Fast Moves': pokemon.get('joined_fast_moves'),
			'Charge Moves': pokemon.get('joined_charge_moves'),
			'CP': pokemon.get('CP'),
		})
	return data

gamepress_pokemons = get_gamepress_pokemons()
# print(f'Gamepress pokemons: {len(gamepress_pokemons)}')

pvpoke_pokemons = get_pvpoke_pokemons()
# print(f'PVPoke pokemons: {len(pvpoke_pokemons)}')

joined_pokemons = joined_data(gamepress_pokemons, pvpoke_pokemons)
# print(f'Joined pokemons: {len(joined_pokemons)}')

interested_data = generate_interested_data(joined_pokemons)

df = pd.DataFrame(interested_data)
df.to_json(f'data/json/pokemon.json', orient='records')
print('Generate pokemon completed')

# print('Gamepress', '#' * 100)
# print(gamepress_pokemons.get('goodra'))
# print('PVPoke', '#' * 100)
# print(pvpoke_pokemons.get('goodra'))
# print('Joined', '#' * 100)
# print(joined_pokemons.get('goodra'))
# print('#' * 100)

# pokemons = []
# pvpoke_pokemons = csv.DictReader(open('data/csv/pvpoke_master_league.csv'))
# for i, pvpoke_pokemon in enumerate(pvpoke_pokemons):
# 	name = pvpoke_pokemon['Pokemon']
# 	
# 	types = [pvpoke_pokemon['Type 1'].capitalize()]
# 	type_2 = pvpoke_pokemon['Type 2']
# 	if type_2 is not None:
# 		types.append(type_2.capitalize())
# 
# 	pokemons.append({
# 		'Rank': i + 1,
# 		'Name': name,
# 		'Types': types,
# 		'CP': pvpoke_pokemon['CP']
# 	})
# 
# 	gamepress_data = gamepress_pokemons.get(name)
# 	if gamepress_data is not None:
# 		print(gamepress_data)
# 		break
# print(f'pvpoke pokemons: {len(pokemons)}')


# data_root = 'data'
# pokemon_root = f'{data_root}/gamepress'
# 
# csv_data = []
# for file in glob(f'{pokemon_root}/*.json'):
# 	data = json.load(open(file))
# 	print(data)
# 	csv_data.append({
# 		'Name': data['name'],
# 		'Types': ', '.join(sorted(data['types'])),
# 		'Evolution': ', '.join([_['name'] for _ in data['evolutions']]),
# 		'Weaknesses': ', '.join(sorted([_['type'] for _ in data['weaknesses']])),
# 		'Resistances': ', '.join(sorted([_['type'] for _ in data['resistances']])),
# 		'Attack': data['attack'],
# 		'Defense': data['defense'],
# 		'Stamina': data['stamina'],
# 	})

# print(csv_data[0])
# df = pd.DataFrame(csv_data)
# df.to_json(f'{data_root}/json/pokemon.json', orient='records')
# print('Generate pokemon completed')
