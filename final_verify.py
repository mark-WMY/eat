import json

with open('js/ingredients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计
cuisine_count = {}
for item in data['items']:
    for cat in item['categories']:
        if cat.startswith('cuisine_'):
            cuisine_count[cat] = cuisine_count.get(cat, 0) + 1

all_cuisines = {v['id']: v['name'] for k, v in data['categories']['cuisine'].items()}

print('=== Final Verification ===')
print(f'Total items: {len(data["items"])}')
print(f'Total cuisines: {len(all_cuisines)}')

# 检查所有菜系是否至少有5个菜品
all_ok = True
for cid, cname in all_cuisines.items():
    count = cuisine_count.get(cid, 0)
    if count < 5:
        print(f'WARNING: {cname} has only {count} dishes')
        all_ok = False

if all_ok:
    print('All cuisines have >= 5 dishes: YES')

# 检查目标菜品
target_dishes = ['辣椒炒鸡蛋', '红烧肉', '干煸茄子', '番茄炒蛋', '酸辣土豆丝', '可乐鸡翅', '糖醋排骨']
item_names = [item['name'] for item in data['items']]
print(f'\n=== Target Dishes ===')
for dish in target_dishes:
    found = dish in item_names
    status = 'OK' if found else 'MISSING'
    print(f'  {dish}: {status}')

# 文件一致性
with open('miniprogram/data/ingredients.json', 'r', encoding='utf-8') as f:
    data2 = json.load(f)
print(f'\nFiles identical: {data == data2}')

print('\n=== DONE ===')
