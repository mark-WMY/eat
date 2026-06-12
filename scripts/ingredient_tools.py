#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingredient_tools.py - Utilities for managing ingredients.json data files.

Usage:
    from scripts.ingredient_tools import load_data, save_data, get_next_id, ...

All functions operate on in-memory data; they do NOT write to files unless you call save_data().
"""

import json
import re
import os
from collections import Counter

# ---------------------------------------------------------------------------
# File paths (relative to project root)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_FILES = [
    os.path.join(BASE_DIR, "js", "ingredients.json"),
]

# ---------------------------------------------------------------------------
# Health-tag matching rules: (tag_id, [keywords])
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Allergen matching rules: (allergen_id, None, [keywords])
#   The None placeholder is for future use.
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Allergens inferred from existing category IDs
# ---------------------------------------------------------------------------
ALLERGEN_BY_CATEGORY = {
    "allergen_pork":     ["food_pork"],
    "allergen_shellfish": ["food_seafood"],
    "allergen_egg":      ["food_egg"],
    "allergen_fish":     ["food_fish"],
}


# ====================== I/O Helpers ======================

def load_data(filepath):
    """Load a JSON file and return the parsed dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(filepath, data):
    """Write data dict back to a JSON file with consistent formatting."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def process_all_files(handler, *args, **kwargs):
    """
    Run `handler(filepath, *args, **kwargs)` for each of the three data files.
    handler receives (filepath, data, *args, **kwargs) and should return True if modified.
    """
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


# ====================== ID / Name Helpers ======================

def get_next_id(data):
    """Return the next sequential item ID (e.g., item_02501) based on existing items."""
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
    """Return a set of all item names (for duplicate checking)."""
    return {i["name"] for i in data.get("items", []) if "name" in i}


def check_names(names_to_check, data_or_names):
    """
    Check which names already exist.
    
    Args:
        names_to_check: iterable of name strings
        data_or_names: either a data dict or a set of existing names
        
    Returns:
        (existing_set, new_set)
    """
    existing = data_or_names if isinstance(data_or_names, set) else get_existing_names(data_or_names)
    existing_found = set()
    new_found = set()
    for name in names_to_check:
        if name in existing:
            existing_found.add(name)
        else:
            new_found.add(name)
    return existing_found, new_found


# ====================== Attribute Matching ======================

def match_health_tags(name):
    """Return a list of health_* tag IDs that match the given item name."""
    result = []
    for tag_id, keywords in HEALTH_RULES:
        for kw in keywords:
            if kw in name:
                result.append(tag_id)
                break
    return result


def match_allergens(name, categories):
    """
    Return a list of allergen_* tag IDs that match the given item name and existing categories.
    Checks both name keywords and category-based inference.
    """
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
    """
    Auto-assign health_* and allergen_* tags to a single item dict based on its name and categories.
    Modifies item['categories'] in-place. Returns number of tags added.
    """
    name = item.get("name", "")
    cats = item.get("categories", [])

    old_cats = set(cats)

    # Remove existing health_/allergen_ tags so we can recompute fresh
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


# ====================== Adding New Items ======================

def add_items_safe(data, new_items):
    """
    Add a list of (name, categories) tuples to data['items'], skipping duplicates.
    
    Args:
        data: the full data dict (modified in-place)
        new_items: iterable of (name_str, categories_list)
        
    Returns:
        (added_count, skipped_count)
    """
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


# ====================== Analysis / Reporting ======================

def count_by_cuisine(data):
    """Return a Counter of cuisine_* category IDs across all items."""
    counter = Counter()
    for item in data.get("items", []):
        for c in item.get("categories", []):
            if c.startswith("cuisine_"):
                counter[c.replace("cuisine_", "")] += 1
    return counter


def count_by_prefix(data, prefix):
    """
    Return a Counter of category IDs matching the given prefix (e.g. 'health_', 'allergen_', 'food_').
    """
    counter = Counter()
    for item in data.get("items", []):
        for c in item.get("categories", []):
            if c.startswith(prefix):
                counter[c] += 1
    return counter


def collect_used_categories(data):
    """Return a sorted set of all category IDs currently in use by any item."""
    ids = set()
    for item in data.get("items", []):
        ids.update(item.get("categories", []))
    return sorted(ids)


def summary(data):
    """Print a brief summary of the dataset."""
    items = data.get("items", [])
    print(f"Total items: {len(items)}")
    cuisines = count_by_cuisine(data)
    print(f"Cuisines represented: {len(cuisines)}")
    print(f"Top 5 cuisines: {', '.join(c for c, _ in cuisines.most_common(5))}")


# ====================== CLI (when run directly) ======================

if __name__ == "__main__":
    data = load_data(DATA_FILES[0])
    summary(data)
