#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import defaultdict

with open('js/ingredients_full.json', 'r', encoding='utf-8') as f:
    full = json.load(f)
with open('js/ingredients_common.json', 'r', encoding='utf-8') as f:
    common = json.load(f)

common_names = {i['name'] for i in common['items']}
full_only = [i for i in full['items'] if i['name'] not in common_names]

by_cuisine = defaultdict(list)
for item in full_only:
    for cat in item['categories']:
        if cat.startswith('cuisine_'):
            by_cuisine[cat].append(item['name'])
            break
    else:
        by_cuisine['cuisine_other'].append(item['name'])

for cuisine in sorted(by_cuisine.keys()):
    items = by_cuisine[cuisine]
    print(f'{cuisine} ({len(items)}): {items[:15]}')
    print()

print("---")
print(f"Common cuisine categories:")
from collections import Counter
common_cuisine = Counter()
for item in common['items']:
    for cat in item['categories']:
        if cat.startswith('cuisine_'):
            common_cuisine[cat.replace('cuisine_', '')] += 1
for c, n in common_cuisine.most_common(20):
    print(f"  {c}: {n}")
