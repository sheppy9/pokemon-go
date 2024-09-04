import json
import pandas as pd

from glob import glob

data_root = 'data'
pokemon_root = f'{data_root}/gamepress/pokemon'

csv_data = []
for file in glob(f'{pokemon_root}/*.json'):
	data = json.load(open(file))
	csv_data.append({
		'ID': data['id'],
		'Name': data['name'],
		'Types': ', '.join(sorted(data['types'])),
		'Evolution': ', '.join([_['name'] for _ in data['evolutions']]),
		'Weaknesses': ', '.join(sorted([_['type'] for _ in data['weaknesses']])),
		'Resistances': ', '.join(sorted([_['type'] for _ in data['resistances']])),
		'Attack': data['attack'],
		'Defense': data['defense'],
		'Stamina': data['stamina'],
	})

df = pd.DataFrame(csv_data)
df.to_json(f'{data_root}/json/pokemon.json', orient='records')
print('Generate pokemon completed')
