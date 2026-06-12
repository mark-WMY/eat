#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查测试结果的脚本"""

import json

# 读取测试输出文件
test_file = 'js/ingredients_test_20260612_095141.json'
data = json.load(open(test_file, 'r', encoding='utf-8'))

print("=" * 80)
print("测试结果检查")
print("=" * 80)
print()

# 检查前10个食物的attributes字段
print("【前10个食物的attributes字段】")
for i, item in enumerate(data['items']):
    name = item['name']
    attrs = item.get('attributes', None)
    
    if attrs is None:
        print(f"{i+1}. {name}: [缺失attributes字段]")
    else:
        health = attrs.get('health', [])
        allergens = attrs.get('allergens', [])
        print(f"{i+1}. {name}:")
        print(f"   - health: {health}")
        print(f"   - allergens: {allergens}")

print()

# 读取原始文件，对比attributes字段
print("【对比原始文件的attributes字段】")
original_file = 'js/ingredients.json.backup_20260612_095020'
original_data = json.load(open(original_file, 'r', encoding='utf-8'))

for i, item in enumerate(original_data['items'][:10]):
    name = item['name']
    attrs = item.get('attributes', None)
    
    if attrs is None:
        print(f"{i+1}. {name}: [缺失attributes字段]")
    else:
        health = attrs.get('health', [])
        allergens = attrs.get('allergens', [])
        print(f"{i+1}. {name}:")
        print(f"   - health: {health}")
        print(f"   - allergens: {allergens}")

print()
print("=" * 80)
print("检查完成")
print("=" * 80)
