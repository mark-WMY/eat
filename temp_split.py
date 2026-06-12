#!/usr/bin/env python3
import json, os

COMMON_CUISINE_IDS = {
    'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
    'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
    'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
    'cuisine_guizhou', 'cuisine_other', 'cuisine_henan', 'cuisine_shaanxi',
    'cuisine_shanxi', 'cuisine_gansu', 'cuisine_xinjiang', 'cuisine_hubei',
    'cuisine_chongqing', 'cuisine_jilin', 'cuisine_guangxi'
}

with open('js/ingredients.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

categories = data['categories']
all_items = data['items']
common_items = [item for item in all_items if set(item.get('categories', [])) & COMMON_CUISINE_IDS]

common_data = {'categories': categories, 'items': common_items}
full_data = {'categories': categories, 'items': all_items}

with open('js/ingredients_common.json', 'w', encoding='utf-8') as f:
    json.dump(common_data, f, ensure_ascii=False)

with open('js/ingredients_full.json', 'w', encoding='utf-8') as f:
    json.dump(full_data, f, ensure_ascii=False)

print(f"common: {len(common_items)} items, {os.path.getsize('js/ingredients_common.json')/1024:.0f} KB")
print(f"full: {len(all_items)} items, {os.path.getsize('js/ingredients_full.json')/1024:.0f} KB")
