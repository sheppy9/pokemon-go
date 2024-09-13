import pandas as pd

data_root = 'data'

def list_join(x):
    return ', '.join(x) if isinstance(x, list) else x

def filter_deprecated_moves(x):
    return [_ for _ in x if '*' not in _['charge_move']][0] if isinstance(x, list) else None

pokemons_df = pd.read_json(f'{data_root}/pokemongohub/pokemon_datas.json')

pokemons_df[['score', 'max_cp', 'attack', 'defense', 'dps', 'tdo']] = pokemons_df[['score', 'max_cp', 'attack', 'defense', 'dps', 'tdo']].apply(pd.to_numeric, errors='coerce')
pokemons_df[['type', 'weaknesses', 'resistances', 'best_move']] = pokemons_df[['type', 'weaknesses', 'resistances', 'best_move']].map(list_join)

pokemons_df['undeprecated_moves'] = pokemons_df['moves_combination'].apply(filter_deprecated_moves)
pokemons_df['backup_fast_move'] = pokemons_df['undeprecated_moves'].apply(lambda x: x.get('fast_move') if x is not None else None)
pokemons_df['backup_charge_move'] = pokemons_df['undeprecated_moves'].apply(lambda x: x.get('charge_move') if x is not None else None)
pokemons_df['backup_dps'] = pokemons_df['undeprecated_moves'].apply(lambda x: x.get('dps') if x is not None else None)
pokemons_df['backup_tdo'] = pokemons_df['undeprecated_moves'].apply(lambda x: x.get('tdo') if x is not None else None)
pokemons_df['backup_score'] = pokemons_df['undeprecated_moves'].apply(lambda x: x.get('score') if x is not None else None)

pokemons_df = pokemons_df[['name', 'type', 'score', 'max_cp', 'attack', 'defense', 'weaknesses', 'resistances', 'best_move', 'dps', 'tdo', 'backup_fast_move', 'backup_charge_move', 'backup_dps', 'backup_tdo', 'backup_score']]

pokemons_df.to_json(f'{data_root}/json/individual_pokemon.json', orient='records')
