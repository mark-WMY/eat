import json

with open('js/ingredients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计每个菜系的菜品数量
cuisine_count = {}
for item in data['items']:
    for cat in item['categories']:
        if cat.startswith('cuisine_'):
            cuisine_count[cat] = cuisine_count.get(cat, 0) + 1

# 获取所有菜系
all_cuisines = {v['id']: v['name'] for k, v in data['categories']['cuisine'].items()}

print('=== Cuisine Distribution After Supplement ===')
print(f'{"Cuisine":<15} {"Count":<8} {"Status"}')
print('-' * 40)

empty_count = 0
low_count = 0
ok_count = 0

for cid, cname in sorted(all_cuisines.items()):
    count = cuisine_count.get(cid, 0)
    if count >= 5:
        status = 'OK'
        ok_count += 1
    elif count > 0:
        status = 'LOW'
        low_count += 1
    else:
        status = 'EMPTY'
        empty_count += 1
    print(f'{cname:<12} {count:<8} {status}')

print(f'\nSummary:')
print(f'  Total items: {len(data["items"])}')
print(f'  OK (>=5): {ok_count}')
print(f'  LOW (<5): {low_count}')
print(f'  EMPTY: {empty_count}')

# 检查特定菜品是否存在
target_dishes = ['辣椒炒鸡蛋', '红烧肉', '干煸茄子', '番茄炒蛋', '酸辣土豆丝', '可乐鸡翅']
print(f'\n=== Check Target Dishes ===')
item_names = [item['name'] for item in data['items']]
for dish in target_dishes:
    found = dish in item_names
    print(f'  {dish}: {"Found" if found else "NOT FOUND"}')

# 验证两个文件一致
with open('miniprogram/data/ingredients.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)

print(f'\nFiles identical: {data == data2}')
