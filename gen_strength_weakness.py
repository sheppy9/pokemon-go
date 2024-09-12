import csv
import json

from pathlib import Path

infile = 'data/csv'
outfile = 'data/json'

Path(infile).mkdir(parents=True, exist_ok=True)
Path(outfile).mkdir(parents=True, exist_ok=True)

json_data = list(csv.DictReader(open(f'{infile}/strength_weakness.csv')))
for row in json_data:
	row['Strong Against'] = ', '.join(sorted([_.strip() for _ in row['Strong Against'].split(', ')]))
	row['Weakness'] = ', '.join(sorted([_.strip() for _ in row['Weakness'].split(', ')]))

writefile = open(f'{outfile}/strength_weakness.json', 'w+')
writefile.write(json.dumps(json_data, indent=4))
writefile.close()