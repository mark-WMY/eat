#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add common everyday food items to both common and full JSON files."""
import json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open('js/ingredients_common.json', 'r', encoding='utf-8') as f:
    common = json.load(f)
with open('js/ingredients_full.json', 'r', encoding='utf-8') as f:
    full = json.load(f)

common_names = set(i['name'] for i in common['items'])
full_names = set(i['name'] for i in full['items'])

# Find max ID
max_id = 0
for item in common['items'] + full['items']:
    try:
        n = int(item['id'].replace('item_', ''))
        if n > max_id: max_id = n
    except: pass

next_id = max_id + 1
def new_id():
    global next_id
    nid = f"item_{next_id:05d}"
    next_id += 1
    return nid

# New items to add to common (synced to full)
# Format: (name, categories, attributes)
new_common_items = [
    # ===== 常见家常菜 =====
    ("土豆炒肉片", ["cuisine_other", "meal_lunch", "meal_dinner", "food_pork", "dish_main"],
     {"health": [], "allergens": []}),
    ("番茄炒鸡蛋", ["cuisine_other", "meal_lunch", "meal_dinner", "food_egg", "dish_main"],
     {"health": [], "allergens": ["egg"]}),
    ("西红柿炒鸡蛋", ["cuisine_other", "meal_lunch", "meal_dinner", "food_egg", "dish_main"],
     {"health": [], "allergens": ["egg"]}),
    ("炝炒圆白菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("蒜蓉菠菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("水蒸蛋", ["cuisine_other", "meal_lunch", "meal_dinner", "food_egg", "dish_main"],
     {"health": ["light"], "allergens": ["egg"]}),
    ("蒸蛋", ["cuisine_other", "meal_lunch", "meal_dinner", "food_egg", "dish_main"],
     {"health": ["light"], "allergens": ["egg"]}),
    ("萝卜炖排骨", ["cuisine_other", "meal_lunch", "meal_dinner", "food_pork", "food_soup", "dish_main"],
     {"health": [], "allergens": ["pork"]}),
    ("炒河粉", ["cuisine_yue", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": ["gluten"]}),
    ("炒米粉", ["cuisine_other", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": []}),
    ("蒜蓉油麦菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "low_fat"], "allergens": []}),

    # ===== 常见蔬菜/食材 =====
    ("土豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "food_wholegrain", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("白菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("黄瓜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("番茄", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("茄子", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("青椒", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("南瓜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("冬瓜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "low_fat"], "allergens": []}),
    ("丝瓜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("胡萝卜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("花菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("菠菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber", "high_protein"], "allergens": ["celery"]}),
    ("蒜苔", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("豆角", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("四季豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("豌豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber", "high_protein"], "allergens": []}),
    ("山药", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("莲藕", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("芋头", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("红薯", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "food_wholegrain", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("紫薯", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "food_wholegrain", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("玉米", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "food_wholegrain", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("白萝卜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie"], "allergens": []}),
    ("韭黄", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": [], "allergens": []}),

    # ===== 常见菌类/干货 =====
    ("木耳", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("香菇", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("金针菇", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),
    ("银耳", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_dessert"],
     {"health": ["high_fiber"], "allergens": []}),
    ("百合", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_dessert"],
     {"health": [], "allergens": []}),

    # ===== 常见豆制品/粉面 =====
    ("豆腐", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_protein"], "allergens": ["soy"]}),
    ("豆腐皮", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_protein"], "allergens": ["soy"]}),
    ("粉丝", ["cuisine_other", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": []}),
    ("粉条", ["cuisine_other", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": []}),
    ("河粉", ["cuisine_yue", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": ["gluten"]}),
    ("挂面", ["cuisine_other", "meal_lunch", "meal_dinner", "food_noodles", "dish_staple"],
     {"health": [], "allergens": ["gluten"]}),
    ("意面", ["cuisine_italian", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": ["gluten"]}),
    ("米粉", ["cuisine_other", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": []}),
    ("生煎包", ["cuisine_shanghai", "meal_breakfast", "meal_lunch", "food_bun", "dish_main"],
     {"health": [], "allergens": ["gluten"]}),
    ("板面", ["cuisine_anhui", "meal_lunch", "meal_dinner", "food_noodles", "dish_main"],
     {"health": [], "allergens": ["gluten"]}),
    ("吐司", ["cuisine_western", "meal_breakfast", "food_bun", "dish_staple"],
     {"health": [], "allergens": ["gluten", "egg", "dairy"]}),
    ("扁豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber"], "allergens": []}),

    # ===== 常见杂粮 =====
    ("小米", ["cuisine_other", "meal_breakfast", "meal_lunch", "meal_dinner", "food_wholegrain", "food_congee", "dish_staple"],
     {"health": ["high_fiber"], "allergens": []}),
    ("燕麦", ["cuisine_western", "meal_breakfast", "food_wholegrain", "dish_staple"],
     {"health": ["high_fiber"], "allergens": ["gluten"]}),
    ("糙米", ["cuisine_other", "meal_lunch", "meal_dinner", "food_wholegrain", "dish_staple"],
     {"health": ["high_fiber"], "allergens": []}),
    ("红豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_wholegrain", "dish_dessert"],
     {"health": ["high_fiber"], "allergens": []}),
    ("绿豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_wholegrain", "dish_dessert"],
     {"health": ["high_fiber"], "allergens": []}),
    ("黑豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_wholegrain", "dish_main"],
     {"health": ["high_fiber", "high_protein"], "allergens": []}),
    ("花生", ["cuisine_other", "meal_lunch", "meal_dinner", "food_wholegrain", "dish_snack"],
     {"health": ["high_protein"], "allergens": ["peanut"]}),
    ("蚕豆", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["high_fiber", "high_protein"], "allergens": []}),

    # ===== 常见肉类 =====
    ("鸡翅", ["cuisine_other", "meal_lunch", "meal_dinner", "food_poultry", "dish_main"],
     {"health": ["high_protein"], "allergens": []}),
    ("鸡腿", ["cuisine_other", "meal_lunch", "meal_dinner", "food_poultry", "dish_main"],
     {"health": ["high_protein"], "allergens": []}),
    ("盐水鸭", ["cuisine_jiangsu", "meal_lunch", "meal_dinner", "food_poultry", "dish_main"],
     {"health": [], "allergens": []}),

    # ===== 常见丸类 =====
    ("鱼丸", ["cuisine_other", "meal_lunch", "meal_dinner", "food_seafood", "dish_main"],
     {"health": ["high_protein"], "allergens": ["fish"]}),
    ("虾丸", ["cuisine_other", "meal_lunch", "meal_dinner", "food_seafood", "dish_main"],
     {"health": ["high_protein"], "allergens": ["shellfish"]}),

    # ===== 常见饮品 =====
    ("奶油", ["cuisine_western", "meal_lunch", "meal_dinner", "food_dessert", "dish_beverage"],
     {"health": [], "allergens": ["dairy"]}),
    ("芝士", ["cuisine_western", "meal_lunch", "meal_dinner", "food_dessert", "dish_main"],
     {"health": [], "allergens": ["dairy"]}),
    ("葡萄酒", ["cuisine_other", "meal_lunch", "meal_dinner", "food_alcohol", "dish_beverage"],
     {"health": [], "allergens": ["sulfite"]}),

    # ===== 常见小吃/快餐 =====
    ("串串", ["cuisine_chuan", "meal_lunch", "meal_dinner", "meal_midnight", "food_meat", "food_hotpot", "dish_main"],
     {"health": [], "allergens": []}),
    ("烧烤", ["cuisine_other", "meal_lunch", "meal_dinner", "meal_midnight", "food_bbq", "dish_main"],
     {"health": [], "allergens": []}),

    # ===== 常见炒菜 =====
    ("蒜蓉菠菜", ["cuisine_other", "meal_lunch", "meal_dinner", "food_vegetarian", "dish_main"],
     {"health": ["low_calorie", "high_fiber"], "allergens": []}),
    ("番茄炒蛋", ["cuisine_other", "meal_lunch", "meal_dinner", "food_egg", "dish_main"],
     {"health": [], "allergens": ["egg"]}),
    ("萝卜炖排骨", ["cuisine_other", "meal_lunch", "meal_dinner", "food_pork", "food_soup", "dish_main"],
     {"health": [], "allergens": ["pork"]}),
]

# Filter out duplicates
added_common = 0
added_full = 0
skipped = 0

for name, categories, attributes in new_common_items:
    if name in common_names:
        skipped += 1
        continue

    item = {
        "id": new_id(),
        "name": name,
        "categories": categories,
        "attributes": attributes
    }

    # Add to common
    common['items'].append(item)
    common_names.add(name)
    added_common += 1

    # Add to full if not already there
    if name not in full_names:
        full['items'].append(item)
        full_names.add(name)
        added_full += 1

# Save files
with open('js/ingredients_common.json', 'w', encoding='utf-8') as f:
    json.dump(common, f, ensure_ascii=False, indent=2)

with open('js/ingredients_full.json', 'w', encoding='utf-8') as f:
    json.dump(full, f, ensure_ascii=False, indent=2)

print(f"Added {added_common} items to common")
print(f"Added {added_full} items to full (new items not previously in full)")
print(f"Skipped {skipped} items (already in common)")
print(f"Final common: {len(common['items'])} items")
print(f"Final full: {len(full['items'])} items")
print(f"Common is subset of full: {set(i['name'] for i in common['items']).issubset(set(i['name'] for i in full['items']))}")
