#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重新检查 ingredients_common.json，找出可能遗漏的地方性菜品
"""

import json
import os
from collections import defaultdict

BASE_DIR = "C:\\Users\\lin\\Downloads\\eatWhat"
DATA_FILE = os.path.join(BASE_DIR, "js", "ingredients_common.json")

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['items']
print(f"当前总条目数: {len(items)}")
print(f"唯一ID数: {len(set(item['id'] for item in items))}")

# 按菜系分组
cuisine_groups = defaultdict(list)
no_cuisine = []

for item in items:
    categories = item.get('categories', [])
    # 找出菜系类别（以 cuisine_ 开头）
    cuisines = [cat for cat in categories if cat.startswith('cuisine_')]
    if cuisines:
        for cuisine in cuisines:
            cuisine_groups[cuisine].append(item)
    else:
        no_cuisine.append(item)

# 读取 categories 定义，获取菜系中文名
categories_def = data.get('categories', {}).get('cuisine', {})
cuisine_names = {v['id']: v['name'] for v in categories_def.values()}

print(f"\n按菜系分组统计:")
print(f"  - 有菜系分类的条目: {sum(len(v) for v in cuisine_groups.values())}")
print(f"  - 无菜系分类的条目: {len(no_cuisine)}")
print(f"  - 菜系数量: {len(cuisine_groups)}")

# 重点检查：小众菜系
MINOR_CUISINES = [
    'cuisine_yunnan',   # 滇菜
    'cuisine_guizhou',   # 黔菜
    'cuisine_anhui',     # 徽菜
    'cuisine_shaanxi',   # 陕菜
    'cuisine_jin',       # 晋菜
    'cuisine_gansu',     # 甘菜
    'cuisine_guangxi',   # 桂菜
    'cuisine_jiangxi',   # 赣菜
    'cuisine_min',       # 闽菜（部分地方性较强）
]

print(f"\n{'='*60}")
print("重点检查：小众菜系（可能含地方性菜品）")
print(f"{'='*60}")

for cuisine_id in MINOR_CUISINES:
    if cuisine_id in cuisine_groups:
        items_in_cuisine = cuisine_groups[cuisine_id]
        cuisine_name = cuisine_names.get(cuisine_id, cuisine_id)
        print(f"\n【{cuisine_name}】 ({cuisine_id}) - {len(items_in_cuisine)} 个条目:")
        for item in items_in_cuisine[:20]:  # 只显示前20个
            print(f"  - {item['name']} (ID: {item['id']})")
        if len(items_in_cuisine) > 20:
            print(f"  ... (还有 {len(items_in_cuisine) - 20} 个)")

# 检查无菜系分类的条目（可能含地方性小吃）
print(f"\n{'='*60}")
print(f"无菜系分类的条目（可能含地方性小吃）: {len(no_cuisine)} 个")
print(f"{'='*60}")

# 按名称关键词检查可能的地方性菜品
LOCAL_KEYWORDS = [
    '老北京', '北京', '豆汁', '爆肚', '炒肝',
    '武汉', '热干面', '三镇', '沔阳', '黄陂',
    '西安', '陕西', '兰州', '甘肃', '新疆', '乌鲁木齐',
    '河南', '道口', '黄河',
    '广西', '桂林', '南宁', '老友', '螺蛳鸭',
    '云南', '大理', '丽江', '傣族',
    '贵州', '遵义', '酸汤',
    '安徽', '徽州', '黄山', '绩溪',
    '山西', '平遥', '晋',
    '佛跳墙', '狗肉', '竹鼠',
]

print(f"\n{'='*60}")
print("关键词搜索：可能遗漏的地方性菜品")
print(f"{'='*60}")

found_local = []
for item in items:
    name = item['name']
    if any(kw in name for kw in LOCAL_KEYWORDS):
        found_local.append(item)

print(f"\n找到 {len(found_local)} 个可能的地方性菜品:")
for item in found_local:
    categories = item.get('categories', [])
    print(f"  - {item['name']} (ID: {item['id']}, 分类: {categories})")

# 保存结果
output_file = os.path.join(BASE_DIR, "recheck_report.json")
output_data = {
    'total_items': len(items),
    'minor_cuisine_items': {cid: [{'id': i['id'], 'name': i['name']} for i in cuisine_groups.get(cid, [])] for cid in MINOR_CUISINES},
    'found_local_items': [{'id': i['id'], 'name': i['name'], 'categories': i.get('categories', [])} for i in found_local]
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"\n详细报告已保存到: {output_file}")
