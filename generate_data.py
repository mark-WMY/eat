#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
食材随机选择器 - 数据生成脚本
生成包含全球主流菜系的完整食物数据
"""

import json

def generate_categories():
    """生成分类数据"""

    # 1. 扩充菜系分类（中国八大菜系 + 国际主流菜系）
    cuisine = {
        # 中国八大菜系
        "川菜": {"id": "cuisine_chuan", "name": "川菜", "parentId": None},
        "鲁菜": {"id": "cuisine_lu", "name": "鲁菜", "parentId": None},
        "粤菜": {"id": "cuisine_yue", "name": "粤菜", "parentId": None},
        "苏菜": {"id": "cuisine_su", "name": "苏菜", "parentId": None},
        "浙菜": {"id": "cuisine_zhe", "name": "浙菜", "parentId": None},
        "闽菜": {"id": "cuisine_min", "name": "闽菜", "parentId": None},
        "湘菜": {"id": "cuisine_xiang", "name": "湘菜", "parentId": None},
        "徽菜": {"id": "cuisine_anhui", "name": "徽菜(皖)", "parentId": None},

        # 中国其他菜系
        "渝菜": {"id": "cuisine_yu", "name": "渝菜", "parentId": None},
        "京菜": {"id": "cuisine_beijing", "name": "京菜", "parentId": None},
        "沪菜": {"id": "cuisine_shanghai", "name": "沪菜", "parentId": None},
        "东北菜": {"id": "cuisine_dongbei", "name": "东北菜", "parentId": None},
        "西北菜": {"id": "cuisine_northwest", "name": "西北菜", "parentId": None},
        "云南菜": {"id": "cuisine_yunnan", "name": "云南菜", "parentId": None},
        "贵州菜": {"id": "cuisine_guizhou", "name": "贵州菜", "parentId": None},

        # 亚洲菜系
        "日式": {"id": "cuisine_japanese", "name": "日式", "parentId": None},
        "韩式": {"id": "cuisine_korean", "name": "韩式", "parentId": None},
        "泰式": {"id": "cuisine_thai", "name": "泰式", "parentId": None},
        "越式": {"id": "cuisine_vietnamese", "name": "越式", "parentId": None},
        "印度菜": {"id": "cuisine_indian", "name": "印度菜", "parentId": None},
        "新加坡菜": {"id": "cuisine_singapore", "name": "新加坡菜", "parentId": None},
        "马来西亚菜": {"id": "cuisine_malaysian", "name": "马来西亚菜", "parentId": None},

        # 欧洲菜系
        "意式": {"id": "cuisine_italian", "name": "意式", "parentId": None},
        "法式": {"id": "cuisine_french", "name": "法式", "parentId": None},
        "西班牙菜": {"id": "cuisine_spanish", "name": "西班牙菜", "parentId": None},
        "德式": {"id": "cuisine_german", "name": "德式", "parentId": None},
        "英式": {"id": "cuisine_british", "name": "英式", "parentId": None},
        "希腊菜": {"id": "cuisine_greek", "name": "希腊菜", "parentId": None},

        # 美洲菜系
        "美式": {"id": "cuisine_american", "name": "美式", "parentId": None},
        "墨西哥菜": {"id": "cuisine_mexican", "name": "墨西哥菜", "parentId": None},
        "巴西菜": {"id": "cuisine_brazilian", "name": "巴西菜", "parentId": None},

        # 其他
        "西餐": {"id": "cuisine_western", "name": "西餐", "parentId": None},
        "中东菜": {"id": "cuisine_middle_eastern", "name": "中东菜", "parentId": None},
        "非洲菜": {"id": "cuisine_african", "name": "非洲菜", "parentId": None},
        "其他": {"id": "cuisine_other", "name": "其他", "parentId": None}
    }

    # 2. 用餐时段
    meal_type = {
        "早餐": {"id": "meal_breakfast", "name": "早餐"},
        "午餐": {"id": "meal_lunch", "name": "午餐"},
        "晚餐": {"id": "meal_dinner", "name": "晚餐"},
        "夜宵": {"id": "meal_midnight", "name": "夜宵"},
        "下午茶": {"id": "meal_afternoon_tea", "name": "下午茶"}
    }

    # 3. 优化食材/食物类型
    food_type = {
        "荤菜": {"id": "food_meat", "name": "荤菜"},
        "素菜": {"id": "food_vegetarian", "name": "素菜"},
        "海鲜": {"id": "food_seafood", "name": "海鲜"},
        "禽类": {"id": "food_poultry", "name": "禽类"},
        "牛肉": {"id": "food_beef", "name": "牛肉"},
        "猪肉": {"id": "food_pork", "name": "猪肉"},
        "羊肉": {"id": "food_lamb", "name": "羊肉"},
        "汤羹": {"id": "food_soup", "name": "汤羹"},
        "粥品": {"id": "food_congee", "name": "粥品"},
        "煲仔": {"id": "food_stew", "name": "煲仔"},
        "饭类": {"id": "food_rice", "name": "饭类"},
        "面食": {"id": "food_noodles", "name": "面食"},
        "饺子": {"id": "food_dumpling", "name": "饺子"},
        "包子": {"id": "food_bun", "name": "包子"},
        "饼类": {"id": "food_pancake", "name": "饼类"},
        "烧烤": {"id": "food_bbq", "name": "烧烤"},
        "火锅": {"id": "food_hotpot", "name": "火锅"},
        "炒菜": {"id": "food_stirfry", "name": "炒菜"},
        "凉菜": {"id": "food_cold", "name": "凉菜"},
        "甜点": {"id": "food_dessert", "name": "甜点"},
        "饮品": {"id": "food_beverage", "name": "饮品"},
        "小吃": {"id": "food_snack", "name": "小吃"},
        "杂粮": {"id": "food_wholegrain", "name": "杂粮"}
    }

    # 4. 新增餐品类型维度
    dish_type = {
        "主食": {"id": "dish_staple", "name": "主食"},
        "正餐": {"id": "dish_main", "name": "正餐"},
        "小吃": {"id": "dish_snack", "name": "小吃"},
        "甜点": {"id": "dish_dessert", "name": "甜点"},
        "饮品": {"id": "dish_beverage", "name": "饮品"},
        "汤品": {"id": "dish_soup", "name": "汤品"},
        "前菜": {"id": "dish_appetizer", "name": "前菜"},
        "沙拉": {"id": "dish_salad", "name": "沙拉"}
    }

    return {
        "cuisine": cuisine,
        "mealType": meal_type,
        "foodType": food_type,
        "dishType": dish_type
    }


def generate_items():
    """生成食物条目 - 全球主流成品菜肴"""

    items = []
    item_id = 1

    # ==================== 川菜 ====================
    chuan_dishes = [
        ("宫保鸡丁", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stirfry"], ["dish_main"]),
        ("鱼香肉丝", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("水煮牛肉", ["meal_lunch", "meal_dinner"], ["food_beef", "food_stirfry"], ["dish_main"]),
        ("麻婆豆腐", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("回锅肉", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("辣子鸡丁", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stirfry"], ["dish_main"]),
        ("夫妻肺片", ["meal_lunch", "meal_dinner"], ["food_meat", "food_cold"], ["dish_main", "dish_appetizer"]),
        ("口水鸡", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_cold"], ["dish_main"]),
        ("樟茶鸭", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("担担面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("钟水饺", ["meal_breakfast", "meal_lunch"], ["food_dumpling"], ["dish_staple"]),
        ("龙抄手", ["meal_breakfast", "meal_lunch"], ["food_dumpling"], ["dish_staple"]),
        ("串串香", ["meal_dinner", "meal_midnight"], ["food_hotpot", "food_meat"], ["dish_main"]),
        ("冒菜", ["meal_lunch", "meal_dinner"], ["food_meat", "food_vegetarian"], ["dish_main"]),
        ("毛血旺", ["meal_lunch", "meal_dinner"], ["food_meat", "food_seafood"], ["dish_main"]),
        ("酸菜鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("泡椒牛蛙", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_main"]),
        ("干煸四季豆", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("红油抄手", ["meal_breakfast", "meal_lunch"], ["food_dumpling"], ["dish_staple"]),
        ("宜宾燃面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
    ]

    for name, meals, foods, dishes in chuan_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_chuan"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 鲁菜 ====================
    lu_dishes = [
        ("糖醋鲤鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("九转大肠", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("爆炒腰花", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("葱烧海参", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("德州扒鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("济南把子肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("锅塌豆腐", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("奶汤蒲菜", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_main", "dish_soup"]),
        ("油爆双脆", ["meal_lunch", "meal_dinner"], ["food_meat", "food_stirfry"], ["dish_main"]),
        ("清汤燕菜", ["meal_lunch", "meal_dinner"], ["food_meat", "food_soup"], ["dish_main", "dish_soup"]),
    ]

    for name, meals, foods, dishes in lu_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_lu"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 粤菜 ====================
    yue_dishes = [
        ("白切鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("烧鹅", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("叉烧", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("蜜汁叉烧", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("豉汁蒸排骨", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("清蒸石斑鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("虾饺", ["meal_breakfast", "meal_lunch"], ["food_seafood", "food_dumpling"], ["dish_staple"]),
        ("烧卖", ["meal_breakfast", "meal_lunch"], ["food_meat", "food_dumpling"], ["dish_staple"]),
        ("肠粉", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("云吞面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("煲仔饭", ["meal_lunch", "meal_dinner"], ["food_rice", "food_stew"], ["dish_staple"]),
        ("老火靓汤", ["meal_lunch", "meal_dinner"], ["food_soup"], ["dish_soup"]),
        ("皮蛋瘦肉粥", ["meal_breakfast"], ["food_congee", "food_pork"], ["dish_staple"]),
        ("及第粥", ["meal_breakfast"], ["food_congee"], ["dish_staple"]),
        ("凤爪", ["meal_breakfast", "meal_lunch"], ["food_poultry"], ["dish_snack"]),
        ("糯米鸡", ["meal_breakfast", "meal_lunch"], ["food_rice", "food_poultry"], ["dish_staple"]),
        ("干炒牛河", ["meal_lunch", "meal_dinner"], ["food_beef", "food_noodles"], ["dish_staple"]),
        ("湿炒牛河", ["meal_lunch", "meal_dinner"], ["food_beef", "food_noodles"], ["dish_staple"]),
        ("咕噜肉", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("蚝油生菜", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in yue_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_yue"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 苏菜 ====================
    su_dishes = [
        ("松鼠桂鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("狮子头", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("大煮干丝", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("盐水鸭", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("响油鳝糊", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("无锡排骨", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("叫花鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("阳澄湖大闸蟹", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("扬州炒饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("小笼包", ["meal_breakfast", "meal_lunch"], ["food_bun", "food_pork"], ["dish_staple"]),
    ]

    for name, meals, foods, dishes in su_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_su"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 浙菜 ====================
    zhe_dishes = [
        ("西湖醋鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("东坡肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("龙井虾仁", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("宋嫂鱼羹", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_soup"], ["dish_main", "dish_soup"]),
        ("叫化童鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("干炸响铃", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("宁波汤圆", ["meal_breakfast", "meal_dinner"], ["food_dessert"], ["dish_dessert"]),
        ("嘉兴粽子", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("杭州小笼包", ["meal_breakfast", "meal_lunch"], ["food_bun"], ["dish_staple"]),
        ("片儿川", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
    ]

    for name, meals, foods, dishes in zhe_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_zhe"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 闽菜 ====================
    min_dishes = [
        ("佛跳墙", ["meal_lunch", "meal_dinner"], ["food_meat", "food_seafood", "food_stew"], ["dish_main"]),
        ("荔枝肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("醉排骨", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("沙县拌面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("沙县扁肉", ["meal_breakfast", "meal_lunch"], ["food_dumpling"], ["dish_staple"]),
        ("蚵仔煎", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_snack"]),
        ("土笋冻", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_snack"]),
        ("面线糊", ["meal_breakfast"], ["food_noodles"], ["dish_staple"]),
        ("海蛎饼", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_pancake"], ["dish_snack"]),
        ("光饼夹糟肉", ["meal_lunch", "meal_dinner"], ["food_pork", "food_pancake"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in min_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_min"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 湘菜 ====================
    xiang_dishes = [
        ("剁椒鱼头", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("辣椒炒肉", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("永州血鸭", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("东安子鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("腊味合蒸", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_main"]),
        ("湘西外婆菜", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("长沙臭豆腐", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_vegetarian"], ["dish_snack"]),
        ("口味虾", ["meal_dinner", "meal_midnight"], ["food_seafood"], ["dish_main"]),
        ("毛氏红烧肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("攸县香干", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in xiang_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_xiang"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 徽菜 ====================
    anhui_dishes = [
        ("徽州臭鳜鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("徽州毛豆腐", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("黄山炖鸽", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stew"], ["dish_main"]),
        ("问政山笋", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("李鸿章杂烩", ["meal_lunch", "meal_dinner"], ["food_meat", "food_seafood"], ["dish_main"]),
        ("虎皮毛豆腐", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("徽州饼", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("包袱饺", ["meal_breakfast", "meal_lunch"], ["food_dumpling"], ["dish_staple"]),
        ("腊八豆腐", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("清蒸鹰龟", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in anhui_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_anhui"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 其他中国菜系 ====================
    other_chinese_dishes = [
        # 渝菜
        ("重庆火锅", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_hotpot", "food_meat"], ["dish_main"]),
        ("万州烤鱼", ["meal_dinner", "meal_midnight"], ["food_seafood"], ["dish_main"]),
        ("黔江鸡杂", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),

        # 京菜
        ("北京烤鸭", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("炸酱面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("京酱肉丝", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("驴打滚", ["meal_breakfast", "meal_afternoon_tea"], ["food_dessert"], ["dish_dessert", "dish_snack"]),
        ("豌豆黄", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),

        # 沪菜
        ("上海小笼包", ["meal_breakfast", "meal_lunch"], ["food_bun"], ["dish_staple"]),
        ("生煎包", ["meal_breakfast", "meal_lunch"], ["food_bun"], ["dish_staple"]),
        ("红烧肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("本帮熏鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("蟹壳黄", ["meal_afternoon_tea"], ["food_snack"], ["dish_snack"]),

        # 东北菜
        ("锅包肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("地三鲜", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("小鸡炖蘑菇", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stew"], ["dish_main"]),
        ("猪肉炖粉条", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("东北乱炖", ["meal_lunch", "meal_dinner"], ["food_meat", "food_vegetarian", "food_stew"], ["dish_main"]),
        ("溜肉段", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("杀猪菜", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("冷面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),

        # 西北菜
        ("羊肉泡馍", ["meal_breakfast", "meal_lunch"], ["food_lamb", "food_pancake"], ["dish_staple"]),
        ("肉夹馍", ["meal_breakfast", "meal_lunch"], ["food_pork", "food_pancake"], ["dish_staple"]),
        ("凉皮", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple", "dish_snack"]),
        ("biangbiang面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("手抓羊肉", ["meal_lunch", "meal_dinner"], ["food_lamb"], ["dish_main"]),
        ("大盘鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("烤羊肉串", ["meal_dinner", "meal_midnight"], ["food_lamb", "food_bbq"], ["dish_snack"]),
        ("酿皮子", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),

        # 云南菜
        ("过桥米线", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("汽锅鸡", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stew"], ["dish_main"]),
        ("宣威火腿", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("傣味手抓饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("菌菇火锅", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_hotpot"], ["dish_main"]),
        ("破酥粑粑", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),

        # 贵州菜
        ("酸汤鱼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("丝娃娃", ["meal_lunch", "meal_dinner"], ["food_pancake", "food_vegetarian"], ["dish_main"]),
        ("肠旺面", ["meal_breakfast"], ["food_noodles"], ["dish_staple"]),
        ("恋爱豆腐果", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("折耳根炒腊肉", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in other_chinese_dishes:
        cuisine_map = {
            "重庆": "cuisine_yu",
            "北京": "cuisine_beijing",
            "上海": "cuisine_shanghai",
            "东北": "cuisine_dongbei",
            "西北": "cuisine_northwest",
            "云南": "cuisine_yunnan",
            "贵州": "cuisine_guizhou"
        }
        cuisine_id = "cuisine_other"
        for key, val in cuisine_map.items():
            if key in name:
                cuisine_id = val
                break

        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": [cuisine_id] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 日式料理 ====================
    japanese_dishes = [
        ("寿司拼盘", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_rice"], ["dish_main"]),
        ("刺身拼盘", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main", "dish_appetizer"]),
        ("天妇罗", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_vegetarian"], ["dish_main"]),
        ("拉面", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("乌冬面", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("荞麦面", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("丼饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("亲子丼", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_rice"], ["dish_staple"]),
        ("牛丼", ["meal_lunch", "meal_dinner"], ["food_beef", "food_rice"], ["dish_staple"]),
        ("猪排饭", ["meal_lunch", "meal_dinner"], ["food_pork", "food_rice"], ["dish_staple"]),
        ("照烧鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("寿喜烧", ["meal_lunch", "meal_dinner"], ["food_beef", "food_hotpot"], ["dish_main"]),
        ("章鱼小丸子", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_seafood"], ["dish_snack"]),
        ("大阪烧", ["meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("味噌汤", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_soup"], ["dish_soup"]),
        ("纳豆", ["meal_breakfast"], ["food_vegetarian"], ["dish_staple"]),
        ("玉子烧", ["meal_breakfast"], ["food_vegetarian"], ["dish_staple"]),
        ("关东煮", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_meat", "food_seafood"], ["dish_snack"]),
        ("抹茶冰淇淋", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("大福", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ]

    for name, meals, foods, dishes in japanese_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_japanese"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 韩式料理 ====================
    korean_dishes = [
        ("泡菜", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("石锅拌饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("冷面", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("烤肉", ["meal_lunch", "meal_dinner"], ["food_beef", "food_pork", "food_bbq"], ["dish_main"]),
        ("炸鸡", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_poultry"], ["dish_main"]),
        ("部队锅", ["meal_lunch", "meal_dinner"], ["food_meat", "food_stew"], ["dish_main"]),
        ("大酱汤", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_soup"], ["dish_soup"]),
        ("参鸡汤", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_soup"], ["dish_main", "dish_soup"]),
        ("紫菜包饭", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("年糕", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_snack"], ["dish_snack"]),
        ("煎饼", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("辣炒年糕", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_snack"], ["dish_snack"]),
        ("米酒", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
        ("韩式豆腐汤", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_main", "dish_soup"]),
        ("烤五花肉", ["meal_lunch", "meal_dinner"], ["food_pork", "food_bbq"], ["dish_main"]),
    ]

    for name, meals, foods, dishes in korean_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_korean"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 泰式料理 ====================
    thai_dishes = [
        ("冬阴功汤", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_soup"], ["dish_main", "dish_soup"]),
        ("绿咖喱鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("红咖喱牛肉", ["meal_lunch", "meal_dinner"], ["food_beef"], ["dish_main"]),
        ("泰式炒河粉", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("芒果糯米饭", ["meal_afternoon_tea"], ["food_dessert", "food_rice"], ["dish_dessert"]),
        ("青木瓜沙拉", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("泰式奶茶", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("椰汁西米糕", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("泰式春卷", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_appetizer"]),
        ("菠萝炒饭", ["meal_lunch", "meal_dinner"], ["food_rice", "food_seafood"], ["dish_staple"]),
    ]

    for name, meals, foods, dishes in thai_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_thai"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 越式料理 ====================
    vietnamese_dishes = [
        ("越南河粉", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("越南春卷", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_appetizer"]),
        ("法棍三明治", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("越南咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("顺化牛肉粉", ["meal_breakfast", "meal_lunch"], ["food_noodles", "food_beef"], ["dish_staple"]),
        ("西贡虾饼", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_snack"]),
    ]

    for name, meals, foods, dishes in vietnamese_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_vietnamese"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 印度菜 ====================
    indian_dishes = [
        ("黄油鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("咖喱羊肉", ["meal_lunch", "meal_dinner"], ["food_lamb"], ["dish_main"]),
        ("玛萨拉 dosa", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("烤馕", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("印度奶茶", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("蔬菜咖喱", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("比尔亚尼饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("萨莫萨三角饺", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
    ]

    for name, meals, foods, dishes in indian_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_indian"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 新加坡/马来西亚菜 ====================
    singapore_malaysian_dishes = [
        ("海南鸡饭", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_rice"], ["dish_staple"]),
        ("叻沙", ["meal_breakfast", "meal_lunch"], ["food_noodles", "food_seafood"], ["dish_staple"]),
        ("肉骨茶", ["meal_breakfast", "meal_lunch"], ["food_pork", "food_soup"], ["dish_main", "dish_soup"]),
        ("炒粿条", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("satay", ["meal_dinner", "meal_midnight"], ["food_meat", "food_bbq"], ["dish_snack"]),
        ("椰浆饭", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("娘惹糕", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("榴莲泡芙", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ]

    for name, meals, foods, dishes in singapore_malaysian_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_singapore"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 意式料理 ====================
    italian_dishes = [
        ("玛格丽特披萨", ["meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("意大利面", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("肉酱面", ["meal_lunch", "meal_dinner"], ["food_beef", "food_noodles"], ["dish_staple"]),
        ("奶油培根面", ["meal_lunch", "meal_dinner"], ["food_pork", "food_noodles"], ["dish_staple"]),
        ("千层面", ["meal_lunch", "meal_dinner"], ["food_meat", "food_pasta"], ["dish_staple"]),
        ("提拉米苏", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("意式冰淇淋", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("卡布奇诺", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("拿铁咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("意式浓缩咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("凯撒沙拉", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("帕尔马火腿", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_appetizer"]),
        ("烩饭", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("番茄罗勒汤", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
    ]

    for name, meals, foods, dishes in italian_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_italian"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 法式料理 ====================
    french_dishes = [
        ("可颂面包", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("法式吐司", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("洋葱汤", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("蜗牛", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_appetizer"]),
        ("鹅肝", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_appetizer"]),
        ("牛排", ["meal_lunch", "meal_dinner"], ["food_beef"], ["dish_main"]),
        ("红酒炖牛肉", ["meal_lunch", "meal_dinner"], ["food_beef", "food_stew"], ["dish_main"]),
        ("马赛鱼汤", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_soup"], ["dish_main", "dish_soup"]),
        ("马卡龙", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("焦糖布丁", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("拿破仑蛋糕", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("法式咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ]

    for name, meals, foods, dishes in french_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_french"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 西班牙菜 ====================
    spanish_dishes = [
        ("海鲜饭", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_rice"], ["dish_staple"]),
        ("tapas", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack", "dish_appetizer"]),
        ("伊比利亚火腿", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_appetizer"]),
        ("西班牙油条", ["meal_breakfast"], ["food_snack"], ["dish_snack"]),
        ("桑格利亚汽酒", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
    ]

    for name, meals, foods, dishes in spanish_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_spanish"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 德式料理 ====================
    german_dishes = [
        ("烤猪肘", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("香肠拼盘", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("德国啤酒", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
        ("碱水面包", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("苹果卷", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ]

    for name, meals, foods, dishes in german_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_german"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 美式料理 ====================
    american_dishes = [
        ("汉堡包", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pork", "food_beef"], ["dish_staple"]),
        ("热狗", ["meal_breakfast", "meal_lunch"], ["food_pork"], ["dish_staple"]),
        ("炸鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("肋排", ["meal_lunch", "meal_dinner"], ["food_pork", "food_bbq"], ["dish_main"]),
        ("薯条", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
        ("可乐", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_beverage"], ["dish_beverage"]),
        ("奶昔", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("布朗尼", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("芝士蛋糕", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("苹果派", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("pancakes", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("华夫饼", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("培根鸡蛋", ["meal_breakfast"], ["food_pork"], ["dish_staple"]),
        ("牛排", ["meal_lunch", "meal_dinner"], ["food_beef"], ["dish_main"]),
        ("凯撒沙拉", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
    ]

    for name, meals, foods, dishes in american_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_american"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 墨西哥菜 ====================
    mexican_dishes = [
        ("tacos", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("burritos", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("玉米片", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
        ("鳄梨酱", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("墨西哥卷饼", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
    ]

    for name, meals, foods, dishes in mexican_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_mexican"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 西式通用 ====================
    western_dishes = [
        ("三明治", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("沙拉", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("牛排", ["meal_lunch", "meal_dinner"], ["food_beef"], ["dish_main"]),
        ("烤鸡", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("奶油蘑菇汤", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("薯条", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
        ("咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("红茶", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ]

    for name, meals, foods, dishes in western_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_western"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 中东菜 ====================
    middle_eastern_dishes = [
        ("法拉费", ["meal_breakfast", "meal_lunch"], ["food_vegetarian"], ["dish_snack"]),
        ("胡姆斯", ["meal_breakfast", "meal_lunch"], ["food_vegetarian"], ["dish_snack"]),
        ("沙威玛", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_staple"]),
        ("皮塔饼", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("土耳其咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ]

    for name, meals, foods, dishes in middle_eastern_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_middle_eastern"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 早餐专用 ====================
    breakfast_dishes = [
        ("豆浆油条", ["meal_breakfast"], ["food_snack"], ["dish_staple"]),
        ("豆腐脑", ["meal_breakfast"], ["food_vegetarian"], ["dish_staple"]),
        ("茶叶蛋", ["meal_breakfast"], ["food_poultry"], ["dish_snack"]),
        ("包子", ["meal_breakfast"], ["food_bun"], ["dish_staple"]),
        ("馒头", ["meal_breakfast"], ["food_bun"], ["dish_staple"]),
        ("花卷", ["meal_breakfast"], ["food_bun"], ["dish_staple"]),
        ("烧饼", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("煎饼果子", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("小米粥", ["meal_breakfast"], ["food_congee"], ["dish_staple"]),
        ("八宝粥", ["meal_breakfast"], ["food_congee"], ["dish_staple"]),
        ("牛奶", ["meal_breakfast"], ["food_beverage"], ["dish_beverage"]),
        ("酸奶", ["meal_breakfast"], ["food_beverage"], ["dish_beverage"]),
        ("果汁", ["meal_breakfast"], ["food_beverage"], ["dish_beverage"]),
        ("麦片", ["meal_breakfast"], ["food_wholegrain"], ["dish_staple"]),
        ("面包", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("黄油", ["meal_breakfast"], ["food_snack"], ["dish_snack"]),
        ("果酱", ["meal_breakfast"], ["food_snack"], ["dish_snack"]),
    ]

    for name, meals, foods, dishes in breakfast_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_other"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 小吃/夜宵 ====================
    snack_dishes = [
        ("炸鸡柳", ["meal_midnight"], ["food_poultry", "food_bbq"], ["dish_snack"]),
        ("烤串", ["meal_midnight"], ["food_meat", "food_bbq"], ["dish_snack"]),
        ("麻辣烫", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_meat", "food_vegetarian"], ["dish_main"]),
        ("关东煮", ["meal_midnight"], ["food_meat", "food_seafood"], ["dish_snack"]),
        ("卤味", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_meat"], ["dish_snack"]),
        ("鸭脖", ["meal_midnight"], ["food_poultry"], ["dish_snack"]),
        ("鸡爪", ["meal_midnight"], ["food_poultry"], ["dish_snack"]),
        ("花生毛豆", ["meal_midnight"], ["food_vegetarian"], ["dish_snack"]),
        ("凉拌黄瓜", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_cold"], ["dish_appetizer"]),
        ("拍黄瓜", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_cold"], ["dish_appetizer"]),
    ]

    for name, meals, foods, dishes in snack_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_other"] + meals + foods + dishes
        })
        item_id += 1

    # ==================== 甜点/饮品 ====================
    dessert_beverage_dishes = [
        ("奶茶", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("咖啡", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("果汁", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("冰淇淋", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("蛋糕", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("饼干", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("巧克力", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("水果沙拉", ["meal_afternoon_tea"], ["food_vegetarian", "food_salad"], ["dish_salad", "dish_dessert"]),
        ("绿豆汤", ["meal_afternoon_tea"], ["food_soup"], ["dish_soup", "dish_dessert"]),
        ("红豆沙", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ]

    for name, meals, foods, dishes in dessert_beverage_dishes:
        items.append({
            "id": f"item_{item_id:05d}",
            "name": name,
            "categories": ["cuisine_other"] + meals + foods + dishes
        })
        item_id += 1

    return items


def main():
    """主函数"""
    data = {
        "categories": generate_categories(),
        "items": generate_items()
    }

    # 输出JSON文件
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    # 写入两个文件
    with open('js/ingredients.json', 'w', encoding='utf-8') as f:
        f.write(json_str)

    with open('miniprogram/data/ingredients.json', 'w', encoding='utf-8') as f:
        f.write(json_str)

    print(f"数据生成完成！")
    print(f"总条目数: {len(data['items'])}")
    print(f"菜系数: {len(data['categories']['cuisine'])}")
    print(f"用餐时段数: {len(data['categories']['mealType'])}")
    print(f"食材类型数: {len(data['categories']['foodType'])}")
    print(f"餐品类型数: {len(data['categories']['dishType'])}")


if __name__ == '__main__':
    main()
