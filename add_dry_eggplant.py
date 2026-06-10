import json

with open('js/ingredients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取下一个ID
max_id = max(int(item['id'].split('_')[1]) for item in data['items'])
next_id = max_id + 1

# 添加干煸茄子
new_dish = {
    "id": f"item_{next_id:05d}",
    "name": "干煸茄子",
    "categories": ["cuisine_chuan", "meal_lunch", "meal_dinner", "food_vegetarian", "food_stirfry", "dish_main"]
}

data['items'].append(new_dish)
print(f'Added: {new_dish["name"]} (ID: {new_dish["id"]})')
print(f'Total items: {len(data["items"])}')

# 保存
json_str = json.dumps(data, ensure_ascii=False, indent=2)
with open('js/ingredients.json', 'w', encoding='utf-8') as f:
    f.write(json_str)
with open('miniprogram/data/ingredients.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

print('Files saved.')
