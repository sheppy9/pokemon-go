import csv
import json
import pandas as pd

from glob import glob

def get_gamepress_pokemons():
	pokemons = {}
	for jfile in glob(f'data/gamepress/pokemons/*.json'):
		pokemon = json.loads(open(jfile).read())
		name = pokemon.get('name')

		pokemon['joined_evolutions'] = ', '.join([_['name'] for _ in pokemon['evolutions']])
		pokemon['joined_weaknesses'] = ', '.join([_['type'] for _ in pokemon['weaknesses']])
		pokemon['joined_resistances'] = ', '.join([_['type'] for _ in pokemon['resistances']])
		pokemon['joined_fast_moves'] = ', '.join([_['name'] for _ in pokemon['fast_moves']])
		pokemon['joined_charge_moves'] = ', '.join([_['name'] for _ in pokemon['charge_moves']])

		if name is not None:
			pokemons[name.lower()] = pokemon
		else:
			pokemons[pokemon['id'].lower()] = pokemon
	return pokemons

def get_pvpoke_pokemons():
	# Downloaded CSV from https://pvpoke.com/rankings/all/10000/overall/
	pokemons = {}

	keyword_replacements = {
		# prepend
		'(standard) (shadow)': { 'prepend': 'shadow-', 'postpend': '' },
		'(alolan) (shadow)': { 'prepend': 'shadow-alolan-', 'postpend': '' },
		'(galarian) (shadow)': { 'prepend': 'shadow-galarian-', 'postpend': '' },

		'(shadow)': { 'prepend': 'shadow-', 'postpend': '' },
		'(galarian)': { 'prepend': 'galarian-', 'postpend': '' },
		'(alolan)': { 'prepend': 'alolan-', 'postpend': '' },
		'(dawn wings)': { 'prepend': 'dawn-', 'postpend': '' },
		'(dusk mane)': { 'prepend': 'dusk-', 'postpend': '' },
		'(hisuian)': { 'prepend': 'hisuian-', 'postpend': '' },
		'(standard)': { 'prepend': 'standard-', 'postpend': '' },
		'(ordinary)': { 'prepend': 'ordinary-', 'postpend': '' },
		'(armored)': { 'prepend': 'armored-', 'postpend': '' },

		# postpend
		'(origin)': { 'prepend': '', 'postpend': '-origin-forme' },
		'(10% forme)': { 'prepend': '', 'postpend': '-10-forme' },
		'(50% forme)': { 'prepend': '', 'postpend': '-50-forme' },
		"(pa'u)": { 'prepend': '', 'postpend': '-pa-039-u-style' },
		'(defense)': { 'prepend': '', 'postpend': '-defense-forme' },
		'(speed)': { 'prepend': '', 'postpend': '-speed-forme' },
		'(incarnate)': { 'prepend': '', 'postpend': '-incarnate-forme' },
		'(burn)': { 'prepend': '', 'postpend': '-burn-drive' },
		'(chill)': { 'prepend': '', 'postpend': '-chill-drive' },
		'(douse)': { 'prepend': '', 'postpend': '-douse-drive' },
		'(shock)': { 'prepend': '', 'postpend': '-shock-drive' },
		'(altered)': { 'prepend': '', 'postpend': '-altered-forme' },
		'(average)': { 'prepend': '', 'postpend': '-average-size' },
		'(large)': { 'prepend': '', 'postpend': '-large-size' },
		'(small)': { 'prepend': '', 'postpend': '-small-size' },
		'(super)': { 'prepend': '', 'postpend': '-super-size' },
		'(unbound)': { 'prepend': '', 'postpend': '-unbound' },
		'(therian)': { 'prepend': '', 'postpend': '-therian-forme' },
		'(dusk)': { 'prepend': '', 'postpend': '-dusk-form' },
		'(midday)': { 'prepend': '', 'postpend': '-midday-form' },
		'(midnight)': { 'prepend': '', 'postpend': '-midnight-form' },
		'(aria)': { 'prepend': '', 'postpend': '-aria-forme' },
		'(female)': { 'prepend': '', 'postpend': '-female' },
		'(male)': { 'prepend': '', 'postpend': '-male' },
		'(baile)': { 'prepend': '', 'postpend': '-baile-style' },
		'(pom-pom)': { 'prepend': '', 'postpend': '-pom-pom-style' },
		'(sensu)': { 'prepend': '', 'postpend': '-sensu-style' },
		'(frost)': { 'prepend': '', 'postpend': '-frost' },
		'(heat)': { 'prepend': '', 'postpend': '-heat' },
		'(mow)': { 'prepend': '', 'postpend': '-mow' },
		'(wash)': { 'prepend': '', 'postpend': '-wash' },
		'(land)': { 'prepend': '', 'postpend': '-land-forme' },
		'(sky)': { 'prepend': '', 'postpend': '-sky-forme' },
		'(hero)': { 'prepend': '', 'postpend': '-hero-of-many-battles' },
		'(complete forme)': { 'prepend': '', 'postpend': '-complete-forme' },
	}

	for i, pokemon in enumerate(csv.DictReader(open('data/csv/pvpoke_master_league.csv'))):
		pokemon['rank'] = i + 1
		
		name = pokemon['Pokemon'].lower()
		if '(' in name:
			replace_word = name[name.find('('): name.rfind(')') + 1].strip()
			if replace_word in keyword_replacements:
				removed_word = name.replace(replace_word, '').strip()
				replacements = keyword_replacements[replace_word]
				name = replacements['prepend'] + removed_word + replacements['postpend']

		pokemons[name] = pokemon

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
		display_name = ' '.join([_.capitalize() for _ in name.split('-')])

		data.append({
			'Rank': pokemon.get('rank'),
			'Name': display_name,
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
pvpoke_pokemons = get_pvpoke_pokemons()
joined_pokemons = joined_data(gamepress_pokemons, pvpoke_pokemons)
interested_data = generate_interested_data(joined_pokemons)

df = pd.DataFrame(interested_data)
df.to_json(f'data/json/pokemon.json', orient='records')
print('Generate pokemon completed')
