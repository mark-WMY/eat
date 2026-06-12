import json
with open('c:/Users/lin/Downloads/eatWhat/js/ingredients.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print('Total:', len(data['items']))
for item in data['items'][-10:]:
    print(f"{item['id']}: {item['name']}")