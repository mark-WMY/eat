#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('js/ingredients_common.json', 'r', encoding='utf-8') as f:
    common = json.load(f)
with open('js/ingredients_full.json', 'r', encoding='utf-8') as f:
    full = json.load(f)

common_names = {i['name'] for i in common['items']}
full_names = {i['name'] for i in full['items']}

print("Common items:", len(common['items']))
print("Full items:", len(full['items']))
print("In common but NOT in full:", len(common_names - full_names))
print("In full but NOT in common:", len(full_names - common_names))
print("Common is subset of full:", common_names.issubset(full_names))

diff = common_names - full_names
if diff:
    print("Items in common but not full (", len(diff), "):")
    for n in sorted(diff)[:20]:
        print("  -", n)
