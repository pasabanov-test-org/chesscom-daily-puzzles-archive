import json
import os
import requests
import sys
import time

API_URL = 'https://api.chess.com/pub/puzzle'

OUTPUT_DIR = 'puzzles'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_date(url):
	# https://www.chess.com/daily/YYYY-MM-DD
	try:
		return url.strip('/').split('/')[-1]
	except:
		return None

seen = set()

for filename in os.listdir(OUTPUT_DIR):
	if filename.endswith('.json'):
		seen.add(filename[:-5])

print(f'Loaded {len(seen)} existing puzzles')

r = requests.get(API_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}, timeout=10)
data = r.json()

url = data.get('url')
if not url:
	raise ValueError

date_str = extract_date(url)
if not date_str:
	raise ValueError

if date_str in seen:
	print(f'duplicate {date_str}')
	exit()

seen.add(date_str)

path = os.path.join(OUTPUT_DIR, f'{date_str}.json')

with open(path, 'w', encoding='utf-8') as f:
	json.dump(data, f, ensure_ascii=False, indent='\t')

print(f'Saved {date_str} (new total: {len(seen)})')