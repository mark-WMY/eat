import json

data = json.load(open('js/ingredients.json', encoding='utf-8'))

# 统计每个菜系的菜品数量
cuisine_count = {}
for item in data['items']:
    for cat in item['categories']:
        if cat.startswith('cuisine_'):
            cuisine_count[cat] = cuisine_count.get(cat, 0) + 1

# 获取所有菜系ID
all_cuisines = {v['id']: v['name'] for k, v in data['categories']['cuisine'].items()}

print('=== 菜系菜品分布 ===')
print(f'{"菜系":<15} {"菜品数":<8} {"状态"}')
print('-' * 40)

for cid, cname in sorted(all_cuisines.items()):
    count = cuisine_count.get(cid, 0)
    status = '✓' if count >= 5 else ('⚠' if count > 0 else '✗')
    print(f'{cname:<12} {count:<8} {status}')

print(f'\n总菜品数: {len(data["items"])}')
print(f'有菜品的菜系数: {len(cuisine_count)}')
print(f'无菜品的菜系数: {len(all_cuisines) - len(cuisine_count)}')

# 找出没有菜品的菜系
empty_cuisines = [cid for cid in all_cuisines if cid not in cuisine_count]
if empty_cuisines:
    print('\n=== 需要补充菜品的菜系 ===')
    for cid in empty_cuisines:
        print(f'  - {all_cuisines[cid]} ({cid})')
