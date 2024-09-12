import http.client

from bs4 import BeautifulSoup

def pokemonhub_get_pokemons(region):
	conn = http.client.HTTPSConnection('db.pokemongohub.net')
	payload = ''
	headers = {
		'User-Agent': 'Mozilla/5.0',
		'Accept': '*/*',
		'Host': 'db.pokemongohub.net',
		'Connection': 'keep-alive'
	}
	conn.request('GET', f'/pokedex/{region}', payload, headers)
	res = conn.getresponse()
	return res.read().decode('utf-8')

def parse_pokemon_html(html_content):
	soup = BeautifulSoup(html_content, 'html.parser')

	pokemons = []
	for row in soup.select('tbody>tr'):
		id, name, shiny, release = row.find_all('td')
		shiny_img = shiny.find('img')
		release_img = release.find('img')
		pokemons.append({
			'id': int(id.text.replace('#', '')),
			'name': name.text,
			'href': name.find('a')['href'],
			'img': name.select_one('img')['src'],
			'shiny': shiny_img is not None and shiny_img['alt'] == 'Yes', 
			'release': release_img is not None and release_img['alt'] == 'Yes'
		})
	return pokemons

regions = [
	'kanto',
	'johto',
	'hoenn',
	'sinnoh',
	'unova',
	'kalos',
	'alola',
	'galar',
	'paldea'
]

full_pokemons = []
for region in regions:
	html_data = pokemonhub_get_pokemons(region)
	pokemons = parse_pokemon_html(html_data)
	full_pokemons.extend(pokemons)
print(f'Number of pokemons: {len(full_pokemons)}')