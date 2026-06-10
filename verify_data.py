import json

data = json.load(open('js/ingredients.json', encoding='utf-8'))
print('Items count:', len(data['items']))
print('Categories:')
for k, v in data['categories'].items():
    print(f'  {k}: {len(v)} items')
print('\nFirst 5 items:')
for i in data['items'][:5]:
    print(f'  {i["name"]}')

# Check if both files are identical
data2 = json.load(open('miniprogram/data/ingredients.json', encoding='utf-8'))
print('\nFiles are identical:', data == data2)
