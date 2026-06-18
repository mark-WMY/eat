const fs = require('fs');
let id = 4100;
function E(n, c, h = [], a = [], s = []) {
  const e = { id: `item_${String(id).padStart(5, '0')}`, name: n, categories: c, attributes: { health: h, allergens: a } };
  if (s.length) e.attributes.searchAliases = s;
  id++; return e;
}

const common = [
  // 川菜
  E('重庆烧鸡公',['cuisine_chongqing','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_chili'],[],[],[]),
  E('烟熏鸭',['cuisine_chuan','meal_lunch','meal_dinner','food_poultry','dish_main'],[],[],[]),
  E('麻辣牛肉干',['cuisine_chuan','meal_lunch','meal_dinner','food_beef','dish_snack','allergen_chili','allergen_sesame'],[],[],[]),

  // 家常
  E('菠菜蛋花汤',['cuisine_other','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_egg'],[],['egg'],[]),

  // 日式
  E('日式咖喱乌冬',['cuisine_japanese','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_dairy'],[],[],[]),
  E('日式咖喱面包',['cuisine_japanese','meal_lunch','food_pancake','dish_snack','allergen_gluten','allergen_chili','allergen_dairy'],[],[],[]),
  E('日式咖喱猪排',['cuisine_japanese','meal_lunch','meal_dinner','food_pork','dish_main','allergen_gluten','allergen_chili','allergen_egg'],[],[],[]),
  E('蘸面',['cuisine_japanese','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy'],[],[],[]),
  E('日式军舰卷',['cuisine_japanese','meal_lunch','meal_dinner','food_seafood','dish_appetizer','allergen_fish','allergen_soy'],[],[],[]),
  E('日式太卷',['cuisine_japanese','meal_lunch','meal_dinner','food_seafood','dish_appetizer','allergen_fish','allergen_soy'],[],[],[]),
  E('日式荞麦面',['cuisine_japanese','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy'],[],[],[]),
  E('日式冷面',['cuisine_japanese','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_egg'],[],[],[]),
  E('日式炒面',['cuisine_japanese','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy'],[],[],[]),
  E('日式茶碗蒸',['cuisine_japanese','meal_lunch','meal_dinner','food_egg','dish_appetizer','allergen_egg','allergen_shellfish'],[],[],[]),

  // 韩式
  E('韩式萝卜泡菜',['cuisine_korean','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_chili','allergen_soy','allergen_shellfish'],[],[],[]),
  E('韩式小菜',['cuisine_korean','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_soy'],[],[],[]),
  E('韩式泡菜豆腐汤',['cuisine_korean','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_chili','allergen_soy','allergen_shellfish'],[],[],[]),
  E('韩式泡菜饼',['cuisine_korean','meal_lunch','meal_dinner','food_pancake','dish_snack','allergen_gluten','allergen_chili','allergen_soy','allergen_shellfish'],[],[],[]),
  E('韩式泡菜拉面',['cuisine_korean','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy','allergen_shellfish'],[],[],[]),
  E('韩式泡菜饺子',['cuisine_korean','meal_lunch','meal_dinner','food_dumpling','dish_staple','allergen_gluten','allergen_chili','allergen_soy','allergen_shellfish'],[],[],[]),

  // 泰式
  E('泰式沙拉',['cuisine_thai','meal_lunch','meal_dinner','food_vegetarian','dish_salad','allergen_chili','allergen_shellfish'],[],[],[]),

  // 意式
  E('意式腊肠披萨',['cuisine_italian','meal_lunch','meal_dinner','food_pork','food_pancake','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),
  E('海鲜披萨',['cuisine_italian','meal_lunch','meal_dinner','food_seafood','food_pancake','dish_main','allergen_gluten','allergen_dairy','allergen_shellfish'],[],[],[]),
  E('意式卡布奇诺',['cuisine_italian','meal_breakfast','meal_afternoon_tea','food_coffee','dish_beverage','allergen_dairy'],[],[],[]),
  E('意式拿铁',['cuisine_italian','meal_breakfast','meal_afternoon_tea','food_coffee','dish_beverage','allergen_dairy'],[],[],[]),
  E('法式蜗牛',['cuisine_french','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_dairy'],[],[],[]),
  E('意式浓缩',['cuisine_italian','meal_breakfast','meal_afternoon_tea','food_coffee','dish_beverage'],[],[],[]),
  E('虾仁沙拉',['cuisine_western','meal_lunch','meal_dinner','food_seafood','dish_salad','allergen_shellfish'],[],[],[]),

  // 墨西哥
  E('墨西哥taco',['cuisine_mexican','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_chili'],[],[],[]),
  E('墨西哥burrito',['cuisine_mexican','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_chili','allergen_dairy'],[],[],[]),
  E('墨西哥fajita',['cuisine_mexican','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_chili'],[],[],[]),
  E('墨西哥quesadilla',['cuisine_mexican','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),
  E('墨西哥nachos',['cuisine_mexican','meal_afternoon_tea','meal_midnight','food_snack','dish_snack','allergen_gluten','allergen_dairy','allergen_chili'],[],[],[]),
  E('墨西哥guacamole',['cuisine_mexican','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_chili'],[],[],[]),

  // 印度
  E('印度咖喱羊',['cuisine_indian','meal_lunch','meal_dinner','food_lamb','dish_main','allergen_chili','allergen_dairy'],[],[],[]),
  E('印度咖喱鱼',['cuisine_indian','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish','allergen_chili','allergen_dairy'],[],[],[]),
  E('印度炸三角',['cuisine_indian','meal_afternoon_tea','food_vegetarian','dish_snack','allergen_gluten'],[],[],[]),

  // 马来西亚
  E('马来西亚福建面',['cuisine_malaysian','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_chili'],[],[],[]),
  E('马来西亚白咖啡',['cuisine_malaysian','meal_afternoon_tea','food_coffee','dish_beverage','allergen_dairy'],[],[],[]),

  // 印尼
  E('印尼仁当牛肉',['cuisine_other','meal_lunch','meal_dinner','food_beef','dish_main','allergen_chili','allergen_dairy'],[],[],[]),
  E('印尼炸鸡',['cuisine_other','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_gluten'],[],[],[]),
  E('印尼烤鱼',['cuisine_other','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish','allergen_chili'],[],[],[]),
  E('印尼椰浆饭',['cuisine_other','meal_lunch','meal_dinner','food_rice','dish_staple','allergen_peanut','allergen_chili'],[],[],[]),
  E('印尼炒面',['cuisine_other','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_chili'],[],[],[]),
  E('印尼汤面',['cuisine_other','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_chili'],[],[],[]),

  // 菲律宾
  E('菲律宾阿斗波',['cuisine_other','meal_lunch','meal_dinner','food_pork','dish_main','allergen_soy'],[],[],[]),
  E('菲律宾酸汤',['cuisine_other','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_shellfish'],[],[],[]),
  E('菲律宾halohalo',['cuisine_other','meal_afternoon_tea','food_dessert','dish_dessert','allergen_dairy'],[],[],[]),
  E('菲律宾炒面',['cuisine_other','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy'],[],[],[]),

  // 土耳其
  E('土耳其披萨',['cuisine_middle_eastern','meal_lunch','meal_dinner','food_meat','food_pancake','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),
  E('土耳其冰淇淋',['cuisine_middle_eastern','meal_afternoon_tea','food_dessert','dish_dessert','allergen_dairy'],[],[],[]),
  E('土耳其红茶',['cuisine_middle_eastern','meal_afternoon_tea','food_tea','dish_beverage'],[],[],[]),
  E('土耳其烤肉卷',['cuisine_middle_eastern','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),
  E('土耳其馅饼',['cuisine_middle_eastern','meal_lunch','meal_dinner','food_meat','food_pancake','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),
  E('土耳其沙拉',['cuisine_middle_eastern','meal_lunch','meal_dinner','food_vegetarian','dish_salad'],[],[],[]),
  E('土耳其酸奶',['cuisine_middle_eastern','meal_afternoon_tea','food_dessert','dish_beverage','allergen_dairy'],[],[],[]),
  E('土耳其甜点',['cuisine_middle_eastern','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten','allergen_dairy','allergen_tree_nut'],[],[],[]),

  // 希腊
  E('希腊穆萨卡',['cuisine_greek','meal_lunch','meal_dinner','food_meat','dish_main','allergen_dairy','allergen_egg','allergen_gluten'],[],[],[]),
  E('希腊菠菜派',['cuisine_greek','meal_lunch','meal_dinner','food_vegetarian','dish_main','allergen_gluten','allergen_dairy','allergen_egg'],[],[],[]),
  E('希腊炸鱿鱼',['cuisine_greek','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish','allergen_gluten'],[],[],[]),
  E('希腊海鲜',['cuisine_greek','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish','allergen_fish'],[],[],[]),

  // 中东
  E('中东炸豆丸子',['cuisine_middle_eastern','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_gluten'],[],[],[]),

  // 巴西
  E('巴西芝士面包',['cuisine_brazilian','meal_breakfast','meal_afternoon_tea','food_bun','dish_snack','allergen_dairy','allergen_egg','allergen_gluten'],[],[],[]),
  E('巴西椰奶虾',['cuisine_brazilian','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish','allergen_dairy'],[],[],[]),

  // 阿根廷
  E('阿根廷牛排',['cuisine_brazilian','meal_lunch','meal_dinner','food_beef','dish_main','health_high_protein'],[],[],[]),
  E('阿根廷饺子',['cuisine_brazilian','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_egg'],[],[],[]),
  E('阿根廷烤肠',['cuisine_brazilian','meal_lunch','meal_dinner','food_meat','dish_main'],[],[],[]),
  E('阿根廷红酒',['cuisine_brazilian','meal_dinner','food_alcohol','dish_beverage','allergen_sulfite'],[],[],[]),

  // 秘鲁
  E('秘鲁柠檬汁腌鱼',['cuisine_other','meal_lunch','meal_dinner','food_seafood','dish_appetizer','allergen_fish'],[],[],[]),
  E('秘鲁炒牛柳',['cuisine_other','meal_lunch','meal_dinner','food_beef','dish_main','allergen_chili','allergen_soy'],[],[],[]),
  E('秘鲁土豆泥',['cuisine_other','meal_lunch','meal_dinner','food_vegetarian','dish_main','allergen_dairy'],[],[],[]),
  E('秘鲁玉米粒',['cuisine_other','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer'],[],[],[]),

  // 古巴
  E('古巴黑豆饭',['cuisine_other','meal_lunch','meal_dinner','food_rice','dish_staple','health_high_protein','health_high_fiber'],[],[],[]),
  E('古巴肉丝',['cuisine_other','meal_lunch','meal_dinner','food_pork','dish_main'],[],[],[]),
  E('古巴mojito',['cuisine_other','meal_afternoon_tea','meal_midnight','food_alcohol','dish_beverage'],[],[],[]),

  // 夏威夷
  E('夏威夷loco moco',['cuisine_american','meal_lunch','meal_dinner','food_rice','food_beef','dish_staple','allergen_egg'],[],[],[]),
  E('夏威夷午餐肉饭团',['cuisine_american','meal_breakfast','meal_lunch','food_rice','food_meat','dish_snack','allergen_soy'],[],[],[]),
  E('夏威夷烤猪',['cuisine_american','meal_lunch','meal_dinner','food_pork','dish_main','health_high_protein'],[],[],[]),
  E('夏威夷刨冰',['cuisine_american','meal_afternoon_tea','food_dessert','dish_dessert'],[],[],[]),

  // 德州
  E('德州辣豆汤',['cuisine_american','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_chili','allergen_soy'],[],[],[]),
  E('德州玉米卷',['cuisine_american','meal_lunch','meal_dinner','food_meat','dish_main','allergen_gluten','allergen_chili'],[],[],[]),
  E('德州汉堡',['cuisine_american','meal_lunch','meal_dinner','food_beef','dish_main','allergen_gluten','allergen_dairy'],[],[],[]),

  // 摩洛哥
  E('摩洛哥库斯库斯',['cuisine_african','meal_lunch','meal_dinner','food_gluten','dish_staple','allergen_gluten'],[],[],[]),
  E('摩洛哥薄荷茶',['cuisine_african','meal_afternoon_tea','food_tea','dish_beverage'],[],[],[]),
  E('摩洛哥豆汤',['cuisine_african','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_soy'],[],[],[]),
  E('摩洛哥烤肉',['cuisine_african','meal_lunch','meal_dinner','food_beef','food_bbq','dish_main','health_high_protein'],[],[],[]),

  // 埃塞俄比亚
  E('埃塞俄比亚炖菜',['cuisine_african','meal_lunch','meal_dinner','food_meat','food_stew','dish_main','allergen_chili'],[],[],[]),
  E('埃塞俄比亚蜂蜜酒',['cuisine_african','meal_dinner','food_alcohol','dish_beverage','allergen_sulfite'],[],[],[]),
  E('埃塞俄比亚炒肉',['cuisine_african','meal_lunch','meal_dinner','food_beef','dish_main','allergen_chili'],[],[],[]),

  // 饮品
  E('芝士奶盖',['cuisine_other','meal_afternoon_tea','food_tea','dish_beverage','allergen_dairy'],[],[],[]),
  E('米浆',['cuisine_other','meal_breakfast','meal_afternoon_tea','food_grain','dish_beverage'],[],[],[]),
  E('花生浆',['cuisine_other','meal_breakfast','meal_afternoon_tea','food_grain','dish_beverage','allergen_peanut'],[],[],[]),

  // 韩式其他
  E('年糕汤',['cuisine_korean','meal_lunch','meal_dinner','food_rice','dish_soup','allergen_gluten'],[],[],[]),

  // 烧烤
  E('烤鸡胸',['cuisine_western','meal_lunch','meal_dinner','food_poultry','dish_main','health_high_protein','health_low_fat'],[],[],[]),

  // 火锅
  E('鱼滑',['cuisine_yue','meal_lunch','meal_dinner','food_seafood','dish_hotpot','allergen_fish'],[],[],[]),
  E('猪肉滑',['cuisine_yue','meal_lunch','meal_dinner','food_pork','dish_hotpot'],[],[],[]),

  // 速食
  E('自热火锅',['cuisine_other','meal_lunch','meal_dinner','food_meat','food_hotpot','dish_main','allergen_chili','allergen_soy'],[],[],[]),
  E('自热米饭',['cuisine_other','meal_lunch','meal_dinner','food_rice','dish_staple'],[],[],[]),
  E('速食饭',['cuisine_other','meal_lunch','meal_dinner','food_rice','dish_staple'],[],[],[]),
  E('速食粥',['cuisine_other','meal_breakfast','meal_lunch','meal_dinner','food_congee','dish_staple'],[],[],[]),
];

// ===== FULL ONLY =====
const fullOnly = [
  E('双流兔头',['cuisine_chuan','meal_lunch','meal_dinner','meal_midnight','food_meat','dish_snack','allergen_chili','allergen_peanut','allergen_sesame'],[],[],[]),
  E('郴州烧鸡公',['cuisine_xiang','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_chili'],[],[],[]),
  E('整鱼两吃',['cuisine_lu','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish'],[],[],[]),
  E('济南甜沫',['cuisine_lu','meal_breakfast','food_soup','dish_soup','allergen_gluten','allergen_soy','allergen_peanut'],[],[],[]),
  E('济南油旋',['cuisine_lu','meal_breakfast','food_pancake','dish_snack','allergen_gluten'],[],[],[]),
  E('临沂炒鸡',['cuisine_lu','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_chili','allergen_soy'],[],[],[]),
  E('枣庄辣子鸡',['cuisine_lu','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_chili'],[],[],[]),
  E('烟台焖子',['cuisine_lu','meal_lunch','meal_dinner','food_vegetarian','dish_snack','allergen_soy','allergen_garlic','allergen_sesame'],[],[],[]),
  E('烟台海肠',['cuisine_lu','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish'],[],[],[]),
  E('白水羊头',['cuisine_beijing','meal_lunch','meal_dinner','food_lamb','dish_appetizer','allergen_garlic'],[],[],[]),
  E('炸松肉',['cuisine_beijing','meal_lunch','meal_dinner','food_meat','dish_snack','allergen_gluten'],[],[],[]),
  E('炸咯吱',['cuisine_beijing','meal_lunch','meal_dinner','food_vegetarian','dish_snack','allergen_gluten','allergen_soy'],[],[],[]),
  E('糖耳朵',['cuisine_beijing','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten'],[],[],[]),
  E('自来红',['cuisine_beijing','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten','allergen_nut'],[],[],[]),
  E('烧饼夹肉',['cuisine_beijing','meal_breakfast','meal_lunch','food_pancake','food_meat','dish_snack','allergen_gluten'],[],[],[]),
  E('烧羊肉',['cuisine_beijing','meal_lunch','meal_dinner','food_lamb','dish_main','allergen_soy'],[],[],[]),
  E('草帽饼',['cuisine_dongbei','meal_breakfast','meal_lunch','food_pancake','dish_staple','allergen_gluten'],[],[],[]),
  E('手撕饼',['cuisine_dongbei','meal_breakfast','meal_lunch','food_pancake','dish_staple','allergen_gluten'],[],[],[]),
  E('熏鸡架',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_snack'],[],[],[]),
  E('拌鸡架',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_appetizer','allergen_chili','allergen_soy'],[],[],[]),
  E('烤鸡架',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_snack','allergen_chili'],[],[],[]),
  E('蘸酱菜',['cuisine_dongbei','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_soy'],[],[],[]),
  E('凉拌拉皮',['cuisine_dongbei','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_soy','allergen_garlic','allergen_sesame'],[],[],[]),
  E('三丝爆豆',['cuisine_dongbei','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer','allergen_chili','allergen_soy'],[],[],[]),
  E('酥黄菜',['cuisine_dongbei','meal_lunch','meal_dinner','food_egg','dish_main','allergen_egg','allergen_gluten'],[],[],[]),
  E('拔丝白果',['cuisine_dongbei','meal_lunch','meal_dinner','food_egg','dish_dessert','allergen_egg'],[],[],[]),
  E('杨凌蘸水面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili'],[],[],[]),
  E('户县软面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('秦镇米皮',['cuisine_northwest','meal_breakfast','meal_lunch','meal_dinner','food_rice','dish_staple','allergen_chili'],[],[],[]),
  E('粉汤羊血',['cuisine_northwest','meal_breakfast','meal_lunch','food_soup','dish_soup','allergen_chili','allergen_gluten'],[],[],[]),
  E('梆梆肉',['cuisine_northwest','meal_lunch','meal_dinner','food_meat','dish_snack','allergen_soy'],[],[],[]),
  E('腊牛羊肉',['cuisine_northwest','meal_lunch','meal_dinner','food_beef','food_lamb','dish_main'],[],[],[]),
  E('羊肉小炒',['cuisine_northwest','meal_lunch','meal_dinner','food_lamb','dish_main','allergen_gluten','allergen_chili'],[],[],[]),
  E('贾三灌汤包',['cuisine_northwest','meal_breakfast','meal_lunch','meal_dinner','food_bun','dish_snack','allergen_gluten'],[],[],[]),
  E('兰州炒面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy'],[],[],[]),
  E('兰州烩面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten'],[],[],[]),
  E('兰州酿皮',['cuisine_northwest','meal_breakfast','meal_lunch','meal_dinner','food_gluten','dish_staple','allergen_gluten','allergen_sesame','allergen_chili'],[],[],[]),
  E('兰州灰豆子',['cuisine_northwest','meal_afternoon_tea','food_dessert','dish_dessert','allergen_soy'],[],[],[]),
  E('天水凉粉',['cuisine_northwest','meal_lunch','meal_dinner','food_vegetarian','dish_snack','allergen_soy','allergen_chili','allergen_sesame'],[],[],[]),
  E('天水杂烩',['cuisine_northwest','meal_lunch','meal_dinner','food_meat','food_soup','dish_main'],[],[],[]),
  E('嘉峪关烤肉',['cuisine_northwest','meal_lunch','meal_dinner','meal_midnight','food_bbq','food_lamb','dish_main','allergen_chili'],[],[],[]),
  E('新疆薄皮包子',['cuisine_xinjiang','meal_breakfast','meal_lunch','meal_dinner','food_bun','food_lamb','dish_snack','allergen_gluten','allergen_onion'],[],[],[]),
  E('新疆盆盆肉',['cuisine_xinjiang','meal_lunch','meal_dinner','food_lamb','food_soup','dish_main','allergen_chili'],[],[],[]),
  E('新疆大盘肚',['cuisine_xinjiang','meal_lunch','meal_dinner','food_meat','dish_main','allergen_chili'],[],[],[]),
  E('新疆丸子汤',['cuisine_xinjiang','meal_lunch','meal_dinner','food_soup','dish_soup','allergen_gluten'],[],[],[]),
  E('新疆扁豆面旗子',['cuisine_xinjiang','meal_breakfast','meal_lunch','food_noodles','dish_soup','allergen_gluten','allergen_soy'],[],[],[]),
  E('新疆炮仗子',['cuisine_xinjiang','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('新疆丁丁炒面',['cuisine_xinjiang','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_chili'],[],[],[]),
  E('青海尕面片',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili'],[],[],[]),
  E('青海羊肠面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili'],[],[],[]),
  E('青海手抓',['cuisine_northwest','meal_lunch','meal_dinner','food_lamb','dish_main'],[],[],[]),
  E('宁夏手抓',['cuisine_northwest','meal_lunch','meal_dinner','food_lamb','dish_main'],[],[],[]),
  E('宁夏烩小吃',['cuisine_northwest','meal_lunch','meal_dinner','food_meat','food_soup','dish_main','allergen_gluten','allergen_chili'],[],[],[]),
  E('宁夏炒糊饽',['cuisine_northwest','meal_lunch','meal_dinner','food_pancake','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('宁夏羊肉搓面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili'],[],[],[]),
  E('宁夏羊肉臊子面',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('宁夏燕面揉揉',['cuisine_northwest','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili'],[],[],[]),
  E('宁夏搅团',['cuisine_northwest','meal_lunch','meal_dinner','food_grain','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('蟹粉生煎',['cuisine_shanghai','meal_breakfast','meal_lunch','food_bun','dish_snack','allergen_gluten','allergen_shellfish'],[],[],[]),
  E('扁肉燕',['cuisine_min','meal_breakfast','meal_lunch','food_meat','dish_snack','allergen_gluten'],[],[],[]),
  E('白炒鲜鱿',['cuisine_min','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish'],[],[],[]),
  E('虾酱蒸肉',['cuisine_min','meal_lunch','meal_dinner','food_pork','dish_main','allergen_shellfish'],[],[],[]),
  E('八宝芋泥',['cuisine_min','meal_afternoon_tea','food_dessert','dish_dessert','allergen_tree_nut'],[],[],[]),
  E('马耳',['cuisine_min','meal_breakfast','meal_afternoon_tea','food_snack','dish_snack','allergen_gluten'],[],[],[]),
  E('礼饼',['cuisine_min','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten','allergen_tree_nut'],[],[],[]),
  E('芋粿',['cuisine_min','meal_breakfast','meal_lunch','food_vegetarian','dish_snack','allergen_gluten'],[],[],[]),
  E('虾酥',['cuisine_min','meal_breakfast','meal_lunch','food_snack','dish_snack','allergen_gluten','allergen_shellfish'],[],[],[]),
  E('肉燕皮',['cuisine_min','meal_breakfast','meal_lunch','food_meat','dish_snack'],[],[],[]),
  E('燕皮馄饨',['cuisine_min','meal_breakfast','meal_lunch','meal_dinner','food_dumpling','dish_staple','allergen_gluten'],[],[],[]),
  E('福州芋泥',['cuisine_min','meal_afternoon_tea','food_dessert','dish_dessert'],[],[],[]),
  E('福州春卷',['cuisine_min','meal_breakfast','meal_lunch','food_vegetarian','dish_snack','allergen_gluten'],[],[],[]),
  E('闽南肉粽',['cuisine_min','meal_breakfast','meal_lunch','food_rice','food_pork','dish_staple','allergen_gluten'],[],[],[]),
  E('石花膏',['cuisine_min','meal_afternoon_tea','food_dessert','dish_dessert'],[],[],[]),
  E('温州鸭舌',['cuisine_zhe','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_snack','allergen_soy'],[],[],[]),
  E('温州鱼饼',['cuisine_zhe','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish','allergen_gluten'],[],[],[]),
  E('宁波年糕',['cuisine_zhe','meal_lunch','meal_dinner','food_rice','dish_staple','allergen_gluten'],[],[],[]),
  E('绍兴酱鸭',['cuisine_zhe','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_soy'],[],[],[]),
  E('金华煲',['cuisine_zhe','meal_lunch','meal_dinner','food_meat','food_stew','dish_main','allergen_soy'],[],[],[]),
  E('龙游发糕',['cuisine_zhe','meal_breakfast','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten'],[],[],[]),
  E('缙云烧饼',['cuisine_zhe','meal_breakfast','meal_lunch','food_pancake','dish_snack','allergen_gluten'],[],[],[]),
  E('衢州鸭头',['cuisine_zhe','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_snack','allergen_chili','allergen_soy'],[],[],[]),
  E('舟山带鱼',['cuisine_zhe','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish'],[],[],[]),
  E('舟山黄鱼',['cuisine_zhe','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_fish'],[],[],[]),
  E('台州海鲜面',['cuisine_zhe','meal_lunch','meal_dinner','food_noodles','food_seafood','dish_staple','allergen_gluten','allergen_shellfish','allergen_fish'],[],[],[]),
  E('台州嵌糕',['cuisine_zhe','meal_breakfast','meal_lunch','food_rice','dish_staple','allergen_gluten'],[],[],[]),
  E('桐乡煲',['cuisine_zhe','meal_lunch','meal_dinner','food_meat','food_stew','dish_main','allergen_chili','allergen_soy'],[],[],[]),
  E('湖州千张包',['cuisine_zhe','meal_lunch','meal_dinner','food_meat','dish_main','allergen_soy'],[],[],[]),
  E('湖州粽子',['cuisine_zhe','meal_breakfast','meal_afternoon_tea','food_rice','dish_dessert','allergen_gluten'],[],[],[]),
  E('嘉兴酱鸭',['cuisine_zhe','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_soy'],[],[],[]),
  E('杭州小笼',['cuisine_zhe','meal_breakfast','meal_lunch','food_bun','dish_snack','allergen_gluten'],[],[],[]),
  E('吴山烤禽',['cuisine_zhe','meal_lunch','meal_dinner','food_poultry','dish_main'],[],[],[]),
  E('杭州定胜糕',['cuisine_zhe','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten'],[],[],[]),
  E('杭州葱包烩',['cuisine_zhe','meal_breakfast','meal_lunch','food_pancake','dish_snack','allergen_gluten','allergen_soy','allergen_chili'],[],[],[]),
  E('无锡面筋',['cuisine_su','meal_lunch','meal_dinner','food_vegetarian','dish_main','allergen_gluten','allergen_soy'],[],[],[]),
  E('无锡肉骨头',['cuisine_su','meal_lunch','meal_dinner','food_pork','dish_main','allergen_soy'],[],[],[]),
  E('常州萝卜干',['cuisine_su','meal_breakfast','meal_lunch','meal_dinner','food_vegetarian','dish_appetizer'],[],[],[]),
  E('常州大麻糕',['cuisine_su','meal_breakfast','meal_afternoon_tea','food_pancake','dish_snack','allergen_gluten','allergen_sesame'],[],[],[]),
  E('徐州辣汤',['cuisine_su','meal_breakfast','food_soup','dish_soup','allergen_gluten','allergen_chili','allergen_egg'],[],[],[]),
  E('徐州伏羊',['cuisine_su','meal_lunch','meal_dinner','food_lamb','dish_main','allergen_chili'],[],[],[]),
  E('淮安茶馓',['cuisine_su','meal_breakfast','meal_afternoon_tea','food_snack','dish_snack','allergen_gluten'],[],[],[]),
  E('淮安蒲菜',['cuisine_su','meal_lunch','meal_dinner','food_vegetarian','dish_main'],[],[],[]),
  E('苏州面拖蟹',['cuisine_su','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish','allergen_gluten','allergen_egg'],[],[],[]),
  E('苏州枫镇大面',['cuisine_su','meal_breakfast','meal_lunch','food_noodles','dish_staple','allergen_gluten','allergen_soy','allergen_pork'],[],[],[]),
  E('苏州绉纱汤包',['cuisine_su','meal_breakfast','meal_lunch','food_bun','dish_snack','allergen_gluten'],[],[],[]),
  E('南京烤鸭',['cuisine_su','meal_lunch','meal_dinner','food_poultry','dish_main','allergen_soy'],[],[],[]),
  E('南京牛肉锅贴',['cuisine_su','meal_breakfast','meal_lunch','food_dumpling','dish_snack','allergen_gluten'],[],[],[]),
  E('南京小馄饨',['cuisine_su','meal_breakfast','meal_lunch','meal_dinner','food_dumpling','dish_staple','allergen_gluten'],[],[],[]),
  E('南京皮肚面',['cuisine_su','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('南京梅花糕',['cuisine_su','meal_breakfast','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten'],[],[],[]),
  E('南京赤豆元宵',['cuisine_su','meal_breakfast','meal_afternoon_tea','food_dessert','dish_dessert','allergen_gluten'],[],[],[]),
  E('南京蜜汁藕',['cuisine_su','meal_breakfast','meal_afternoon_tea','food_vegetarian','dish_dessert'],[],[],[]),
  E('南京芦蒿炒香干',['cuisine_su','meal_lunch','meal_dinner','food_vegetarian','dish_main','allergen_soy'],[],[],[]),
  E('屯溪烧饼',['cuisine_anhui','meal_breakfast','meal_afternoon_tea','food_pancake','dish_snack','allergen_gluten'],[],[],[]),
  E('合肥炸串',['cuisine_anhui','meal_lunch','meal_dinner','meal_midnight','food_meat','dish_snack','allergen_gluten','allergen_chili'],[],[],[]),
  E('蚌埠烧饼夹里脊',['cuisine_anhui','meal_breakfast','meal_lunch','food_pancake','food_pork','dish_snack','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('日式相扑锅',['cuisine_japanese','meal_lunch','meal_dinner','food_meat','food_seafood','food_hotpot','dish_main','allergen_soy'],[],[],[]),
  E('日式石狩锅',['cuisine_japanese','meal_lunch','meal_dinner','food_seafood','food_hotpot','dish_main','allergen_fish','allergen_soy','allergen_dairy'],[],[],[]),
  E('印尼加多加多',['cuisine_other','meal_lunch','meal_dinner','food_vegetarian','dish_salad','allergen_peanut','allergen_chili'],[],[],[]),
  E('新疆烤包子',['cuisine_xinjiang','meal_breakfast','meal_lunch','meal_dinner','food_bun','food_lamb','dish_snack','allergen_gluten','allergen_onion'],[],[],[]),
  E('新疆炒面',['cuisine_xinjiang','meal_lunch','meal_dinner','food_noodles','dish_staple','allergen_gluten','allergen_chili','allergen_soy'],[],[],[]),
  E('辣酱油',['cuisine_shanghai','meal_lunch','meal_dinner','food_condiment','dish_condiment','allergen_chili','allergen_soy'],[],[],[]),
  E('单县羊汤',['cuisine_lu','meal_breakfast','meal_lunch','meal_dinner','food_soup','food_lamb','dish_soup','health_nourishing'],[],[],[]),
  E('菏泽羊汤',['cuisine_lu','meal_breakfast','meal_lunch','meal_dinner','food_soup','food_lamb','dish_soup','health_nourishing'],[],[],[]),
  E('青岛锅贴',['cuisine_lu','meal_breakfast','meal_lunch','food_dumpling','dish_snack','allergen_gluten','allergen_seafood'],[],[],[]),
  E('烤实蛋',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_egg','dish_snack','allergen_egg','allergen_chili'],[],[],[]),
  E('烤毛蛋',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_egg','food_poultry','dish_snack','allergen_chili'],[],[],[]),
  E('烤腰子',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_meat','dish_snack','allergen_chili'],[],[],[]),
  E('烤心管',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_meat','dish_snack','allergen_chili'],[],[],[]),
  E('烤鸽子',['cuisine_dongbei','meal_lunch','meal_dinner','meal_midnight','food_poultry','dish_main','allergen_chili'],[],[],[]),
  E('连云港海鲜',['cuisine_su','meal_lunch','meal_dinner','food_seafood','dish_main','allergen_shellfish','allergen_fish'],[],[],[]),
  E('长沙臭干子',['cuisine_xiang','meal_lunch','meal_dinner','meal_midnight','food_vegetarian','dish_snack','allergen_chili','allergen_soy'],[],[],[]),
  E('冒午餐肉',['cuisine_chuan','meal_lunch','meal_dinner','food_meat','dish_snack','allergen_chili','allergen_soy'],[],[],[]),
  E('冒素菜',['cuisine_chuan','meal_lunch','meal_dinner','food_vegetarian','dish_main','allergen_chili'],[],[],[]),
];

// Execute
const commonDB = JSON.parse(fs.readFileSync('./js/ingredients_common.json', 'utf8'));
const fullDB = JSON.parse(fs.readFileSync('./js/ingredients_full.json', 'utf8'));
const ec = new Set(commonDB.items.map(x => x.name));
const ef = new Set(fullDB.items.map(x => x.name));

let ca = 0, fa = 0;
for (const e of common) {
  if (ec.has(e.name)) { console.log('SKIP c: ' + e.name); continue; }
  commonDB.items.push(e); ec.add(e.name); ca++;
}
for (const e of [...common, ...fullOnly]) {
  if (ef.has(e.name)) { console.log('SKIP f: ' + e.name); continue; }
  fullDB.items.push(e); ef.add(e.name); fa++;
}

fs.writeFileSync('./js/ingredients_common.json', JSON.stringify(commonDB, null, 4), 'utf8');
fs.writeFileSync('./js/ingredients_full.json', JSON.stringify(fullDB, null, 4), 'utf8');
console.log('Common: +' + ca + ' total:' + commonDB.items.length);
console.log('Full: +' + fa + ' total:' + fullDB.items.length);