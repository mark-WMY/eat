#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze full-only items to find candidates for common promotion
and identify gaps in the database
"""
import json
from collections import Counter

with open('js/ingredients_common.json', 'r', encoding='utf-8') as f:
    common = json.load(f)
with open('js/ingredients_full.json', 'r', encoding='utf-8') as f:
    full = json.load(f)

common_names = {i['name'] for i in common['items']}
full_names = {i['name'] for i in full['items']}
full_only = [i for i in full['items'] if i['name'] not in common_names]

print("=" * 60)
print(f"Common items: {len(common['items'])}")
print(f"Full items: {len(full['items'])}")
print(f"Full-only items: {len(full_only)}")
print(f"Common is subset of full: {common_names.issubset(full_names)}")
print("=" * 60)

# Find max ID
max_id = 0
for item in full['items']:
    try:
        n = int(item['id'].replace('item_', ''))
        if n > max_id:
            max_id = n
    except:
        pass
print(f"Max existing ID: {max_id}")

# Categorize full-only items
def get_cuisine(item):
    for c in item['categories']:
        if c.startswith('cuisine_'):
            return c
    return 'cuisine_other'

by_cuisine = Counter()
for item in full_only:
    by_cuisine[get_cuisine(item)] += 1

print("\n--- Full-only items by cuisine ---")
for c, n in by_cuisine.most_common():
    print(f"  {c}: {n}")

# Find national/common items in full that should be promoted
# These are items from major Chinese cuisines that are well-known nationally
promote_candidates = []
regional_items = []

for item in full_only:
    cuisine = get_cuisine(item)
    name = item['name']
    
    # Skip non-Chinese cuisine items - those are for full only
    if cuisine in ['cuisine_french', 'cuisine_italian', 'cuisine_japanese', 'cuisine_korean',
                   'cuisine_american', 'cuisine_british', 'cuisine_german', 'cuisine_spanish',
                   'cuisine_greek', 'cuisine_mexican', 'cuisine_brazilian', 'cuisine_indian',
                   'cuisine_thai', 'cuisine_vietnamese', 'cuisine_malaysian', 'cuisine_singapore',
                   'cuisine_middle_eastern', 'cuisine_african', 'cuisine_western']:
        regional_items.append((name, cuisine))
        continue
    
    # Chinese cuisine items - check if nationally known
    # Items without city/region prefix from major cuisines are more likely to be national
    has_region_prefix = False
    region_prefixes = ['北京', '上海', '广州', '深圳', '重庆', '天津', '武汉', '南京',
                       '杭州', '成都', '西安', '长沙', '昆明', '贵阳', '兰州', '拉萨',
                       '乌鲁木齐', '沈阳', '大连', '青岛', '厦门', '福州', '南宁',
                       '海口', '哈尔滨', '长春', '郑州', '济南', '太原', '合肥',
                       '南昌', '银川', '西宁', '呼和浩特', '石家庄', '台北', '香港',
                       '澳门', '苏州', '无锡', '宁波', '温州', '绍兴', '嘉兴',
                       '金华', '台州', '泉州', '漳州', '莆田', '洛阳', '开封',
                       '安阳', '许昌', '南阳', '信阳', '荆州', '宜昌', '襄阳',
                       '桂林', '柳州', '遵义', '大理', '丽江', '曲靖', '腾冲',
                       '汉中', '延安', '咸阳', '大同', '运城', '忻州', '张掖',
                       '天水', '酒泉', '嘉峪关', '延吉', '延边', '凯里', '安顺',
                       '兴义', '荔波', '岐山', '潍坊', '德州', '临沂', '淄博',
                       '湘潭', '邵阳', '岳阳', '衡阳', '株洲', '湘西', '芜湖',
                       '马鞍山', '安庆', '黄山', '阜阳', '孝感', '黄石', '恩施',
                       '潜江', '公安', '镇江', '扬州', '徐州', '常州', '南通',
                       '宜宾', '达州', '自贡', '乐山', '泸州', '绵阳', '南充',
                       '遵义', '贵阳', '花溪', '遵义', '荔波', '陇西', '静宁',
                       '河西', '庆岭', '集安', '长白', '嘉峪关', '南山', '白市驿',
                       '军屯', '天河', '歌乐山', '璧山', '太安', '邮亭',
                       '老北京', '武汉', '昆明', '大理', '腾冲', '宜良',
                       '曲靖', '建水', '蒙自', '宣威', '贵阳', '花溪',
                       '凯里', '镇远', '贞丰', '安顺', '青岩', '荔波']
    
    for prefix in region_prefixes:
        if name.startswith(prefix):
            has_region_prefix = True
            break
    
    # Items like "盐水鸭", "叫花鸡" etc. that are well-known nationally but from specific region
    # These are on the boundary and need careful consideration
    well_known_national = [
        "盐水鸭", "无锡排骨", "叫花鸡", "松鼠鳜鱼", "狮子头", "大煮干丝",
        "东坡肉", "西湖醋鱼", "龙井虾仁", "宋嫂鱼羹",
        "佛跳墙", "荔枝肉", "醉排骨", "蚵仔煎", "面线糊",
        "腊味合蒸", "口味虾", "酱板鸭", "糖油粑土",
        "火腿炖甲鱼", "红烧果子狸", "腌鲜鳜鱼",
        "汽锅鸡", "酸汤鱼", "折耳根炒腊肉", "过桥米线",
        "清蒸武昌鱼", "排骨藕汤", "红菜苔炒腊肉",
        "糖醋鲤鱼", "锅塌豆腐", "奶汤蒲菜", "九转大肠", "油爆双脆",
        "白肉血肠", "锅包肉", "地三鲜", "小鸡炖蘑菇",
        "甑糕", "烤全羊", "手抓饭",
        "杀猪菜", "本帮熏鱼"
    ]
    
    if name in well_known_national:
        promote_candidates.append(name)
    elif has_region_prefix:
        regional_items.append((name, cuisine))
    else:
        # Without region prefix, likely more broadly known
        promote_candidates.append(name)

print(f"\n--- Promotion candidates (national common dishes) ---")
for n in sorted(promote_candidates):
    print(f"  {n}")
print(f"Total: {len(promote_candidates)}")

print(f"\n--- Regional items (stay in full only) ---")
for n, c in sorted(regional_items)[:30]:
    print(f"  {n} [{c}]")
print(f"Total: {len(regional_items)} (showing first 30)")

# Also check which common dishes from the previous scripts are already there
check_names = [
    "鸡蛋灌饼", "酱香饼", "烩面", "刀削面", "热干面", "炸酱面",
    "葱油拌面", "阳春面", "炒面", "炒饭", "蛋炒饭", "盖浇饭",
    "小笼包", "生煎包", "灌汤包", "叉烧包", "豆沙包", "肉夹馍",
    "煎饼果子", "葱油饼", "手抓饼", "韭菜盒子",
    "皮蛋瘦肉粥", "白粥", "八宝粥", "小米粥",
    "紫菜蛋花汤", "番茄蛋汤", "酸辣汤", "排骨汤", "鸡汤",
    "红烧肉", "糖醋排骨", "回锅肉", "鱼香肉丝", "宫保鸡丁",
    "麻婆豆腐", "水煮肉片", "水煮鱼", "辣子鸡", "口水鸡",
    "西红柿炒鸡蛋", "青椒肉丝", "木须肉",
    "酸辣土豆丝", "醋溜白菜", "手撕包菜", "蒜蓉西兰花",
    "可乐", "雪碧", "果汁", "奶茶", "珍珠奶茶",
    "咖啡", "拿铁", "绿茶", "红茶", "豆浆",
    "啤酒", "白酒", "红酒",
    "炸鸡", "薯条", "汉堡", "披萨", "意面", "牛排", "沙拉",
    "寿司", "三文鱼刺身", "味噌汤", "韩式烤肉", "石锅拌饭", "泡菜",
    "螺蛳粉", "酸辣粉", "凉皮", "胡辣汤", "肠粉",
    "皮蛋", "酱牛肉", "凉拌黄瓜",
    "蛋糕", "冰淇淋", "汤圆", "粽子", "月饼", "年糕",
    "麻辣烫", "烧烤", "烤羊肉串", "烤鱼",
    "臭豆腐", "冰糖葫芦", "糖炒栗子", "茶叶蛋",
]

print(f"\n--- Checking if common dishes already exist ---")
for n in sorted(check_names):
    status = "EXISTS" if n in common_names else "MISSING"
    print(f"  {status}: {n}")
