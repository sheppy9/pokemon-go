import json
import requests

from pathlib import Path

refresh_data = False
endpoints = '''
/api/v1/api_hashes.json
/api/v1/pokemon_names.json
/api/v1/released_pokemon.json
/api/v1/nesting_pokemon.json
/api/v1/shiny_pokemon.json
/api/v1/raid_exclusive_pokemon.json
/api/v1/alolan_pokemon.json
/api/v1/possible_ditto_pokemon.json
/api/v1/pokemon_stats.json
/api/v1/fast_moves.json
/api/v1/charged_moves.json
/api/v1/pokemon_max_cp.json
/api/v1/pokemon_buddy_distances.json
/api/v1/pokemon_candy_to_evolve.json
/api/v1/pokemon_encounter_data.json
/api/v1/pokemon_types.json
/api/v1/weather_boosts.json
/api/v1/type_effectiveness.json
/api/v1/pokemon_rarity.json
/api/v1/pokemon_powerup_requirements.json
/api/v1/pokemon_genders.json
/api/v1/player_xp_requirements.json
/api/v1/pokemon_generations.json
/api/v1/shadow_pokemon.json
/api/v1/pokemon_forms.json
/api/v1/current_pokemon_moves.json
/api/v1/pvp_exclusive_pokemon.json
/api/v1/galarian_pokemon.json
/api/v1/cp_multiplier.json
/api/v1/community_days.json
/api/v1/pokemon_evolutions.json
/api/v1/raid_bosses.json
/api/v1/research_task_exclusive_pokemon.json
/api/v1/mega_pokemon.json
/api/v1/pokemon_height_weight_scale.json
/api/v1/levelup_rewards.json
/api/v1/badges.json
/api/v1/gobattle_league_rewards.json
/api/v1/raid_settings.json
/api/v1/mega_evolution_settings.json
/api/v1/friendship_level_settings.json
/api/v1/gobattle_ranking_settings.json
/api/v1/baby_pokemon.json
/api/v1/pvp_fast_moves.json
/api/v1/pvp_charged_moves.json
/api/v1/time_limited_shiny_pokemon.json
/api/v1/photobomb_exclusive_pokemon.json
'''.split('\n')

pokoapi = Path('data/pogoapi')
pokoapi.mkdir(parents=True, exist_ok=True)

host = 'https://pogoapi.net'
for endpoint in endpoints:
	if len(endpoint) == 0:
		continue

	out = endpoint.split('/')[-1]
	if len(out) == 0:
		continue
	
	json_file = pokoapi.joinpath(out)
	if json_file.exists() and not refresh_data:
		continue

	res = requests.get(f'{host}{endpoint}')
	with open(json_file, 'w') as f:
		f.write(json.dumps(res.json(), indent=4))
		print(f'Wrote {json_file} successfully')
print(f'Queried data successfully, data located at {pokoapi}')