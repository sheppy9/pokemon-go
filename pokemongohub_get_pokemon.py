import time
import json
import http.client

from pathlib import Path
from bs4 import BeautifulSoup

def query_pokemongohub(endpoint):
    conn = http.client.HTTPSConnection("db.pokemongohub.net")
    payload = ''
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Host': 'db.pokemongohub.net',
        'Connection': 'keep-alive'
    }
    conn.request('GET', endpoint, payload, headers)
    res = conn.getresponse()
    return res.read().decode('utf-8')

def parse_pokemon_data(html_content):
    data = {}
    soup = BeautifulSoup(html_content, 'html.parser')
    articles = soup.select('article')

    # for i, _ in enumerate(articles):
    #     print(i, _)

    basic_info_article = articles[0]
    name = basic_info_article.select_one('header>h1').text
    print(f'Processing HTML content for {name}')

    if ' not available yet' in name:
        print('Not available yet')
        return data

    weakness_div = [_ for _ in basic_info_article.select('div') if _.find('h4') is not None and _.find('h4').text == 'Weaknesses'][0]
    resistances_div = [_ for _ in basic_info_article.select('div') if _.find('h4') is not None and _.find('h4').text == 'Resistances'][0]

    data['name'] = name
    data['type'] = [_.text for _ in basic_info_article.select('div>span:nth-child(3)>span') if len(_.text) > 0]
    data['max_cp'] = int(basic_info_article.select_one('section>figure:nth-child(1)>strong').text.replace('CP', '').strip())
    data['attack'] = int(basic_info_article.select_one('section>figure:nth-child(2)>strong').text.replace('ATK', '').strip())
    data['defense'] = int(basic_info_article.select_one('section>figure:nth-child(3)>strong').text.replace('DEF', '').strip())
    data['stamina'] = int(basic_info_article.select_one('section>figure:nth-child(4)>strong').text.replace('STA', '').strip())
    data['weather_boost'] = [_.select_one('span').text for _ in basic_info_article.select('section>figure:nth-child(5)>ul>li')]
    data['released'] = basic_info_article.select_one('section>figure:nth-child(6)>img')['alt'] == 'Yes'
    data['shiny'] = basic_info_article.select_one('section>figure:nth-child(7)>img')['alt'] == 'Yes'
    data['buddy_distance'] = ''.join([_ for _ in basic_info_article.select_one('section>figure:nth-child(8)').find_all(string=True, recursive=False) if len(_.strip()) > 0])
    data['weaknesses'] = sorted([_.find(string=True) for _ in weakness_div.select('li')])
    data['resistances'] = sorted([_.find(string=True) for _ in resistances_div.select('li')])

    moveset_article = evolution_article = [_ for _ in articles if _.find('h2') is not None and 'best moveset' in _.find('h2').text][0]
    data['best_move'] = [_.text.strip() for _ in moveset_article.select_one('div>div').find_all('div') if len(_.text.strip()) > 0]
    data['dps'] = moveset_article.find_all('div')[5].select_one('div>span:nth-child(2)').text
    data['tdo'] = moveset_article.find_all('div')[6].select_one('div>span:nth-child(2)').text
    data['score'] = moveset_article.find_all('div')[7].select_one('div>span:nth-child(2)').text
    data['moves_combination'] = [{
        'fast_move': tr.select_one('td:nth-child(2)').text.strip(),
        'charge_move': tr.select_one('td:nth-child(3)>a').text.strip(),
        'dps': tr.select_one('td:nth-child(4)').text.strip(),
        'tdo': tr.select_one('td:nth-child(5)').text.strip(),
        'score': tr.select_one('td:nth-child(6)').text.strip()
    } for tr in moveset_article.select('section>table:nth-child(1)>tbody>tr') if tr is not None]

    evolution_article = [_ for _ in articles if _.find('h2') is not None and 'evolution chart' in _.find('h2').text][0]

    data['evolutions'] = [{
        'evolution': _.select('td')[2].text,
        'candy_required': _.select('td')[1].text
    } for _ in evolution_article.select('table>tbody>tr')]

    mega_boost_pokemon = [_ for _ in articles if _.find('h1') is not None and ' that boost ' in _.find('h1').text][0]
    mega_boost_elements = [_.text.strip() for _ in mega_boost_pokemon.select('h3')]
    data['mega_boost_pokemon'] = [{mega_boost_elements[i]:sorted([li.text for li in _.select('li')])}for i, _ in enumerate(mega_boost_pokemon.select('section'))]

    max_cp_article = articles[12]
    data['max_cp_chart'] = {}

    for _ in max_cp_article.select('tr'):
        lvls = _.select('th')
        cps = _.select('td')
        if len(lvls) == len(cps):
            for i in range(len(lvls)):
                data['max_cp_chart'][lvls[i].text] = cps[i].text

    return data

gohub_root = 'data/pokemongohub/'
Path(gohub_root).mkdir(parents=True, exist_ok=True)

pokemons_file = f'{gohub_root}/pokemons.json'
if Path(pokemons_file).exists():
    pokemons = json.loads(open(f'{gohub_root}/pokemons.json').read())
    for pokemon in pokemons:
        id = pokemon['id']
        name = pokemon['name']
        print(f'Querying pokemon details {id} - {name}')
        html_data = query_pokemongohub(f'/pokemon/{id}')

        for i in range(3):
            try:
                pokemon_data = parse_pokemon_data(html_data)
                pokemon.update(pokemon_data)
                break
            except Exception as e:
                print(f'Error processing {id} - {name}, sleep for 10 secs. {e}')
                time.sleep(10)

    with open(f'{gohub_root}/pokemon_datas.json', 'w+') as outfile:
        outfile.write(json.dumps(pokemons, indent=4))
    print('Get pokemon data completed')