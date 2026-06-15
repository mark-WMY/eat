#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
筛选中国国内省份日常常见的家常菜或大众饮品
判断依据：网络上的大众认知与普遍记录（菜品在各省份餐馆、家庭餐桌上的出现频率、网络菜谱收录情况等）
不使用：菜系归属、烹饪工艺或食材属性作为判断标准
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 基于网络大众认知，以下是中国各省份日常常见的家常菜或大众饮品
# 这些菜品/饮品在各大菜谱网站（下厨房、美食杰等）有高频收录，且在家庭餐桌和餐馆中常见
COMMON_DISH_IDS = {
    # 新疆/西北菜品 - 在当地家庭常见
    "item_01669",  # 新疆馕包肉
    "item_02195",  # 乌鲁木齐烤羊肉
    "item_01667",  # 新疆烤羊肉串
    "item_03228",  # 红柳烤肉
    
    # 河南菜品 - 在当地家庭常见
    "item_01680",  # 河南道口烧鸡
    "item_02795",  # 道口烧鸡
    "item_02796",  # 黄河大鲤鱼
    
    # 湖北菜品 - 在当地家庭常见
    "item_02108",  # 沔阳三蒸
    "item_03214",  # 黄陂三合
    "item_01665",  # 黄陂三鲜
    "item_02111",  # 面窝
    "item_01664",  # 武汉面窝
    "item_03020",  # 豆皮(武汉)
    
    # 陕西菜品 - 在当地家庭常见
    "item_03222",  # 金线油塔
    "item_03224",  # 石子馍
    "item_01677",  # 山西碗托
    "item_02798",  # 柿子饼
    "item_02799",  # 黄桂柿子饼
    "item_02806",  # 碗托
    "item_02807",  # 碗团
    
    # 山西菜品 - 在当地家庭常见
    "item_02805",  # 平遥牛肉
    
    # 甘肃/西北菜品 - 在当地家庭常见
    "item_03221",  # 洋芋搅团
    
    # 广西菜品 - 在当地家庭常见
    "item_03244",  # 螺蛳鸭脚煲
    "item_03238",  # 酸嘢
    "item_03240",  # 玉林牛巴
    "item_03241",  # 柠檬鸭
    "item_03243",  # 南宁老友粉
    
    # 全国性流行菜品 - 多省份餐馆和家庭常见
    "item_03029",  # 小龙虾(麻辣)
    "item_03030",  # 小龙虾(蒜蓉)
    "item_03031",  # 小龙虾(十三香)
    "item_03047",  # 纸包鱼
    "item_02193",  # 重庆麻辣火锅
}


def main():
    # 读取源文件
    with open('ingredients_full.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)
    
    # 读取目标文件
    with open('ingredients_common.json', 'r', encoding='utf-8') as f:
        common_data = json.load(f)
    
    # 获取已存在的item id，避免重复
    existing_ids = {item['id'] for item in common_data['items']}
    
    # 筛选符合条件的条目
    common_items = []
    skipped_items = []
    
    for item in full_data['items']:
        if item['id'] in existing_ids:
            continue  # 已存在，跳过
        
        if item['id'] in COMMON_DISH_IDS:
            common_items.append(item)
            existing_ids.add(item['id'])
        else:
            skipped_items.append(item['name'])
    
    # 追加到目标列表
    common_data['items'].extend(common_items)
    
    # 写回文件
    with open('ingredients_common.json', 'w', encoding='utf-8') as f:
        json.dump(common_data, f, ensure_ascii=False, indent=2)
    
    print(f"处理了 {len(full_data['items'])} 个条目")
    print(f"找到 {len(common_items)} 个常见家常菜/大众饮品，已添加到目标文件")
    print(f"目标文件现在有 {len(common_data['items'])} 个条目")
    print()
    print("添加的条目:")
    for item in common_items:
        print(f"  - {item['name']} (id: {item['id']})")
    print()
    print(f"跳过（非常见家常菜）的条目数: {len(skipped_items)}")


if __name__ == '__main__':
    main()
