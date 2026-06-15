#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤1: 去重 + 步骤2: 删除地方性菜品
"""

import json
import os

BASE_DIR = "C:\\Users\\lin\\Downloads\\eatWhat"
DATA_FILE = os.path.join(BASE_DIR, "js", "ingredients_common.json")
REMOVAL_FILE = os.path.join(BASE_DIR, "removal_candidates.json")

# 读取删除名单
with open(REMOVAL_FILE, 'r', encoding='utf-8') as f:
    removal_list = json.load(f)
remove_ids = set(item['id'] for item in removal_list)
print(f"待删除 ID 数: {len(remove_ids)}")

# 读取原数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

original_count = len(data['items'])
print(f"原条目总数 (含重复): {original_count}")

# 步骤1: 去重 - 保留每个 ID 的第一个出现
seen_ids = set()
deduped_items = []
duplicates = []
for item in data['items']:
    if item['id'] not in seen_ids:
        deduped_items.append(item)
        seen_ids.add(item['id'])
    else:
        duplicates.append(item['id'])

print(f"去重后条目数: {len(deduped_items)}")
print(f"删除重复条目数: {len(data['items']) - len(deduped_items)}")

# 步骤2: 删除地方性菜品
new_items = [item for item in deduped_items if item['id'] not in remove_ids]
removed_count = len(deduped_items) - len(new_items)

print(f"\n删除地方性菜品数: {removed_count}")
print(f"最终条目数: {len(new_items)}")

# 验证：列出未找到的 ID
found_ids = set(item['id'] for item in deduped_items)
not_found = remove_ids - found_ids
if not_found:
    print(f"\n警告：以下 {len(not_found)} 个 ID 在去重后未找到:")
    for rid in sorted(not_found):
        print(f"  - {rid}")

# 更新数据
data['items'] = new_items

# 保存
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n[完成] 文件已保存: {DATA_FILE}")
print(f"  原总数 (含重复): {original_count}")
print(f"  去重删除: {len(duplicates)} 条")
print(f"  地方性删除: {removed_count} 条")
print(f"  最终总数: {len(new_items)}")

# 输出被删除的地方性菜品
print(f"\n被删除的地方性菜品 ({removed_count} 个):")
for item in removal_list:
    if item['id'] in remove_ids and item['id'] not in not_found:
        print(f"  - {item['name']} (ID: {item['id']})")
