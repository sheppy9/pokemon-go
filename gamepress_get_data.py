import requests
import pandas as pd

from pathlib import Path
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

get_pokemons()
