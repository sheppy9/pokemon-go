import json
import pandas as pd

from glob import glob

data_root = 'data'
pokemon_root = f'{data_root}/gamepress/pokemon'

csv_data = []
for file in glob(f'{pokemon_root}/*.json'):
	data = json.load(open(file))
	csv_data.append({
		'Name': data['id'],
		'Weaknesses': ', '.join(sorted([_['type'] for _ in data['weaknesses']])),
		'Resistances': ', '.join(sorted([_['type'] for _ in data['resistances']])),
	})

df = pd.DataFrame(csv_data)
df.to_json(f'{data_root}/json/pokemon.json', orient='records')
