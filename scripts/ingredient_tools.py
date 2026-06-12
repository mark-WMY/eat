#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingredient_tools.py - Utilities for managing ingredients data files.

Usage:
    from scripts.ingredient_tools import load_data, save_data, get_next_id, ...

The data has been split into two files:
  - ingredients_full.json   (all 3339 dishes)
  - ingredients_common.json (2254 Chinese-cuisine dishes, loaded first)

All functions operate on in-memory data; they do NOT write to files unless you call save_data().
"""

import json
import re
import os
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILES = [
    os.path.join(BASE_DIR, "js", "ingredients_full.json"),
    os.path.join(BASE_DIR, "js", "ingredients_common.json"),
]

HEALTH_RULES = [
    ("health_low_fat",       ["清蒸", "白灼", "水煮", "凉拌", "清炒", "炖", "卤"]),
    ("health_low_sugar",     ["无糖", "少糖", "低糖"]),
    ("health_low_salt",      ["低盐", "清淡", "清汤"]),
    ("health_high_protein",  ["鸡", "鱼", "虾", "牛肉", "蛋白", "精肉", "里脊"]),
    ("health_sugar_free",    ["无糖", "代糖"]),
    ("health_high_fiber",    ["杂粮", "全麦", "蔬菜", "芹", "木耳", "菌", "菇", "藻"]),
    ("health_vegan",         ["素", "蔬菜", "凉拌", "清炒", "豆制品", "豆腐", "香菇", "菌菇", "藻"]),
    ("health_nourishing",    ["滋补", "炖", "煲", "汤", "粥"]),
    ("health_light",         ["清淡", "清炒", "白灼", "清蒸", "凉拌"]),
]

ALLERGEN_RULES = [
    ("allergen_pork",      None, ["猪肉", "五花", "里脊", "排骨", "猪蹄", "猪脚", "红烧肉", "回锅肉", "糖醋里脊"]),
    ("allergen_chili",     None, ["辣", "麻辣", "香辣", "酸辣", "麻辣香锅", "辣子", "剁椒", "泡椒"]),
    ("allergen_onion",     None, ["葱"]),
    ("allergen_ginger",    None, ["姜", "姜葱", "姜丝"]),
    ("allergen_garlic",    None, ["蒜", "大蒜", "蒜蓉", "蒜泥"]),
    ("allergen_peanut",    None, ["花生", "花生碎", "宫保"]),
    ("allergen_tree_nut",  None, ["核桃", "杏仁", "腰果", "坚果", "松仁", "瓜子"]),
    ("allergen_dairy",     None, ["奶酪", "芝士", "奶油", "牛奶", "乳糖", "炼乳", "黄油"]),
    ("allergen_egg",       None, ["蛋", "炒蛋", "荷包蛋", "鸡蛋", "蛋花", "蒸蛋"]),
    ("allergen_shellfish", None, ["虾", "蟹", "蛤", "贝", "蚝", "蛏", "扇贝", "海鲜", "鲈鱼", "草鱼", "鲤鱼", "鲫鱼", "鱼香", "水煮鱼", "酸菜鱼"]),
    ("allergen_fish",      None, ["鱼", "鲈", "鲤", "草鱼", "鲫鱼", "鲢", "鳙", "青鱼", "罗非", "三文鱼", "鳕鱼"]),
    ("allergen_soy",       None, ["豆", "豆浆", "豆腐", "酱油", "豆制品", "腐竹", "豆皮", "黄豆"]),
    ("allergen_gluten",    None, ["面", "饼", "包", "饺", "麸", "麦", "馒头", "面条", "拉面", "刀削面"]),
    ("allergen_sesame",    None, ["芝麻", "芝麻酱", "麻酱"]),
]

ALLERGEN_BY_CATEGORY = {
    "allergen_pork":     ["food_pork"],
    "allergen_shellfish": ["food_seafood"],
    "allergen_egg":      ["food_egg"],
    "allergen_fish":     ["food_fish"],
}

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def process_all_files(handler, *args, **kwargs):
    for fp in DATA_FILES:
        print(f"Processing: {fp}")
        if not os.path.exists(fp):
            print("  SKIP: file not found")
            continue
        data = load_data(fp)
        modified = handler(fp, data, *args, **kwargs)
        if modified:
            save_data(fp, data)
            print(f"  Saved ({len(data['items'])} items)")
        else:
            print("  No changes")

def get_next_id(data):
    max_num = 0
    for item in data.get("items", []):
        if "id" in item:
            m = re.search(r"item_(\d+)", item["id"])
            if m:
                n = int(m.group(1))
                if n > max_num:
                    max_num = n
    return max_num + 1

def get_existing_names(data):
    return {i["name"] for i in data.get("items", []) if "name" in i}

def check_names(names_to_check, data_or_names):
    existing = data_or_names if isinstance(data_or_names, set) else get_existing_names(data_or_names)
    existing_found = set()
    new_found = set()
    for name in names_to_check:
        if name in existing:
            existing_found.add(name)
        else:
            new_found.add(name)
    return existing_found, new_found

def match_health_tags(name):
    result = []
    for tag_id, keywords in HEALTH_RULES:
        for kw in keywords:
            if kw in name:
                result.append(tag_id)
                break
    return result

def match_allergens(name, categories):
    result = []
    for allergen_id, _, keywords in ALLERGEN_RULES:
        for kw in keywords:
            if kw in name:
                result.append(allergen_id)
                break
    for allergen_id, cat_ids in ALLERGEN_BY_CATEGORY.items():
        for cid in cat_ids:
            if cid in categories and allergen_id not in result:
                result.append(allergen_id)
                break
    return result

def auto_assign_attributes(item):
    name = item.get("name", "")
    cats = item.get("categories", [])
    old_cats = set(cats)
    cats = [c for c in cats if not c.startswith("health_") and not c.startswith("allergen_")]
    added = 0
    for tag in match_health_tags(name):
        if tag not in cats:
            cats.append(tag)
            added += 1
    for tag in match_allergens(name, cats):
        if tag not in cats:
            cats.append(tag)
            added += 1
    if set(cats) != old_cats:
        item["categories"] = cats
    return added

def add_items_safe(data, new_items):
    existing = get_existing_names(data)
    next_id = get_next_id(data)
    added = 0
    skipped = 0
    for name, cats in new_items:
        if name in existing:
            skipped += 1
            continue
        data["items"].append({"id": f"item_{next_id:05d}", "name": name, "categories": list(cats)})
        existing.add(name)
        next_id += 1
        added += 1
    return added, skipped

def count_by_cuisine(data):
    counter = Counter()
    for item in data.get("items", []):
        for c in item.get("categories", []):
            if c.startswith("cuisine_"):
                counter[c.replace("cuisine_", "")] += 1
    return counter

def count_by_prefix(data, prefix):
    counter = Counter()
    for item in data.get("items", []):
        for c in item.get("categories", []):
            if c.startswith(prefix):
                counter[c] += 1
    return counter

def collect_used_categories(data):
    ids = set()
    for item in data.get("items", []):
        ids.update(item.get("categories", []))
    return sorted(ids)

def summary(data):
    items = data.get("items", [])
    print(f"Total items: {len(items)}")
    cuisines = count_by_cuisine(data)
    print(f"Cuisines represented: {len(cuisines)}")
    print(f"Top 5 cuisines: {', '.join(c for c, _ in cuisines.most_common(5))}")

if __name__ == "__main__":
    data = load_data(DATA_FILES[0])
    summary(data)
