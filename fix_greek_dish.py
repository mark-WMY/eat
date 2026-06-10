import json

# 加载数据
with open('js/ingredients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 获取下一个ID
max_id = max(int(item['id'].split('_')[1]) for item in data['items'])
next_id = max_id + 1

# 添加缺失的希腊菜品（修正cuisine_id）
new_dish = {
    "id": f"item_{next_id:05d}",
    "name": "希腊烤肉串",
    "categories": ["cuisine_greek", "meal_lunch", "meal_dinner", "food_meat", "food_bbq", "dish_main"]
}

data['items'].append(new_dish)

print(f'Added new dish: {new_dish["name"]} (ID: {new_dish["id"]})')
print(f'Total items now: {len(data["items"])}')

# 保存文件
json_str = json.dumps(data, ensure_ascii=False, indent=2)

with open('js/ingredients.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

with open('miniprogram/data/ingredients.json', 'w', encoding='utf-8') as f:
    f.write(json_str)

print('Files saved.')

# 验证希腊菜数量
greek_count = sum(1 for item in data['items'] if 'cuisine_greek' in item['categories'])
print(f'Greek cuisine dishes: {greek_count}')
