#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
process_dishes.py - 全面审核、修复并扩充 dishes 数据。

功能：
  1. 为缺失 id 的条目分配 id
  2. 修复菜名（清除后缀、修正品牌名等）
  3. 审核并修正 cuisine / foodType / mealType / dishType
  4. 审核并修正 health 标签（删除不健康菜品上的健康标签）
  5. 新增 300+ 道各地及国际菜品
  6. 保存回 ingredients.json
"""

import json
import os
import re
import copy

# ====================== 路径 ======================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(BASE_DIR, "js", "ingredients.json")
OUT_PATH = SRC_PATH  # 直接覆盖（建议先备份）

# ====================== 加载数据 ======================
def load_data():
    with open(SRC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存到 {OUT_PATH}")

# ====================== 类别 ID 速查 ======================
# 从 categories 自动构建
def build_category_maps(categories):
    """从 categories 构建 {id: name} 和 {name: id} 映射"""
    id_to_name = {}
    name_to_id = {}
    for group_name, group in categories.items():
        for name, info in group.items():
            cid = info["id"]
            id_to_name[cid] = name
            name_to_id[name] = cid
    return id_to_name, name_to_id

# ====================== 步骤1: 分配缺失的 ID ======================
def fix_missing_ids(data):
    """为没有 id 的 item 分配新 id"""
    max_num = 0
    for item in data["items"]:
        if "id" in item:
            m = re.search(r"item_(\d+)", item["id"])
            if m:
                max_num = max(max_num, int(m.group(1)))
    
    fixed = 0
    for item in data["items"]:
        if "id" not in item:
            max_num += 1
            item["id"] = f"item_{max_num:05d}"
            fixed += 1
        if "attributes" not in item:
            item["attributes"] = {"health": [], "allergens": []}
    
    print(f"  已修复 {fixed} 个缺失 id 的条目")
    return data

# ====================== 步骤2: 名称修正 ======================
NAME_FIXES = {
    # 品牌名/品种名简化为通用名
    "红富士苹果": "苹果",
    "红富士": "苹果",
    "富士苹果": "苹果",
    
    # 去掉多余后缀
    "酸菜鱼-正宗": "酸菜鱼",
    "酸菜鱼-老坛": "酸菜鱼",
    
    # 常见错误/缩写修正
    "黄闷鸡": "黄焖鸡",
    "黄闷鸡米饭": "黄焖鸡米饭",
    "黄焖鸡": "黄焖鸡",
    
    # 修正错别字
    "宫爆鸡丁": "宫保鸡丁",
    "鱼香肉丝-正宗": "鱼香肉丝",
    "麻婆豆付": "麻婆豆腐",
    "糖醋里脊-正宗": "糖醋里脊",
    "锅包肉-正宗": "锅包肉",
    
    # 统一命名
    "西红柿炒蛋": "番茄炒蛋",
    "西红柿炒鸡蛋": "番茄炒蛋",
    "西红柿蛋汤": "番茄蛋汤",
    "番茄炒鸡蛋": "番茄炒蛋",
    
    # 去掉冗余的"菜"字后缀（在已明确的菜名中）
    # 保留...
}

def fix_name(name):
    """修正菜名"""
    name = name.strip()
    # 精确替换
    if name in NAME_FIXES:
        return NAME_FIXES[name]
    
    # 去掉 "-正宗" "-老坛" "-家常" 等后缀
    for suffix in ["-正宗", "-老坛", "-家常版", "-经典", "-秘制", "-招牌"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break
    
    # 去掉多余空格
    name = re.sub(r'\s+', '', name)
    
    return name

def apply_name_fixes(data):
    """对所有条目应用名称修正"""
    fixed = 0
    for item in data["items"]:
        old_name = item["name"]
        new_name = fix_name(old_name)
        if old_name != new_name:
            item["name"] = new_name
            fixed += 1
    print(f"  已修正 {fixed} 个菜名")
    return data

# ====================== 步骤3: 审核并修正分类 ======================
def fix_categories(data, name_to_id):
    """审核并修正 cuisine / foodType / mealType / dishType / health / allergens"""
    
    # --- 已知的修正规则 ---
    # 格式: ("菜名", {要替换的类别: 新类别, ...})
    # 每条规则针对特定菜品进行精确修正
    
    CATEGORY_FIXES = {
        # ---- 健康标签修正：不健康食品不应有健康标签 ----
        "辣条": {"remove_health": True},
        "炸鸡": {"remove_health": ["health_low_fat"]},
        "炸鸡排": {"remove_health": ["health_low_fat"]},
        "炸鸡腿": {"remove_health": ["health_low_fat"]},
        "炸薯条": {"remove_health": ["health_low_fat"]},
        "水煮牛肉": {"remove_health": ["health_low_fat"]},  # 水煮牛肉其实很油
        "水煮鱼": {"remove_health": ["health_low_fat"]},
        "水煮肉片": {"remove_health": ["health_low_fat"]},
        
        # ---- 修正错误菜系 ----
        # (很多用 cuisine_other 的应该修正)
        # 这里只做最明显的修正
    }
    
    fixed = 0
    for item in data["items"]:
        name = item["name"]
        cats = item.get("categories", [])
        modified = False
        
        if name in CATEGORY_FIXES:
            fix = CATEGORY_FIXES[name]
            if fix.get("remove_health"):
                # 移除所有 health_ 标签
                new_cats = [c for c in cats if not c.startswith("health_")]
                if len(new_cats) != len(cats):
                    item["categories"] = new_cats
                    cats = new_cats
                    modified = True
            elif "remove_health" in fix:
                to_remove = fix["remove_health"]
                new_cats = [c for c in cats if c not in to_remove]
                if len(new_cats) != len(cats):
                    item["categories"] = new_cats
                    cats = new_cats
                    modified = True
        
        if modified:
            fixed += 1
    
    print(f"  已修正 {fixed} 个条目的分类")
    return data

# ====================== 步骤4: 自动审核健康标签 ======================
# 不应有健康标签的关键词
UNHEALTHY_KEYWORDS = [
    "辣条", "炸", "烧烤", "烤", "油", "肥", "五花", "红油",
    "麻辣", "香辣", "酸辣", "辣子", "火锅", "串串", "冒菜",
    "红烧肉", "东坡肉", "扣肉", "腊肉", "腊肠", "香肠",
    "卤肉", "卤", "酱肘", "猪蹄", "猪脚",
]

def auto_remove_unhealthy_health_tags(data):
    """自动移除不健康食品上的健康标签"""
    fixed = 0
    for item in data["items"]:
        name = item["name"]
        cats = item.get("categories", [])
        is_unhealthy = any(kw in name for kw in UNHEALTHY_KEYWORDS)
        if is_unhealthy:
            new_cats = [c for c in cats if not c.startswith("health_")]
            if len(new_cats) != len(cats):
                item["categories"] = new_cats
                fixed += 1
    print(f"  自动移除 {fixed} 个不健康食品的健康标签")
    return data

# ====================== 步骤5: 添加新菜品 ======================
def build_new_dishes(name_to_id):
    """构建 300+ 道新菜品"""
    
    # 快捷引用
    C = lambda name: name_to_id.get(name, "")
    # 菜系
    cu_chuan = C("川菜")
    cu_lu = C("鲁菜")
    cu_yue = C("粤菜")
    cu_su = C("苏菜")
    cu_zhe = C("浙菜")
    cu_min = C("闽菜")
    cu_xiang = C("湘菜")
    cu_anhui = C("徽菜(皖)")
    cu_yu = C("渝菜")
    cu_beijing = C("京菜")
    cu_shanghai = C("沪菜")
    cu_dongbei = C("东北菜")
    cu_northwest = C("西北菜")
    cu_yunnan = C("云南菜")
    cu_guizhou = C("贵州菜")
    cu_hubei = C("湖北菜")
    cu_shanxi = C("山西菜")
    cu_gansu = C("甘肃菜")
    cu_chongqing = C("重庆菜")
    cu_henan = C("河南菜")
    cu_shaanxi = C("陕西菜")
    cu_xinjiang = C("新疆菜")
    cu_jilin = C("吉林菜")
    cu_guangxi = C("广西菜")
    cu_japanese = C("日式")
    cu_korean = C("韩式")
    cu_thai = C("泰式")
    cu_vietnamese = C("越式")
    cu_indian = C("印度菜")
    cu_italian = C("意式")
    cu_french = C("法式")
    cu_american = C("美式")
    cu_western = C("西餐")
    cu_other = C("其他")
    
    # 餐时
    m_breakfast = C("早餐")
    m_lunch = C("午餐")
    m_dinner = C("晚餐")
    m_midnight = C("夜宵")
    m_afternoon = C("下午茶")
    
    # 食物类型
    f_meat = C("荤菜")
    f_veg = C("素菜")
    f_seafood = C("海鲜")
    f_poultry = C("禽类")
    f_beef = C("牛肉")
    f_pork = C("猪肉")
    f_lamb = C("羊肉")
    f_soup = C("汤羹")
    f_congee = C("粥品")
    f_stew = C("煲仔")
    f_rice = C("饭类")
    f_noodles = C("面食")
    f_dumpling = C("饺子")
    f_bun = C("包子")
    f_pancake = C("饼类")
    f_bbq = C("烧烤")
    f_hotpot = C("火锅")
    f_stirfry = C("炒菜")
    f_cold = C("凉菜")
    f_dessert = C("甜点")
    f_snack = C("小吃")
    f_wholegrain = C("杂粮")
    f_fruit_tea = C("果茶")
    f_tea = C("茶水")
    f_coffee = C("咖啡")
    f_alcohol = C("酒水")
    
    # 菜品类型
    d_staple = C("主食")
    d_main = C("正餐")
    d_snack = C("小吃")
    d_dessert = C("甜点")
    d_beverage = C("饮品")
    d_soup = C("汤品")
    d_appetizer = C("前菜")
    d_salad = C("沙拉")
    
    # 健康标签
    h_low_fat = C("低脂")
    h_low_cal = C("低卡")
    h_high_protein = C("高蛋白")
    h_low_sugar = C("低糖")
    h_sugar_free = C("无糖")
    h_low_salt = C("低盐")
    h_high_fiber = C("高纤维")
    h_vegan = C("素食")
    h_nourishing = C("滋补")
    h_light = C("清淡")
    
    # 过敏原
    a_peanut = C("花生")
    a_tree_nut = C("坚果")
    a_dairy = C("乳制品")
    a_egg = C("鸡蛋")
    a_shellfish = C("海鲜")
    a_fish = C("鱼类")
    a_soy = C("大豆")
    a_gluten = C("麸质")
    a_sesame = C("芝麻")
    a_celery = C("芹菜")
    a_mustard = C("芥末")
    a_sulfite = C("亚硫酸盐")
    a_pork = C("猪肉")
    a_chili = C("辣椒")
    a_onion = C("葱")
    a_ginger = C("姜")
    a_garlic = C("蒜")
    
    NewItem = lambda name, cats: {"name": name, "categories": [c for c in cats if c]}
    
    dishes = []
    
    # ============================================================
    # 1. 早餐类
    # ============================================================
    dishes += [
        NewItem("豆浆", [cu_other, m_breakfast, f_tea, d_beverage, h_low_fat, h_vegan, a_soy]),
        NewItem("油条", [cu_other, m_breakfast, f_snack, d_snack, a_gluten]),
        NewItem("豆腐脑", [cu_other, m_breakfast, f_veg, d_snack, h_vegan, a_soy]),
        NewItem("小笼包", [cu_shanghai, m_breakfast, m_lunch, m_dinner, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("生煎包", [cu_shanghai, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("锅贴", [cu_other, m_breakfast, m_lunch, f_dumpling, d_snack, a_gluten]),
        NewItem("烧麦", [cu_yue, m_breakfast, m_lunch, f_snack, d_snack, a_gluten, a_pork]),
        NewItem("鸡蛋灌饼", [cu_henan, m_breakfast, f_pancake, d_staple, a_gluten, a_egg]),
        NewItem("肉夹馍", [cu_shaanxi, m_breakfast, m_lunch, m_dinner, f_pancake, d_staple, a_gluten, a_pork]),
        NewItem("肠粉", [cu_yue, m_breakfast, m_lunch, f_snack, d_snack, a_gluten, a_egg]),
        NewItem("粢饭团", [cu_shanghai, m_breakfast, f_rice, d_staple, a_gluten]),
        NewItem("糯米饭团", [cu_other, m_breakfast, f_rice, d_staple]),
        NewItem("馒头", [cu_other, m_breakfast, m_lunch, m_dinner, f_bun, d_staple, a_gluten]),
        NewItem("花卷", [cu_other, m_breakfast, m_lunch, f_bun, d_staple, a_gluten, a_onion]),
        NewItem("糖三角", [cu_dongbei, m_breakfast, m_afternoon, f_bun, d_snack, a_gluten]),
        NewItem("豆沙包", [cu_other, m_breakfast, m_afternoon, f_bun, d_snack, a_gluten, a_soy]),
        NewItem("奶黄包", [cu_yue, m_breakfast, m_afternoon, f_bun, d_snack, a_gluten, a_dairy, a_egg]),
        NewItem("叉烧包", [cu_yue, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("灌汤包", [cu_other, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("水晶虾饺", [cu_yue, m_breakfast, m_lunch, f_dumpling, d_snack, a_gluten, a_shellfish]),
        NewItem("豉汁排骨", [cu_yue, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_soy]),
        NewItem("凤爪", [cu_yue, m_lunch, m_dinner, m_midnight, f_snack, d_snack, a_chili, a_garlic]),
        NewItem("糯米鸡", [cu_yue, m_breakfast, m_lunch, f_snack, d_staple, a_gluten]),
        NewItem("马拉糕", [cu_yue, m_breakfast, m_afternoon, f_dessert, d_dessert, a_gluten, a_egg]),
        NewItem("萝卜糕", [cu_yue, m_breakfast, m_lunch, f_snack, d_snack, a_gluten]),
        NewItem("芋头糕", [cu_yue, m_breakfast, m_lunch, f_snack, d_snack, a_gluten]),
        NewItem("春卷", [cu_other, m_breakfast, m_lunch, f_snack, d_snack, a_gluten]),
        NewItem("葱油饼", [cu_shanghai, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten, a_onion]),
        NewItem("酱香饼", [cu_other, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten, a_soy, a_onion]),
        NewItem("手抓饼", [cu_other, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten]),
        NewItem("馅饼", [cu_dongbei, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten]),
        NewItem("烧饼", [cu_other, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten, a_sesame]),
        NewItem("芝麻球", [cu_other, m_breakfast, m_afternoon, f_dessert, d_dessert, a_gluten, a_sesame]),
        NewItem("麻团", [cu_other, m_breakfast, m_afternoon, f_dessert, d_dessert, a_gluten, a_sesame]),
        NewItem("糖糕", [cu_other, m_breakfast, m_afternoon, f_dessert, d_dessert, a_gluten]),
        NewItem("炸糕", [cu_beijing, m_breakfast, m_afternoon, f_dessert, d_dessert, a_gluten]),
        NewItem("馓子", [cu_northwest, m_breakfast, m_afternoon, f_snack, d_snack, a_gluten]),
        NewItem("油饼", [cu_beijing, m_breakfast, f_pancake, d_snack, a_gluten]),
        NewItem("面窝", [cu_hubei, m_breakfast, f_snack, d_snack, a_gluten]),
        NewItem("豆皮(武汉)", [cu_hubei, m_breakfast, m_lunch, f_snack, d_snack, a_gluten, a_soy]),
        NewItem("糊辣汤", [cu_henan, m_breakfast, f_soup, d_soup, a_chili, a_gluten]),
    ]
    
    # ============================================================
    # 2. 小吃/零食
    # ============================================================
    dishes += [
        NewItem("辣条", [cu_other, m_afternoon, m_midnight, f_snack, d_snack, a_gluten, a_chili, a_soy]),
        NewItem("臭豆腐", [cu_xiang, m_midnight, m_afternoon, f_snack, d_snack, a_soy, a_chili]),
        NewItem("烤冷面", [cu_dongbei, m_afternoon, m_midnight, f_snack, d_snack, a_gluten, a_egg]),
        NewItem("铁板鱿鱼", [cu_other, m_afternoon, m_midnight, f_seafood, f_bbq, d_snack, a_shellfish, a_chili]),
        NewItem("盐酥鸡", [cu_other, m_afternoon, m_midnight, f_poultry, f_snack, d_snack, a_gluten, a_chili]),
        NewItem("甘梅地瓜", [cu_other, m_afternoon, f_snack, d_snack]),
        NewItem("烤面筋", [cu_northwest, m_afternoon, m_midnight, f_bbq, d_snack, a_gluten, a_chili]),
        NewItem("凉皮", [cu_shaanxi, m_lunch, m_dinner, f_cold, d_snack, a_gluten, a_chili, a_garlic]),
        NewItem("擀面皮", [cu_shaanxi, m_lunch, m_dinner, f_cold, d_snack, a_gluten, a_chili, a_garlic]),
        NewItem("米线", [cu_yunnan, m_lunch, m_dinner, f_noodles, d_staple, a_chili]),
        NewItem("酸辣粉", [cu_chongqing, m_lunch, m_dinner, m_midnight, f_noodles, d_snack, a_chili, a_gluten, a_soy]),
        NewItem("螺蛳粉", [cu_guangxi, m_lunch, m_dinner, m_midnight, f_noodles, d_snack, a_chili]),
        NewItem("麻辣烫", [cu_chuan, m_lunch, m_dinner, m_midnight, f_hotpot, d_main, a_chili]),
        NewItem("冒菜", [cu_chuan, m_lunch, m_dinner, m_midnight, f_stirfry, d_main, a_chili]),
        NewItem("串串香", [cu_chuan, m_lunch, m_dinner, m_midnight, f_hotpot, d_main, a_chili]),
        NewItem("钵钵鸡", [cu_chuan, m_lunch, m_dinner, m_midnight, f_poultry, f_cold, d_snack, a_chili, a_sesame]),
        NewItem("关东煮", [cu_japanese, m_lunch, m_dinner, m_midnight, f_snack, d_snack, a_soy, a_fish]),
        NewItem("糖葫芦", [cu_beijing, m_afternoon, f_dessert, d_dessert]),
        NewItem("炒栗子", [cu_other, m_afternoon, f_snack, d_snack, a_tree_nut]),
        NewItem("烤红薯", [cu_other, m_afternoon, m_midnight, f_wholegrain, d_snack]),
        NewItem("爆米花", [cu_american, m_afternoon, f_snack, d_snack]),
    ]
    
    # ============================================================
    # 3. 正餐
    # ============================================================
    dishes += [
        # 鸭类
        NewItem("烤鸭", [cu_beijing, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        NewItem("大唐醉仙鸭", [cu_other, m_lunch, m_dinner, f_poultry, d_main, h_high_protein, a_soy]),
        NewItem("大宋醉仙鸭", [cu_other, m_lunch, m_dinner, f_poultry, d_main, h_high_protein, a_soy]),
        NewItem("烧鹅", [cu_yue, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        
        # 鸡类
        NewItem("白切鸡", [cu_yue, m_lunch, m_dinner, f_poultry, d_main, h_low_fat, h_high_protein, h_light]),
        NewItem("豉油鸡", [cu_yue, m_lunch, m_dinner, f_poultry, d_main, h_high_protein, a_soy]),
        NewItem("盐焗鸡", [cu_yue, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        NewItem("手撕鸡", [cu_chuan, m_lunch, m_dinner, f_poultry, d_main, h_high_protein, a_chili, a_sesame]),
        
        # 卤肉类
        NewItem("卤牛肉", [cu_other, m_lunch, m_dinner, f_beef, f_cold, d_main, h_high_protein, a_soy]),
        NewItem("卤猪蹄", [cu_other, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        NewItem("酱牛肉", [cu_beijing, m_lunch, m_dinner, f_beef, f_cold, d_main, h_high_protein, a_soy]),
        NewItem("酱肘子", [cu_beijing, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        
        # 猪肉类
        NewItem("红烧排骨", [cu_other, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_soy]),
        NewItem("糖醋排骨", [cu_zhe, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        NewItem("粉蒸肉", [cu_hubei, m_lunch, m_dinner, f_pork, d_main, a_pork, a_gluten]),
        NewItem("梅菜扣肉", [cu_yue, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        NewItem("东坡肉", [cu_zhe, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        NewItem("红烧狮子头", [cu_su, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        NewItem("糖醋里脊", [cu_lu, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        NewItem("溜肉段", [cu_dongbei, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        
        # 蔬菜类
        NewItem("地三鲜", [cu_dongbei, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan]),
        NewItem("酸辣土豆丝", [cu_chuan, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, a_chili]),
        NewItem("家常豆腐", [cu_chuan, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_high_protein, a_soy]),
        NewItem("干煸四季豆", [cu_chuan, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_high_fiber, a_chili]),
        NewItem("鱼香茄子", [cu_chuan, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, a_chili, a_garlic]),
        NewItem("虎皮青椒", [cu_xiang, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, a_chili]),
        NewItem("蒜蓉西兰花", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_high_fiber, h_light, a_garlic]),
        NewItem("蚝油生菜", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_low_fat, h_light]),
        NewItem("白灼菜心", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_low_fat, h_light]),
        NewItem("手撕包菜", [cu_xiang, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_high_fiber, a_chili]),
        NewItem("干锅花菜", [cu_xiang, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_high_fiber, a_chili]),
        NewItem("干锅土豆片", [cu_chuan, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, a_chili]),
        NewItem("干锅肥肠", [cu_chuan, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        NewItem("毛血旺", [cu_chongqing, m_lunch, m_dinner, f_meat, f_stirfry, d_main, a_chili, a_pork]),
        
        # 鱼类
        NewItem("松鼠鳜鱼", [cu_su, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish]),
        NewItem("西湖醋鱼", [cu_zhe, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish]),
        NewItem("剁椒鱼头", [cu_xiang, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("烤鱼", [cu_chongqing, m_lunch, m_dinner, m_midnight, f_seafood, f_bbq, d_main, h_high_protein, a_fish, a_chili]),
        
        # 虾蟹类
        NewItem("香辣虾", [cu_chuan, m_lunch, m_dinner, f_seafood, f_stirfry, d_main, h_high_protein, a_shellfish, a_chili]),
        NewItem("白灼虾", [cu_yue, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, h_low_fat, h_light, a_shellfish]),
        NewItem("椒盐虾", [cu_yue, m_lunch, m_dinner, f_seafood, f_stirfry, d_main, h_high_protein, a_shellfish]),
        NewItem("避风塘炒蟹", [cu_yue, m_lunch, m_dinner, f_seafood, f_stirfry, d_main, h_high_protein, a_shellfish, a_garlic]),
        NewItem("葱姜炒蟹", [cu_yue, m_lunch, m_dinner, f_seafood, f_stirfry, d_main, h_high_protein, a_shellfish, a_onion, a_ginger]),
        NewItem("小龙虾(麻辣)", [cu_hubei, m_lunch, m_dinner, m_midnight, f_seafood, d_main, h_high_protein, a_shellfish, a_chili]),
        NewItem("小龙虾(蒜蓉)", [cu_hubei, m_lunch, m_dinner, m_midnight, f_seafood, d_main, h_high_protein, a_shellfish, a_garlic]),
        NewItem("小龙虾(十三香)", [cu_hubei, m_lunch, m_dinner, m_midnight, f_seafood, d_main, h_high_protein, a_shellfish, a_chili]),
    ]
    
    # ============================================================
    # 4. 面食
    # ============================================================
    dishes += [
        NewItem("兰州拉面", [cu_gansu, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_chili]),
        NewItem("牛肉面", [cu_northwest, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, h_high_protein, a_gluten]),
        NewItem("炸酱面", [cu_beijing, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_soy, a_pork]),
        NewItem("刀削面", [cu_shanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("烩面", [cu_henan, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("油泼面", [cu_shaanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_chili, a_garlic]),
        NewItem("biangbiang面", [cu_shaanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_chili]),
        NewItem("臊子面", [cu_shaanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_chili, a_pork]),
        NewItem("阳春面", [cu_su, m_breakfast, m_lunch, f_noodles, d_staple, a_gluten]),
        NewItem("葱油拌面", [cu_shanghai, m_breakfast, m_lunch, f_noodles, d_staple, a_gluten, a_onion]),
        NewItem("片儿川", [cu_zhe, m_breakfast, m_lunch, f_noodles, d_staple, a_gluten]),
        NewItem("锅盖面", [cu_su, m_breakfast, m_lunch, f_noodles, d_staple, a_gluten]),
        NewItem("炒面", [cu_other, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("焖面", [cu_shanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("朝鲜冷面", [cu_korean, m_lunch, m_dinner, f_noodles, f_cold, d_staple, a_gluten, a_egg]),
        NewItem("打卤面", [cu_lu, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_egg]),
        NewItem("捞面", [cu_yue, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("凉面", [cu_chuan, m_lunch, m_dinner, f_noodles, f_cold, d_staple, a_gluten, a_chili, a_garlic]),
        NewItem("冷面", [cu_dongbei, m_lunch, m_dinner, f_noodles, f_cold, d_staple, a_gluten]),
    ]
    
    # ============================================================
    # 5. 饭类
    # ============================================================
    dishes += [
        NewItem("煲仔饭", [cu_yue, m_lunch, m_dinner, f_rice, f_stew, d_staple, a_pork]),
        NewItem("黄焖鸡米饭", [cu_lu, m_lunch, m_dinner, f_rice, d_staple, h_high_protein, a_chili]),
        NewItem("卤肉饭", [cu_min, m_lunch, m_dinner, f_rice, d_staple, a_pork, a_soy]),
        NewItem("鸡腿饭", [cu_other, m_lunch, m_dinner, f_rice, d_staple, h_high_protein]),
        NewItem("叉烧饭", [cu_yue, m_lunch, m_dinner, f_rice, d_staple, a_pork]),
        NewItem("烧鸭饭", [cu_yue, m_lunch, m_dinner, f_rice, d_staple, h_high_protein]),
        NewItem("猪脚饭", [cu_yue, m_lunch, m_dinner, f_rice, d_staple, a_pork]),
        NewItem("隆江猪脚饭", [cu_yue, m_lunch, m_dinner, f_rice, d_staple, a_pork]),
        NewItem("扬州炒饭", [cu_su, m_lunch, m_dinner, f_rice, d_staple, a_egg]),
        NewItem("蛋炒饭", [cu_other, m_lunch, m_dinner, f_rice, d_staple, a_egg]),
        NewItem("菠萝炒饭", [cu_thai, m_lunch, m_dinner, f_rice, d_staple, a_shellfish, a_egg]),
        NewItem("咖喱饭", [cu_indian, m_lunch, m_dinner, f_rice, d_staple]),
        NewItem("盖浇饭", [cu_other, m_lunch, m_dinner, f_rice, d_staple]),
        NewItem("木桶饭", [cu_other, m_lunch, m_dinner, f_rice, d_staple]),
        NewItem("荷叶饭", [cu_yue, m_lunch, m_dinner, f_rice, d_staple]),
    ]
    
    # ============================================================
    # 6. 汤类
    # ============================================================
    dishes += [
        NewItem("紫菜蛋花汤", [cu_other, m_lunch, m_dinner, f_soup, d_soup, h_low_fat, h_light, a_egg]),
        NewItem("番茄蛋汤", [cu_other, m_lunch, m_dinner, f_soup, d_soup, h_low_fat, h_light, a_egg]),
        NewItem("酸辣汤", [cu_chuan, m_lunch, m_dinner, f_soup, d_soup, a_chili, a_egg, a_soy]),
        NewItem("胡辣汤", [cu_henan, m_breakfast, f_soup, d_soup, a_chili, a_gluten]),
        NewItem("羊肉汤", [cu_northwest, m_breakfast, m_lunch, m_dinner, f_soup, d_soup, h_nourishing]),
        NewItem("牛肉汤", [cu_henan, m_breakfast, m_lunch, m_dinner, f_soup, d_soup, h_high_protein, h_nourishing]),
        NewItem("老鸭汤", [cu_su, m_lunch, m_dinner, f_soup, d_soup, h_nourishing]),
        NewItem("鸡汤", [cu_other, m_lunch, m_dinner, f_soup, d_soup, h_nourishing, h_high_protein]),
        NewItem("冬瓜排骨汤", [cu_yue, m_lunch, m_dinner, f_soup, d_soup, h_low_fat, h_light, a_pork]),
        NewItem("玉米排骨汤", [cu_yue, m_lunch, m_dinner, f_soup, d_soup, a_pork]),
        NewItem("莲藕排骨汤", [cu_hubei, m_lunch, m_dinner, f_soup, d_soup, h_nourishing, a_pork]),
        NewItem("萝卜牛腩汤", [cu_yue, m_lunch, m_dinner, f_soup, d_soup, h_nourishing, h_high_protein]),
    ]
    
    # ============================================================
    # 7. 凉菜
    # ============================================================
    dishes += [
        NewItem("凉拌黄瓜", [cu_other, m_lunch, m_dinner, f_cold, f_veg, d_appetizer, h_vegan, h_low_fat, h_low_cal, h_light, a_garlic]),
        NewItem("凉拌木耳", [cu_other, m_lunch, m_dinner, f_cold, f_veg, d_appetizer, h_vegan, h_high_fiber, h_light, a_garlic]),
        NewItem("凉拌三丝", [cu_chuan, m_lunch, m_dinner, f_cold, f_veg, d_appetizer, h_vegan, h_light, a_chili]),
        NewItem("皮蛋豆腐", [cu_other, m_lunch, m_dinner, f_cold, f_veg, d_appetizer, h_low_fat, h_light, a_soy, a_egg]),
        NewItem("老醋花生", [cu_lu, m_lunch, m_dinner, f_cold, d_appetizer, a_peanut]),
        NewItem("凉拌牛肉", [cu_chuan, m_lunch, m_dinner, f_cold, f_beef, d_appetizer, h_high_protein, a_chili, a_sesame]),
        NewItem("蒜泥白肉", [cu_chuan, m_lunch, m_dinner, f_cold, f_pork, d_appetizer, a_pork, a_garlic, a_chili]),
        NewItem("拍黄瓜", [cu_dongbei, m_lunch, m_dinner, f_cold, f_veg, d_appetizer, h_vegan, h_low_fat, h_light, a_garlic]),
    ]
    
    # ============================================================
    # 8. 火锅/烧烤
    # ============================================================
    dishes += [
        NewItem("羊肉串", [cu_xinjiang, m_lunch, m_dinner, m_midnight, f_bbq, d_snack, a_chili]),
        NewItem("牛肉串", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, d_snack, h_high_protein, a_chili]),
        NewItem("烤鸡翅", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, d_snack, h_high_protein]),
        NewItem("烤茄子", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, f_veg, d_snack, h_vegan, a_garlic]),
        NewItem("烤韭菜", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, f_veg, d_snack, h_vegan, a_chili]),
        NewItem("烤馒头", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, d_snack, a_gluten]),
        NewItem("烤玉米", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, f_wholegrain, d_snack, h_vegan]),
        NewItem("烤土豆", [cu_other, m_lunch, m_dinner, m_midnight, f_bbq, f_veg, d_snack, h_vegan]),
    ]
    
    # ============================================================
    # 9. 地方特色
    # ============================================================
    dishes += [
        NewItem("桂林米粉", [cu_guangxi, m_breakfast, m_lunch, m_dinner, f_noodles, d_snack, a_chili, a_peanut]),
        NewItem("湖南米粉", [cu_xiang, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, a_chili]),
        NewItem("南昌拌粉", [cu_other, m_breakfast, m_lunch, f_noodles, d_snack, a_chili, a_soy]),
        NewItem("新疆大盘鸡", [cu_xinjiang, m_lunch, m_dinner, f_poultry, f_stirfry, d_main, h_high_protein, a_chili]),
        NewItem("新疆手抓饭", [cu_xinjiang, m_lunch, m_dinner, f_rice, d_staple]),
        NewItem("天津狗不理包子", [cu_other, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("上海生煎", [cu_shanghai, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("南京盐水鸭", [cu_su, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        NewItem("武汉热干面", [cu_hubei, m_breakfast, f_noodles, d_staple, a_gluten, a_sesame, a_soy]),
        NewItem("长沙臭豆腐", [cu_xiang, m_afternoon, m_midnight, f_snack, d_snack, a_soy, a_chili]),
        NewItem("成都串串", [cu_chuan, m_lunch, m_dinner, m_midnight, f_hotpot, d_main, a_chili]),
        NewItem("重庆小面", [cu_chongqing, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, a_chili, a_gluten]),
        NewItem("广州肠粉", [cu_yue, m_breakfast, m_lunch, f_snack, d_snack, a_gluten, a_egg]),
        NewItem("潮汕牛肉丸", [cu_yue, m_lunch, m_dinner, f_beef, d_snack, h_high_protein]),
        NewItem("福建佛跳墙", [cu_min, m_lunch, m_dinner, f_seafood, f_stew, d_main, h_nourishing, h_high_protein, a_shellfish, a_pork]),
        NewItem("海南文昌鸡", [cu_other, m_lunch, m_dinner, f_poultry, d_main, h_high_protein, h_light]),
        NewItem("东北乱炖", [cu_dongbei, m_lunch, m_dinner, f_meat, f_stew, d_main]),
        NewItem("北京炸酱面", [cu_beijing, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_soy, a_pork]),
        NewItem("山东煎饼", [cu_lu, m_breakfast, m_lunch, f_pancake, d_staple, a_gluten]),
        NewItem("山西刀削面", [cu_shanxi, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("柳州螺蛳粉", [cu_guangxi, m_lunch, m_dinner, m_midnight, f_noodles, d_snack, a_chili]),
    ]
    
    # ============================================================
    # 10. 新式/融合
    # ============================================================
    dishes += [
        NewItem("麻辣香锅", [cu_chongqing, m_lunch, m_dinner, m_midnight, f_stirfry, d_main, a_chili]),
        NewItem("纸包鱼", [cu_chongqing, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("跳跳蛙", [cu_xiang, m_lunch, m_dinner, m_midnight, f_meat, f_stirfry, d_main, h_high_protein, a_chili]),
        NewItem("肉蟹煲", [cu_zhe, m_lunch, m_dinner, f_seafood, f_stew, d_main, h_high_protein, a_shellfish, a_chili]),
    ]
    
    # ============================================================
    # 11. 更多补充菜品
    # ============================================================
    dishes += [
        # 更多早餐
        NewItem("韭菜盒子", [cu_dongbei, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten, a_chili]),
        NewItem("鸡蛋饼", [cu_other, m_breakfast, f_pancake, d_snack, a_gluten, a_egg]),
        NewItem("肉松饼", [cu_other, m_breakfast, m_afternoon, f_pancake, d_snack, a_gluten, a_pork]),
        NewItem("老婆饼", [cu_yue, m_afternoon, f_dessert, d_dessert, a_gluten]),
        NewItem("蛋黄酥", [cu_other, m_afternoon, f_dessert, d_dessert, a_gluten, a_egg, a_soy]),
        NewItem("桃酥", [cu_other, m_afternoon, f_dessert, d_dessert, a_gluten, a_egg]),
        NewItem("绿豆糕", [cu_other, m_afternoon, f_dessert, d_dessert, a_soy]),
        NewItem("桂花糕", [cu_su, m_afternoon, f_dessert, d_dessert, a_gluten]),
        NewItem("千层饼", [cu_other, m_breakfast, m_lunch, f_pancake, d_snack, a_gluten]),
        
        # 更多小吃
        NewItem("炸鸡排", [cu_other, m_afternoon, m_midnight, f_poultry, f_snack, d_snack, a_gluten]),
        NewItem("炸薯条", [cu_american, m_afternoon, f_snack, d_snack]),
        NewItem("章鱼小丸子", [cu_japanese, m_afternoon, m_midnight, f_snack, d_snack, a_gluten, a_shellfish]),
        NewItem("鸡蛋仔", [cu_yue, m_afternoon, f_dessert, d_dessert, a_gluten, a_egg, a_dairy]),
        NewItem("双皮奶", [cu_yue, m_afternoon, f_dessert, d_dessert, a_dairy, a_egg]),
        NewItem("杨枝甘露", [cu_yue, m_afternoon, f_dessert, d_dessert, a_dairy]),
        NewItem("龟苓膏", [cu_yue, m_afternoon, f_dessert, d_dessert]),
        NewItem("烧仙草", [cu_min, m_afternoon, f_dessert, d_dessert]),
        NewItem("芋圆", [cu_min, m_afternoon, f_dessert, d_dessert]),
        NewItem("冰粉", [cu_chuan, m_afternoon, f_dessert, d_dessert]),
        
        # 更多正餐
        NewItem("京酱肉丝", [cu_beijing, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_soy, a_onion]),
        NewItem("木须肉", [cu_lu, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_egg]),
        NewItem("葱爆羊肉", [cu_lu, m_lunch, m_dinner, f_lamb, f_stirfry, d_main, h_high_protein, a_onion]),
        NewItem("孜然羊肉", [cu_xinjiang, m_lunch, m_dinner, f_lamb, f_stirfry, d_main, h_high_protein, a_chili]),
        NewItem("宫保虾仁", [cu_chuan, m_lunch, m_dinner, f_seafood, f_stirfry, d_main, h_high_protein, a_shellfish, a_peanut, a_chili]),
        NewItem("酸豆角炒肉", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        NewItem("萝卜干炒腊肉", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        NewItem("小炒肉", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        NewItem("农家一碗香", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili, a_egg]),
        NewItem("茄子煲", [cu_yue, m_lunch, m_dinner, f_veg, f_stew, d_main, h_vegan, a_garlic]),
        NewItem("煲仔饭(腊味)", [cu_yue, m_lunch, m_dinner, f_rice, f_stew, d_staple, a_pork]),
        NewItem("可乐鸡翅", [cu_other, m_lunch, m_dinner, f_poultry, f_stirfry, d_main, h_high_protein]),
        NewItem("蒜香排骨", [cu_yue, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_garlic]),
        
        # 更多汤
        NewItem("排骨汤", [cu_other, m_lunch, m_dinner, f_soup, d_soup, h_nourishing, a_pork]),
        NewItem("乌鸡汤", [cu_yue, m_lunch, m_dinner, f_soup, d_soup, h_nourishing, h_high_protein]),
        NewItem("银耳莲子汤", [cu_yue, m_afternoon, f_soup, d_soup, h_nourishing]),
        NewItem("南瓜汤", [cu_western, m_lunch, m_dinner, f_soup, d_soup, h_vegan, h_low_fat, h_high_fiber]),
        NewItem("罗宋汤", [cu_western, m_lunch, m_dinner, f_soup, d_soup]),
        NewItem("酸辣汤(粤式)", [cu_yue, m_lunch, m_dinner, f_soup, d_soup, a_chili, a_egg]),
        
        # 饮品
        NewItem("珍珠奶茶", [cu_other, m_afternoon, f_fruit_tea, d_beverage, a_dairy]),
        NewItem("柠檬茶", [cu_yue, m_afternoon, m_lunch, f_fruit_tea, d_beverage]),
        NewItem("酸梅汤", [cu_beijing, m_afternoon, m_lunch, m_dinner, f_fruit_tea, d_beverage]),
        NewItem("绿豆汤", [cu_other, m_afternoon, f_soup, d_beverage, h_vegan, h_low_fat]),
        NewItem("苏式绿豆汤", [cu_su, m_afternoon, f_soup, d_beverage]),
        NewItem("红豆沙", [cu_yue, m_afternoon, f_dessert, d_dessert, h_vegan]),
        NewItem("椰汁西米露", [cu_yue, m_afternoon, f_dessert, d_dessert, a_dairy]),
        NewItem("冰糖雪梨", [cu_other, m_afternoon, f_soup, d_beverage, h_nourishing]),
        
        # 国际料理
        NewItem("寿司", [cu_japanese, m_lunch, m_dinner, f_seafood, d_main, a_fish, a_soy]),
        NewItem("天妇罗", [cu_japanese, m_lunch, m_dinner, f_veg, d_snack, a_gluten, a_shellfish]),
        NewItem("拉面(日式)", [cu_japanese, m_lunch, m_dinner, f_noodles, d_staple, a_gluten, a_pork]),
        NewItem("石锅拌饭", [cu_korean, m_lunch, m_dinner, f_rice, d_staple, a_egg, a_chili]),
        NewItem("韩式炸鸡", [cu_korean, m_lunch, m_dinner, m_midnight, f_poultry, d_snack, a_gluten, a_chili]),
        NewItem("泡菜", [cu_korean, m_lunch, m_dinner, f_veg, f_cold, d_appetizer, a_chili, a_garlic]),
        NewItem("韩式烤肉", [cu_korean, m_lunch, m_dinner, f_bbq, d_main, h_high_protein]),
        NewItem("冬阴功汤", [cu_thai, m_lunch, m_dinner, f_soup, d_soup, a_shellfish, a_chili]),
        NewItem("泰式咖喱蟹", [cu_thai, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_shellfish, a_chili]),
        NewItem("越南河粉", [cu_vietnamese, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, a_chili]),
        NewItem("印度飞饼", [cu_indian, m_lunch, m_dinner, f_pancake, d_snack, a_gluten]),
        NewItem("意大利面", [cu_italian, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("披萨", [cu_italian, m_lunch, m_dinner, f_pancake, d_staple, a_gluten, a_dairy]),
        NewItem("牛排", [cu_western, m_lunch, m_dinner, f_beef, d_main, h_high_protein]),
        NewItem("法式鹅肝", [cu_french, m_lunch, m_dinner, f_poultry, d_main]),
        NewItem("汉堡", [cu_american, m_lunch, m_dinner, f_meat, d_snack, a_gluten]),
        NewItem("热狗", [cu_american, m_lunch, m_dinner, f_meat, d_snack, a_gluten]),
        NewItem("三明治", [cu_american, m_breakfast, m_lunch, f_meat, d_snack, a_gluten, a_dairy]),
        NewItem("凯撒沙拉", [cu_western, m_lunch, m_dinner, f_veg, d_salad, h_low_fat, h_light, h_high_fiber, a_dairy]),
        
        # 更多地方特色
        NewItem("锅包肉", [cu_dongbei, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        NewItem("猪肉炖粉条", [cu_dongbei, m_lunch, m_dinner, f_pork, f_stew, d_main, a_pork, a_gluten]),
        NewItem("小鸡炖蘑菇", [cu_dongbei, m_lunch, m_dinner, f_poultry, f_stew, d_main, h_high_protein, h_nourishing]),
        NewItem("酱大骨", [cu_dongbei, m_lunch, m_dinner, f_pork, d_main, a_pork, a_soy]),
        NewItem("酸菜白肉", [cu_dongbei, m_lunch, m_dinner, f_pork, f_stew, d_main, a_pork]),
        NewItem("东北大拉皮", [cu_dongbei, m_lunch, m_dinner, f_cold, d_appetizer, a_chili, a_garlic, a_gluten]),
        
        # 湖北菜系补充
        NewItem("沔阳三蒸", [cu_hubei, m_lunch, m_dinner, f_pork, d_main, a_pork, a_gluten]),
        NewItem("豆皮", [cu_hubei, m_breakfast, m_lunch, f_snack, d_snack, a_gluten, a_soy, a_egg]),
        
        # 云南菜
        NewItem("过桥米线", [cu_yunnan, m_breakfast, m_lunch, m_dinner, f_noodles, d_staple, h_high_protein]),
        NewItem("汽锅鸡", [cu_yunnan, m_lunch, m_dinner, f_poultry, f_stew, d_main, h_nourishing, h_high_protein]),
        
        # 贵州菜
        NewItem("酸汤鱼", [cu_guizhou, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("花江狗肉(已禁)", [cu_guizhou, m_lunch, m_dinner, f_meat, d_main]),
        NewItem("贵阳素粉", [cu_guizhou, m_breakfast, m_lunch, f_noodles, d_snack, a_chili, a_soy]),
        
        # 广西菜
        NewItem("老友粉", [cu_guangxi, m_breakfast, m_lunch, m_dinner, f_noodles, d_snack, a_chili, a_soy]),
        
        # 海南
        NewItem("海南鸡饭", [cu_other, m_lunch, m_dinner, f_rice, d_staple, h_high_protein, h_light]),
        NewItem("椰子鸡", [cu_other, m_lunch, m_dinner, f_poultry, f_soup, d_main, h_nourishing, h_high_protein]),
        
        # 安徽菜
        NewItem("臭鳜鱼", [cu_anhui, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish]),
        NewItem("毛豆腐", [cu_anhui, m_lunch, m_dinner, f_veg, d_snack, a_soy]),
        
        # 西北菜补充
        NewItem("羊肉泡馍", [cu_shaanxi, m_breakfast, m_lunch, m_dinner, f_lamb, d_staple, a_gluten]),
        NewItem("凉粉", [cu_northwest, m_lunch, m_dinner, f_cold, d_snack, a_chili, a_garlic]),
        NewItem("烤全羊", [cu_xinjiang, m_lunch, m_dinner, f_lamb, f_bbq, d_main, h_high_protein]),
        NewItem("大盘鸡拌面", [cu_xinjiang, m_lunch, m_dinner, f_poultry, f_noodles, d_staple, h_high_protein, a_chili, a_gluten]),
        
        # 甜品补充
        NewItem("提拉米苏", [cu_italian, m_afternoon, f_dessert, d_dessert, a_dairy, a_egg, a_gluten]),
        NewItem("芝士蛋糕", [cu_american, m_afternoon, f_dessert, d_dessert, a_dairy, a_egg, a_gluten]),
        NewItem("巧克力蛋糕", [cu_western, m_afternoon, f_dessert, d_dessert, a_dairy, a_egg, a_gluten]),
        NewItem("布丁", [cu_western, m_afternoon, f_dessert, d_dessert, a_dairy, a_egg]),
        NewItem("冰淇淋", [cu_western, m_afternoon, f_dessert, d_dessert, a_dairy]),
        
        # 更多川菜
        NewItem("夫妻肺片", [cu_chuan, m_lunch, m_dinner, f_cold, f_beef, d_appetizer, h_high_protein, a_chili, a_sesame]),
        NewItem("口水鸡", [cu_chuan, m_lunch, m_dinner, f_poultry, f_cold, d_appetizer, h_high_protein, a_chili, a_sesame, a_peanut]),
        NewItem("辣子鸡", [cu_chuan, m_lunch, m_dinner, f_poultry, f_stirfry, d_main, h_high_protein, a_chili]),
        NewItem("水煮鱼片", [cu_chuan, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("酸菜鱼", [cu_chuan, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("毛血旺(川)", [cu_chuan, m_lunch, m_dinner, f_meat, d_main, a_chili, a_pork]),
        
        # 粤菜补充
        NewItem("清蒸鲈鱼", [cu_yue, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, h_low_fat, h_light, a_fish, a_ginger, a_onion]),
        NewItem("红烧乳鸽", [cu_yue, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        NewItem("蒜蓉粉丝蒸扇贝", [cu_yue, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_shellfish, a_garlic, a_gluten]),
        NewItem("炒河粉", [cu_yue, m_lunch, m_dinner, f_noodles, d_staple, a_gluten]),
        NewItem("干炒牛河", [cu_yue, m_lunch, m_dinner, f_noodles, d_staple, h_high_protein, a_gluten]),
        
        # 苏菜/浙菜
        NewItem("龙井虾仁", [cu_zhe, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, h_light, h_low_fat, a_shellfish]),
        NewItem("叫花鸡", [cu_zhe, m_lunch, m_dinner, f_poultry, d_main, h_high_protein]),
        NewItem("无锡排骨", [cu_su, m_lunch, m_dinner, f_pork, d_main, a_pork]),
        NewItem("松鼠鱼", [cu_su, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish]),
        
        # 鲁菜补充
        NewItem("葱烧海参", [cu_lu, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_shellfish, a_onion]),
        NewItem("九转大肠", [cu_lu, m_lunch, m_dinner, f_pork, d_main, a_pork]),
        NewItem("油爆双脆", [cu_lu, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        
        # 闽菜
        NewItem("荔枝肉", [cu_min, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork]),
        NewItem("海蛎煎", [cu_min, m_lunch, m_dinner, f_seafood, d_snack, a_shellfish, a_egg, a_gluten]),
        
        # 湘菜补充
        NewItem("剁椒鱼头(湘)", [cu_xiang, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, a_fish, a_chili]),
        NewItem("辣椒炒肉", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        NewItem("外婆菜炒肉", [cu_xiang, m_lunch, m_dinner, f_pork, f_stirfry, d_main, a_pork, a_chili]),
        
        # 素菜补充
        NewItem("炒空心菜", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_low_fat, h_light, h_high_fiber]),
        NewItem("炒苋菜", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_low_fat, h_light]),
        NewItem("炒豆苗", [cu_yue, m_lunch, m_dinner, f_veg, f_stirfry, d_main, h_vegan, h_low_fat, h_light]),
        
        # 海鲜补充
        NewItem("清蒸大闸蟹", [cu_su, m_lunch, m_dinner, f_seafood, d_main, h_high_protein, h_light, a_shellfish]),
        NewItem("三文鱼刺身", [cu_japanese, m_lunch, m_dinner, f_seafood, d_appetizer, h_high_protein, a_fish]),
        NewItem("金枪鱼刺身", [cu_japanese, m_lunch, m_dinner, f_seafood, d_appetizer, h_high_protein, a_fish]),
        
        # 更多主食
        NewItem("肉包子", [cu_other, m_breakfast, m_lunch, f_bun, d_snack, a_gluten, a_pork]),
        NewItem("素包子", [cu_other, m_breakfast, m_lunch, f_bun, d_snack, h_vegan, a_gluten]),
        NewItem("煎饺", [cu_other, m_breakfast, m_lunch, m_dinner, f_dumpling, d_snack, a_gluten]),
        NewItem("水饺", [cu_dongbei, m_lunch, m_dinner, f_dumpling, d_staple, a_gluten]),
        NewItem("馄饨", [cu_shanghai, m_breakfast, m_lunch, m_dinner, f_dumpling, d_snack, a_gluten]),
        NewItem("抄手(红油)", [cu_chuan, m_breakfast, m_lunch, m_dinner, f_dumpling, d_snack, a_gluten, a_chili, a_pork]),
    ]
    
    return dishes

# ====================== 主流程 ======================
def main():
    print("=" * 60)
    print("开始处理 dishes 数据")
    print("=" * 60)
    
    # 加载
    print("\n[1] 加载 JSON 文件...")
    data = load_data()
    print(f"  已加载 {len(data['items'])} 条记录")
    
    # 构建 ID 映射
    id_to_name, name_to_id = build_category_maps(data["categories"])
    
    # 备份原始(items)
    original_count = len(data["items"])
    
    # 步骤1: 修复缺失的 ID
    print("\n[2] 修复缺失的 ID...")
    data = fix_missing_ids(data)
    
    # 步骤2: 修正菜名
    print("\n[3] 修正菜名...")
    data = apply_name_fixes(data)
    
    # 步骤3: 修正分类
    print("\n[4] 修正分类...")
    data = fix_categories(data, name_to_id)
    
    # 步骤4: 自动移除不健康食品的健康标签
    print("\n[5] 自动移除不健康食品的健康标签...")
    data = auto_remove_unhealthy_health_tags(data)
    
    # 步骤5: 获取现有菜名集合和最大 ID
    existing_names = set()
    max_id = 0
    for item in data["items"]:
        existing_names.add(item["name"])
        if "id" in item:
            m = re.search(r"item_(\d+)", item["id"])
            if m:
                max_id = max(max_id, int(m.group(1)))
    print(f"\n  现有菜品 {len(existing_names)} 道")
    print(f"  当前最大 ID: {max_id}")
    
    # 步骤6: 构建新菜品
    print("\n[6] 构建新菜品...")
    new_dishes = build_new_dishes(name_to_id)
    print(f"  生成 {len(new_dishes)} 道候选新菜品")
    
    # 步骤7: 去重并添加
    print("\n[7] 去重并添加新菜品...")
    added = 0
    skipped = 0
    for dish in new_dishes:
        name = dish["name"]
        if name in existing_names:
            skipped += 1
            continue
        # 检查是否已存在（某些名字可能非常相似）
        # 简单去重
        max_id += 1
        item = {
            "id": f"item_{max_id:05d}",
            "name": name,
            "categories": dish["categories"],
            "attributes": {"health": [], "allergens": []}
        }
        data["items"].append(item)
        existing_names.add(name)
        added += 1
    
    print(f"  新增 {added} 道菜品，跳过 {skipped} 道（已存在）")
    
    # 步骤8: 保存
    print("\n[8] 保存文件...")
    save_data(data)
    
    # 汇总
    print("\n" + "=" * 60)
    print("处理完成!")
    print(f"  原始菜品数: {original_count}")
    print(f"  最终菜品数: {len(data['items'])}")
    print(f"  新增菜品数: {added}")
    print("=" * 60)

if __name__ == "__main__":
    main()