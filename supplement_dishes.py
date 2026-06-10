#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充菜品数据脚本
确保每个菜系至少有5个菜品，并添加国内主流家常菜
"""

import json

def load_data():
    with open('js/ingredients.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_next_id(data):
    """获取下一个可用的item ID"""
    max_id = 0
    for item in data['items']:
        num = int(item['id'].split('_')[1])
        if num > max_id:
            max_id = num
    return max_id + 1

def add_dishes(data, dishes):
    """添加菜品到数据中"""
    start_id = get_next_id(data)
    for i, (name, cuisine_id, meals, foods, dish_types) in enumerate(dishes):
        item = {
            "id": f"item_{start_id + i:05d}",
            "name": name,
            "categories": [cuisine_id] + meals + foods + dish_types
        }
        data['items'].append(item)
    return start_id + len(dishes)

def generate_supplement_dishes():
    """生成需要补充的菜品"""
    
    dishes = []
    
    # ==================== 补充空菜系的菜品 ====================
    
    # 巴西菜 (cuisine_brazilian) -  EMPTY
    dishes.extend([
        ("巴西烤肉", "cuisine_brazilian", ["meal_lunch", "meal_dinner"], ["food_beef", "food_bbq"], ["dish_main"]),
        ("费乔达", "cuisine_brazilian", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("巴西芝士面包球", "cuisine_brazilian", ["meal_breakfast", "meal_afternoon_tea"], ["food_snack"], ["dish_snack"]),
        ("阿萨伊碗", "cuisine_brazilian", ["meal_breakfast", "meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("莫凯卡鱼汤", "cuisine_brazilian", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_soup"], ["dish_main", "dish_soup"]),
    ])
    
    # 希腊菜 (cuisine_greek) - EMPTY
    dishes.extend([
        ("希腊沙拉", "cuisine_greek", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("穆萨卡", "cuisine_greek", ["meal_lunch", "meal_dinner"], ["food_lamb", "food_vegetarian"], ["dish_main"]),
        ("希腊烤肉串", "cuisine_greek", ["meal_lunch", "meal_dinner"], ["food_meat", "food_bbq"], ["dish_main"]),
        ("皮塔饼配鹰嘴豆泥", "cuisine_greek", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("巴克拉瓦", "cuisine_greek", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # 英式 (cuisine_british) - EMPTY
    dishes.extend([
        ("炸鱼薯条", "cuisine_british", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_snack"], ["dish_main"]),
        ("英式早餐", "cuisine_british", ["meal_breakfast"], ["food_meat", "food_poultry"], ["dish_staple"]),
        ("牧羊人派", "cuisine_british", ["meal_lunch", "meal_dinner"], ["food_lamb"], ["dish_main"]),
        ("约克郡布丁", "cuisine_british", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
        ("司康饼", "cuisine_british", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # 非洲菜 (cuisine_african) - EMPTY
    dishes.extend([
        ("塔吉锅", "cuisine_african", ["meal_lunch", "meal_dinner"], ["food_meat", "food_stew"], ["dish_main"]),
        ("富富", "cuisine_african", ["meal_lunch", "meal_dinner"], ["food_wholegrain"], ["dish_staple"]),
        ("贾洛夫饭", "cuisine_african", ["meal_lunch", "meal_dinner"], ["food_rice", "food_poultry"], ["dish_staple"]),
        ("花生炖菜", "cuisine_african", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stew"], ["dish_main"]),
        ("萨摩萨", "cuisine_african", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_snack"]),
    ])
    
    # 马来西亚菜 (cuisine_malaysian) - 已有但可能较少，补充
    dishes.extend([
        ("椰浆饭配参巴酱", "cuisine_malaysian", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("亚参叻沙", "cuisine_malaysian", ["meal_breakfast", "meal_lunch"], ["food_noodles", "food_seafood"], ["dish_staple"]),
        ("仁当牛肉", "cuisine_malaysian", ["meal_lunch", "meal_dinner"], ["food_beef"], ["dish_main"]),
        ("马来炒面", "cuisine_malaysian", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("煎蕊", "cuisine_malaysian", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # ==================== 补充国内主流家常菜 ====================
    
    # 川菜补充 - 辣椒炒鸡蛋等
    dishes.extend([
        ("辣椒炒鸡蛋", "cuisine_chuan", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_poultry", "food_stirfry"], ["dish_main"]),
        ("家常豆腐", "cuisine_chuan", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("鱼香茄子", "cuisine_chuan", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("干煸土豆丝", "cuisine_chuan", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("虎皮青椒", "cuisine_chuan", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
    ])
    
    # 鲁菜补充 - 红烧肉等
    dishes.extend([
        ("红烧肉", "cuisine_lu", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("红烧排骨", "cuisine_lu", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("红烧茄子", "cuisine_lu", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stew"], ["dish_main"]),
        ("糖醋里脊", "cuisine_lu", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("木须肉", "cuisine_lu", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
    ])
    
    # 粤菜补充
    dishes.extend([
        ("白灼菜心", "cuisine_yue", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("清蒸鲈鱼", "cuisine_yue", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("豉油皇大虾", "cuisine_yue", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("滑蛋虾仁", "cuisine_yue", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_poultry"], ["dish_main"]),
        ("豉汁蒸凤爪", "cuisine_yue", ["meal_breakfast", "meal_lunch"], ["food_poultry"], ["dish_snack"]),
    ])
    
    # 苏菜补充
    dishes.extend([
        ("松鼠鳜鱼", "cuisine_su", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("清炖蟹粉狮子头", "cuisine_su", ["meal_lunch", "meal_dinner"], ["food_pork", "food_seafood"], ["dish_main"]),
        ("无锡酱排骨", "cuisine_su", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("苏州熏鱼", "cuisine_su", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("桂花糖藕", "cuisine_su", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # 浙菜补充
    dishes.extend([
        ("龙井虾仁", "cuisine_zhe", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("东坡肘子", "cuisine_zhe", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("西湖莼菜汤", "cuisine_zhe", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("宁波烤菜", "cuisine_zhe", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("绍兴醉鸡", "cuisine_zhe", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
    ])
    
    # 闽菜补充
    dishes.extend([
        ("荔枝肉", "cuisine_min", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("淡糟香螺片", "cuisine_min", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("鸡汤汆海蚌", "cuisine_min", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_poultry"], ["dish_main"]),
        ("莆田卤面", "cuisine_min", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("福州鱼丸", "cuisine_min", ["meal_breakfast", "meal_lunch"], ["food_seafood"], ["dish_snack"]),
    ])
    
    # 湘菜补充
    dishes.extend([
        ("小炒黄牛肉", "cuisine_xiang", ["meal_lunch", "meal_dinner"], ["food_beef", "food_stirfry"], ["dish_main"]),
        ("农家小炒肉", "cuisine_xiang", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("酸辣鸡杂", "cuisine_xiang", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("擂辣椒皮蛋", "cuisine_xiang", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_appetizer"]),
        ("腊味合蒸", "cuisine_xiang", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
    ])
    
    # 徽菜补充
    dishes.extend([
        ("徽州臭鳜鱼", "cuisine_anhui", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("徽州刀板香", "cuisine_anhui", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("绩溪一品锅", "cuisine_anhui", ["meal_lunch", "meal_dinner"], ["food_meat", "food_vegetarian", "food_stew"], ["dish_main"]),
        ("黄山烧饼", "cuisine_anhui", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("徽州毛豆腐", "cuisine_anhui", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
    ])
    
    # 渝菜补充
    dishes.extend([
        ("来凤鱼", "cuisine_yu", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("璧山兔", "cuisine_yu", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("太安鱼", "cuisine_yu", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("邮亭鲫鱼", "cuisine_yu", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("辣子肥肠", "cuisine_yu", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
    ])
    
    # 京菜补充
    dishes.extend([
        ("京酱肉丝", "cuisine_beijing", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("老北京爆肚", "cuisine_beijing", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_main"]),
        ("老北京卤煮", "cuisine_beijing", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_pork"], ["dish_main"]),
        ("老北京炒肝", "cuisine_beijing", ["meal_breakfast"], ["food_pork"], ["dish_staple"]),
        ("艾窝窝", "cuisine_beijing", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # 沪菜补充
    dishes.extend([
        ("上海红烧肉", "cuisine_shanghai", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("上海熏鱼", "cuisine_shanghai", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("草头圈子", "cuisine_shanghai", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("八宝辣酱", "cuisine_shanghai", ["meal_lunch", "meal_dinner"], ["food_meat", "food_vegetarian"], ["dish_main"]),
        ("酒酿圆子", "cuisine_shanghai", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # 东北菜补充
    dishes.extend([
        ("酸菜白肉", "cuisine_dongbei", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("拔丝地瓜", "cuisine_dongbei", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_dessert"]),
        ("雪衣豆沙", "cuisine_dongbei", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("芹菜炒粉条", "cuisine_dongbei", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("尖椒干豆腐", "cuisine_dongbei", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
    ])
    
    # 西北菜补充
    dishes.extend([
        ("臊子面", "cuisine_northwest", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("油泼面", "cuisine_northwest", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("葫芦头泡馍", "cuisine_northwest", ["meal_breakfast", "meal_lunch"], ["food_pancake", "food_meat"], ["dish_staple"]),
        ("擀面皮", "cuisine_northwest", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("甑糕", "cuisine_northwest", ["meal_breakfast"], ["food_wholegrain"], ["dish_staple"]),
    ])
    
    # 云南菜补充
    dishes.extend([
        ("宜良烤鸭", "cuisine_yunnan", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("大理砂锅鱼", "cuisine_yunnan", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_stew"], ["dish_main"]),
        ("曲靖蒸饵丝", "cuisine_yunnan", ["meal_breakfast"], ["food_noodles"], ["dish_staple"]),
        ("玫瑰红糖凉糕", "cuisine_yunnan", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("建水烧豆腐", "cuisine_yunnan", ["meal_lunch", "meal_dinner", "meal_midnight"], ["food_vegetarian"], ["dish_snack"]),
    ])
    
    # 贵州菜补充
    dishes.extend([
        ("花溪王记牛肉粉", "cuisine_guizhou", ["meal_breakfast"], ["food_noodles", "food_beef"], ["dish_staple"]),
        ("青岩猪脚", "cuisine_guizhou", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("贞丰糯米饭", "cuisine_guizhou", ["meal_breakfast"], ["food_rice"], ["dish_staple"]),
        ("安顺裹卷", "cuisine_guizhou", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("镇远陈年道菜", "cuisine_guizhou", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
    ])
    
    # ==================== 日式料理补充 ====================
    dishes.extend([
        ("三文鱼刺身", "cuisine_japanese", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("鳗鱼饭", "cuisine_japanese", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_rice"], ["dish_staple"]),
        ("天妇罗丼", "cuisine_japanese", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_rice"], ["dish_staple"]),
        ("味噌拉面", "cuisine_japanese", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("铜锣烧", "cuisine_japanese", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # ==================== 韩式料理补充 ====================
    dishes.extend([
        ("泡菜炒饭", "cuisine_korean", ["meal_breakfast", "meal_lunch"], ["food_rice"], ["dish_staple"]),
        ("韩式拌饭", "cuisine_korean", ["meal_lunch", "meal_dinner"], ["food_rice"], ["dish_staple"]),
        ("韩式煎饼", "cuisine_korean", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("韩式豆腐煲", "cuisine_korean", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stew"], ["dish_main"]),
        ("韩式甜米露", "cuisine_korean", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 泰式料理补充 ====================
    dishes.extend([
        ("泰式打抛猪肉饭", "cuisine_thai", ["meal_lunch", "meal_dinner"], ["food_pork", "food_rice"], ["dish_staple"]),
        ("泰式船面", "cuisine_thai", ["meal_lunch", "meal_dinner"], ["food_noodles"], ["dish_staple"]),
        ("泰式木瓜沙拉", "cuisine_thai", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("泰式椰子冰淇淋", "cuisine_thai", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("泰式柠檬茶", "cuisine_thai", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 越式料理补充 ====================
    dishes.extend([
        ("越南米粉", "cuisine_vietnamese", ["meal_breakfast", "meal_lunch"], ["food_noodles"], ["dish_staple"]),
        ("越南三明治", "cuisine_vietnamese", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("越南春卷", "cuisine_vietnamese", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_appetizer"]),
        ("越南滴漏咖啡", "cuisine_vietnamese", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("越南甘蔗虾", "cuisine_vietnamese", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_snack"]),
    ])
    
    # ==================== 印度菜补充 ====================
    dishes.extend([
        ("印度咖喱角", "cuisine_indian", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("印度烤饼", "cuisine_indian", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("印度酸奶", "cuisine_indian", ["meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
        ("印度蔬菜咖喱", "cuisine_indian", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_main"]),
        ("印度酥油鸡", "cuisine_indian", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
    ])
    
    # ==================== 意式料理补充 ====================
    dishes.extend([
        ("意大利肉丸", "cuisine_italian", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("意式烤面包", "cuisine_italian", ["meal_breakfast", "meal_afternoon_tea"], ["food_pancake"], ["dish_snack"]),
        ("意式奶冻", "cuisine_italian", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("意式蔬菜汤", "cuisine_italian", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("意式咖啡", "cuisine_italian", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 法式料理补充 ====================
    dishes.extend([
        ("法式可丽饼", "cuisine_french", ["meal_breakfast", "meal_afternoon_tea"], ["food_pancake"], ["dish_staple"]),
        ("法式鹅肝酱", "cuisine_french", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_appetizer"]),
        ("法式洋葱汤", "cuisine_french", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("法式舒芙蕾", "cuisine_french", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("法式香槟", "cuisine_french", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 西班牙菜补充 ====================
    dishes.extend([
        ("西班牙海鲜饭", "cuisine_spanish", ["meal_lunch", "meal_dinner"], ["food_seafood", "food_rice"], ["dish_staple"]),
        ("西班牙土豆蛋饼", "cuisine_spanish", ["meal_breakfast", "meal_lunch"], ["food_pancake", "food_poultry"], ["dish_staple"]),
        ("西班牙冷汤", "cuisine_spanish", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("西班牙油条巧克力", "cuisine_spanish", ["meal_breakfast", "meal_afternoon_tea"], ["food_snack", "food_dessert"], ["dish_snack"]),
        ("西班牙果酒", "cuisine_spanish", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 德式料理补充 ====================
    dishes.extend([
        ("德国烤猪膝", "cuisine_german", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("德国香肠拼盘", "cuisine_german", ["meal_lunch", "meal_dinner"], ["food_pork"], ["dish_main"]),
        ("德国碱水结", "cuisine_german", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("德国苹果卷", "cuisine_german", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("德国小麦啤酒", "cuisine_german", ["meal_dinner"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 美式料理补充 ====================
    dishes.extend([
        ("美式煎饼", "cuisine_american", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("美式烧烤肋排", "cuisine_american", ["meal_lunch", "meal_dinner"], ["food_pork", "food_bbq"], ["dish_main"]),
        ("美式水牛城鸡翅", "cuisine_american", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_snack"]),
        ("美式苹果派", "cuisine_american", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("美式冰咖啡", "cuisine_american", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 墨西哥菜补充 ====================
    dishes.extend([
        ("墨西哥玉米饼", "cuisine_mexican", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("墨西哥卷饼", "cuisine_mexican", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_pancake"], ["dish_staple"]),
        ("墨西哥玉米片配 salsa", "cuisine_mexican", ["meal_lunch", "meal_dinner"], ["food_snack"], ["dish_snack"]),
        ("墨西哥鳄梨酱", "cuisine_mexican", ["meal_lunch", "meal_dinner"], ["food_vegetarian"], ["dish_snack"]),
        ("墨西哥三奶蛋糕", "cuisine_mexican", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
    ])
    
    # ==================== 中东菜补充 ====================
    dishes.extend([
        ("中东法拉费", "cuisine_middle_eastern", ["meal_breakfast", "meal_lunch"], ["food_vegetarian"], ["dish_snack"]),
        ("中东胡姆斯酱", "cuisine_middle_eastern", ["meal_breakfast", "meal_lunch"], ["food_vegetarian"], ["dish_snack"]),
        ("中东沙威玛", "cuisine_middle_eastern", ["meal_lunch", "meal_dinner"], ["food_meat"], ["dish_staple"]),
        ("中东皮塔饼", "cuisine_middle_eastern", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("中东土耳其咖啡", "cuisine_middle_eastern", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 新加坡菜补充 ====================
    dishes.extend([
        ("新加坡辣椒螃蟹", "cuisine_singapore", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("新加坡黑胡椒螃蟹", "cuisine_singapore", ["meal_lunch", "meal_dinner"], ["food_seafood"], ["dish_main"]),
        ("新加坡咖椰吐司", "cuisine_singapore", ["meal_breakfast"], ["food_pancake"], ["dish_staple"]),
        ("新加坡九层糕", "cuisine_singapore", ["meal_afternoon_tea"], ["food_dessert"], ["dish_dessert"]),
        ("新加坡拉茶", "cuisine_singapore", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 西餐通用补充 ====================
    dishes.extend([
        ("西式三明治", "cuisine_western", ["meal_breakfast", "meal_lunch"], ["food_pancake"], ["dish_staple"]),
        ("西式凯撒沙拉", "cuisine_western", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_salad"], ["dish_salad"]),
        ("西式奶油蘑菇汤", "cuisine_western", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_soup"], ["dish_soup"]),
        ("西式烤鸡", "cuisine_western", ["meal_lunch", "meal_dinner"], ["food_poultry"], ["dish_main"]),
        ("西式咖啡", "cuisine_western", ["meal_breakfast", "meal_afternoon_tea"], ["food_beverage"], ["dish_beverage"]),
    ])
    
    # ==================== 其他/通用补充 ====================
    dishes.extend([
        ("番茄炒蛋", "cuisine_other", ["meal_breakfast", "meal_lunch", "meal_dinner"], ["food_poultry", "food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("酸辣土豆丝", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("地三鲜", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("可乐鸡翅", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stew"], ["dish_main"]),
        ("蒜蓉西兰花", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("麻婆豆腐", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_vegetarian", "food_stirfry"], ["dish_main"]),
        ("宫保鸡丁", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_poultry", "food_stirfry"], ["dish_main"]),
        ("鱼香肉丝", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stirfry"], ["dish_main"]),
        ("糖醋排骨", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
        ("红烧狮子头", "cuisine_other", ["meal_lunch", "meal_dinner"], ["food_pork", "food_stew"], ["dish_main"]),
    ])
    
    return dishes


def main():
    print("Loading data...")
    data = load_data()
    
    print("Generating supplement dishes...")
    dishes = generate_supplement_dishes()
    
    print(f"Adding {len(dishes)} new dishes...")
    add_dishes(data, dishes)
    
    print(f"Total items now: {len(data['items'])}")
    
    # 保存文件
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    
    with open('js/ingredients.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    with open('miniprogram/data/ingredients.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    
    print("Done! Files saved.")
    
    # 验证分布
    cuisine_count = {}
    for item in data['items']:
        for cat in item['categories']:
            if cat.startswith('cuisine_'):
                cuisine_count[cat] = cuisine_count.get(cat, 0) + 1
    
    all_cuisines = {v['id']: v['name'] for k, v in data['categories']['cuisine'].items()}
    
    print("\n=== Updated Distribution ===")
    empty_count = 0
    low_count = 0
    for cid, cname in sorted(all_cuisines.items()):
        count = cuisine_count.get(cid, 0)
        if count == 0:
            status = 'EMPTY'
            empty_count += 1
        elif count < 5:
            status = 'LOW'
            low_count += 1
        else:
            status = 'OK'
        print(f'{cname}: {count} ({status})')
    
    print(f"\nEmpty cuisines: {empty_count}")
    print(f"Low count cuisines (<5): {low_count}")
    print(f"Total items: {len(data['items'])}")


if __name__ == '__main__':
    main()
