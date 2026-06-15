#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成二次删除名单（更严格标准）
保留真正全国常见的，删除其余地方性菜品
"""

import json
import os

BASE_DIR = "C:\\Users\\lin\\Downloads\\eatWhat"
DATA_FILE = os.path.join(BASE_DIR, "js", "ingredients_common.json")

# 读取数据
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

items = data['items']

# 明确保留名单（已全国流行，即使在小众菜系中）
KEEP_LIST = [
    # 滇菜 - 已全国流行
    '过桥米线', '米线', '酸辣米线', '野生菌火锅', '菠萝饭',
    # 黔菜 - 已全国流行
    '酸汤鱼', '辣子鸡',  # 注意：贵州辣子鸡与重庆辣子鸡不同，但辣子鸡已全国流行
    # 陕菜 - 已全国流行
    '肉夹馍', '凉皮', '油泼面', '羊肉泡馍', '臊子面', 'biangbiang面',
    # 山西菜 - 已全国流行
    '刀削面', '过油肉',
    # 甘肃菜 - 已全国流行
    '兰州拉面', '兰州牛肉面', '酿皮',
    # 新疆菜 - 已全国流行
    '新疆大盘鸡', '烤羊肉串', '馕', '抓饭',
    # 河南菜 - 已全国流行
    '烩面', '胡辣汤', '开封灌汤包',
    # 广西菜 - 已全国流行
    '螺蛳粉',
    # 闽菜 - 已全国流行
    '沙县小吃', '福州鱼丸', '沙茶面', '海蛎煎', '肉燕',
    # 徽菜 - 已全国流行（少）
    '黄山烧饼',  # 在电商/特产店常见
]

# 明确删除名单（地方性菜品）
REMOVE_LIST = [
    # 滇菜 - 地方性
    '腾冲大救驾', '曲靖蒸饵丝', '云南小锅米线', '宣威火腿炒饭',
    '蒙自过桥米线', '傣族竹筒饭', '昆明过桥米线', '饵块', '烧饵块',
    '大救驾', '饵丝', '鸡丝凉面', '凉拌木瓜丝', '云南玫瑰鲜花饼',
    '砂锅米线', '凉拌米线', '番茄米线', '竹筒饭',
    # 黔菜 - 地方性
    '盐酸菜', '豆豉鱼', '贵州豆腐丸子', '折耳根炒腊肉',
    '乌江鱼', '糟辣鱼', '贵州豆豉鱼', '折耳根炒肉',
    '贵州辣子鸡(黔菜)', '贵州酸汤鱼(黔菜)', '贵州豆腐丸子(黔菜)',
    '辣子鸡(黔菜)', '盐酸菜(黔菜)', '酸汤(黔菜)',
    # 陕菜 - 地方性
    '锅盔', '油泼扯面', '岐山臊子面', '陕西羊肉泡馍',
    '陕西凉皮', '陕西肉夹馍', '柿子饼', '肉夹馍(陕西)',
    '凉皮(陕西)', '臊子面(陕西)',
    # 山西菜 - 地方性
    '山西揪片', '山西猫耳朵', '山西莜面栲栳栳', '山西碗托',
    '莜面栲栳栳', '碗托', '碗团',
    # 甘肃菜 - 地方性
    '甘肃酿皮',
    # 新疆菜 - 地方性
    '新疆烤包子', '新疆拉条子', '新疆馕', '新疆抓饭',
    # 河南菜 - 地方性
    '河南烩面', '河南胡辣汤', '开封灌汤包',
    # 广西菜 - 地方性（螺蛳粉已保留）
    '广西酸笋炒肉',
    # 徽菜 - 地方性（只剩2个）
    '徽式烧饼',
    # 北京菜 - 地方性（豆汁等已删除，但可能还有遗漏）
    '北京卤煮', '北京炸酱面',  # 炸酱面已全国流行，但"北京炸酱面"可能地方性较强
    # 湖北菜 - 地方性
    '武汉热干面', '排骨藕汤', '洪山菜薹', '沔阳三蒸(已删)',
    # 其他地方性
    '德州扒鸡', '道口烧鸡(已删)', '符离集烧鸡',
]

# 分类
keep_items = []
remove_items = []
review_items = []

for item in items:
    name = item['name']
    
    # 检查是否在明确保留名单中
    if any(kw in name for kw in KEEP_LIST):
        keep_items.append(item)
        continue
    
    # 检查是否在明确删除名单中
    if any(kw in name for kw in REMOVE_LIST):
        remove_items.append({
            'id': item['id'],
            'name': name,
            'reason': '明确地方性菜品'
        })
        continue
    
    # 检查是否属于小众菜系且无全国流行证据
    categories = item.get('categories', [])
    minor_cuisines = ['cuisine_yunnan', 'cuisine_guizhou', 'cuisine_anhui',
                      'cuisine_shaanxi', 'cuisine_jin', 'cuisine_gansu',
                      'cuisine_guangxi', 'cuisine_jiangxi']
    
    if any(cat in minor_cuisines for cat in categories):
        review_items.append({
            'id': item['id'],
            'name': name,
            'categories': categories,
            'reason': '属于小众菜系，需审核'
        })
    else:
        # 其他：保留
        keep_items.append(item)

# 输出统计
print(f"当前总条目: {len(items)}")
print(f"\n分类结果:")
print(f"  明确保留: {len(keep_items)}")
print(f"  明确删除: {len(remove_items)}")
print(f"  需审核: {len(review_items)}")

# 保存删除名单
output_file = os.path.join(BASE_DIR, "removal_candidates_2nd.json")
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(remove_items, f, ensure_ascii=False, indent=2)
print(f"\n明确删除名单已保存到: {output_file}")
print(f"  共 {len(remove_items)} 个条目")

# 保存需审核名单
review_file = os.path.join(BASE_DIR, "review_candidates_2nd.json")
with open(review_file, 'w', encoding='utf-8') as f:
    json.dump(review_items, f, ensure_ascii=False, indent=2)
print(f"需审核名单已保存到: {review_file}")
print(f"  共 {len(review_items)} 个条目")

# 显示明确删除名单
print(f"\n明确删除名单 ({len(remove_items)} 个):")
for item in remove_items:
    print(f"  - {item['name']} (ID: {item['id']})")

# 显示需审核名单（前20个）
print(f"\n需审核名单 ({len(review_items)} 个)，显示前20个:")
for item in review_items[:20]:
    print(f"  - {item['name']} (ID: {item['id']}, 菜系: {item['categories']})")
