---
name: "food-db-maintenance"
description: "食材数据库5项维护操作：ADD常见菜品、SYNC到full、MOVE地域条目、DELETE虚构条目、验证JSON。Invoke when user asks for food database maintenance, adding/removing items, or cleaning ingredients data."
references:
  - "AGENTS.md (项目全局规则)"
  - ".trae/skills/food-db-cleaner/SKILL.md (删除/移动规则)"
---

# 食材数据库维护工具

> **前置必读**: 操作前必须先阅读 `AGENTS.md` 和 `food-db-cleaner/SKILL.md`。本 SKILL 是对数据库维护完整流程的标准化指南。

## 适用场景

当用户提出以下类型请求时调用本技能：
- "对食材数据文件进行系统性更新与维护"
- "添加常见菜品到数据库"
- "清理数据库中不存在的条目"
- "移除 common 中不常见的食材"
- 任何涉及 ingredients_common.json / ingredients_full.json 的增删改操作

## 核心原则

### 1. Common ⊆ Full 永远成立
- `ingredients_common.json` 是 `ingredients_full.json` 的子集
- 任何添加到 common 的条目必须同步添加到 full
- 修改后必须验证此关系

### 2. 真实性原则
- 所有条目必须是真实存在的菜品/饮品
- 禁止添加虚构、AI 生成、编造的菜品
- 仅在条目现实中确实不存在时才从 full 删除

### 3. 全国性原则（Common 准入）
- Common 条目必须覆盖国内 ≥3 个省份
- 地域性过强（1-2省）的条目只放入 full
- 全国连锁/普及的地方菜可保留在 common

## 五项标准维护任务

### 任务1：ADD — 添加常见菜品到 Common
**目标**: 补充日常生活中常见但数据库中缺失的菜品/饮品

**执行步骤**:
1. 列出候选菜品（从日常饮食、菜系代表菜、常见饮品等方面 brainstorm）
2. 检查候选是否已存在于数据库（common ∪ full）
3. 筛选：真实存在 + 全国常见（≥3省覆盖）
4. 分配新 ID（接续当前最大 `item_XXXXX` 编号）
5. 填写分类标签（categories）、健康标签（health）、过敏原（allergens）
6. 同步添加到 common 和 full

**常见遗漏类型**:
- 家常菜：鸡蛋汤、黄瓜鸡蛋汤、竹笋炒肉、蘑菇炒肉
- 主食类：荷叶饼、稀饭、泡饭、萝卜干
- 素食类：凉拌豆腐丝、面筋、油面筋、蒜蓉蒸金针菇
- 蛋类：煮鸡蛋、蛋羹
- 其他：香菇饺子、松子鱼

### 任务2：SYNC — 同步 Common 到 Full
**目标**: 确保 common 是 full 的子集

**执行步骤**:
1. 提取 common 所有条目名称
2. 提取 full 所有条目名称
3. 计算 common - full（common 有但 full 没有的）
4. 将缺失的条目从 common 复制到 full
5. 验证：common ⊆ full = True

**注意**: 通常与任务1合并执行，新增条目时直接同步添加。

### 任务3：MOVE — Common 中不常见条目移至 Full
**目标**: 确保 common 仅保留全国常见菜品

**判定标准**（符合任一即 MOVE）:

| 类型 | 示例 | 说明 |
|------|------|------|
| 单省地域菜 | 烤乳扇、糌粑、酥油茶 | 仅在特定省份/地区食用 |
| 前缀冗余 | 东北地三鲜、东北锅包肉 | 基础菜名已存在，前缀为地域强调 |
| 后缀冗余 | 麻辣烫套餐、拉面套餐 | 基础菜名已存在，后缀为组合形式 |
| 小众外国菜 | 春川炒鸡、米肠 | 非全国普及的外国菜 |
| 场景前缀 | 公司三明治、欧陆早餐 | 场景名称，非菜品本身 |

**保留情况**（符合任一即 KEEP in common）:
- 全国连锁普及（兰州拉面、沙县小吃、螺蛳粉）
- 基础菜名不存在（东北乱炖 → 乱炖 不存在）
- 不同菜系的独立做法（日式拉面 ≠ 拉面，韩式烤肉 ≠ 烤肉）

### 任务4：CONDITIONAL DELETE — 条件删除
**目标**: 仅删除现实中不存在的条目，真实条目保留在 full

**执行逻辑**:
```
if 条目在现实中不存在:
    从 full 删除
    如果 common 中也有，同步删除
else:
    仅从 common 移除（MOVE），保留在 full
```

### 任务5：DELETE FICTIONAL — 删除虚构条目
**目标**: 从 full 中彻底删除现实中不存在的条目

**虚构/非菜品特征识别**:

| 特征类型 | 识别模式 | 示例 |
|----------|----------|------|
| AI场景前缀 | 孕妇/老年/糖尿/减肥/救灾/军用/酒店/食堂/大锅 | 老年蒸蛋、糖尿病餐 |
| 品类标签 | 地域+品类的通用描述（非具体菜名） | 中东烤肉、印度豆类汤 |
| 非食材 | 水的状态、通用物质名称 | 温水、矿泉水、纯净水 |
| 品牌名 | 具体品牌产品 | 可口可乐、星巴克拿铁 |
| 括号冗余 | 基础菜名已存在，括号内为变体 | 麻婆豆腐(微辣) |
| 套餐冗余 | 基础菜名已存在，套餐后缀 | 兰州拉面套餐 |

**保留情况**:
- 品牌名：真实产品，但不放入 common，保留在 full
- 宴席前缀：菜品真实，场景形式，保留在 full

## 数据结构规范

### 条目格式
```json
{
  "id": "item_08623",
  "name": "荷叶饼",
  "categories": ["cuisine_other", "meal_lunch", "meal_dinner", "dish_staple"],
  "attributes": {
    "health": [],
    "allergens": ["allergen_gluten"],
    "searchAliases": ["别名1"]
  }
}
```

### 常用分类参考
| 分类前缀 | 含义 | 示例 |
|----------|------|------|
| `cuisine_` | 菜系 | cuisine_chuan, cuisine_japanese |
| `meal_` | 时段 | meal_breakfast, meal_lunch, meal_dinner |
| `food_` | 食材/做法类型 | food_vegetarian, food_soup, food_stirfry |
| `dish_` | 菜品类型 | dish_main, dish_soup, dish_snack, dish_staple |
| `health_` | 健康属性 | health_low_calorie, health_nourishing |
| `allergen_` | 过敏原 | allergen_gluten, allergen_soy, allergen_egg |

## 标准执行流程

### 阶段1：分析（_analyze.py）
```
1. 读取两个 JSON 文件
2. 计算统计数据（条目数、子集关系、full-only 数量）
3. ADD候选：列出常见菜品，检查缺失
4. MOVE候选：扫描地域前缀、套餐后缀、地域特征词
5. DELETE候选：扫描AI场景前缀、品类标签、括号冗余
6. 输出候选清单供人工确认
```

### 阶段2：详查（_check.py）
```
1. 逐条检查ADD候选：是否真实、是否全国常见
2. 逐条检查MOVE候选：判断KEEP或MOVE
3. 逐条检查DELETE候选：判断DELETE或保留
4. 查看现有条目的结构，确保格式一致
5. 输出最终操作清单
```

### 阶段3：执行（_execute.py）
```
1. 读取 JSON 文件，构建 name→item 字典
2. 计算最大 ID，分配新编号
3. 执行 DELETE（从 common 和 full 中删除）
4. 执行 MOVE（从 common 删除，确保 full 中有）
5. 执行 ADD（创建新条目，添加到 common 和 full）
6. 写回 JSON 文件
7. 内置验证：子集关系、重复检查、结构检查
```

### 阶段4：独立验证（_verify.py）
```
1. 独立脚本读取写入后的文件
2. 验证：条目数、子集关系、名称重复、ID重复
3. 验证：结构完整性（所有必要字段存在）
4. 验证：ADD/MOVE/DELETE 抽样检查
5. 输出 PASS / FAIL
```

### 阶段5：清理
```
1. 删除所有临时脚本（_analyze.py, _check.py, _execute.py, _verify.py）
2. 删除中间输出文件（_common_names.txt, _full_only_names.txt 等）
3. 如有存档需求，将脚本移入 scripts/ 目录
```

## 验证清单

每次维护后必须确认：
- [ ] Common ⊆ Full = True
- [ ] Common 名称重复 = 0
- [ ] Full 名称重复 = 0
- [ ] Common ID 重复 = 0
- [ ] Full ID 重复 = 0
- [ ] 所有条目结构完整（id, name, categories, attributes{health, allergens}）
- [ ] JSON 语法正确（可被 json.load 正常解析）
- [ ] ADD 条目同时存在于 common 和 full
- [ ] MOVE 条目只存在于 full，不在 common
- [ ] DELETE 条目在 common 和 full 中都不存在

## 历史维护记录

| 轮次 | 日期 | Common 变化 | Full 变化 | 主要操作 |
|------|------|-------------|-----------|----------|
| 第4轮 | 2026-06-15/18 | 4361→4245 (-116) | 7275→7037 (-238) | DELETE 251虚构, MOVE 129, ADD 13 |
| 第5轮 | 2026-06-25 | 4258→4236 (-22) | 7050→6913 (-137) | DELETE 144, MOVE 6, ADD 7 |
| 第6轮 | 2026-06-25 | 4301→4319 (+18) | 6985→7021 (+36) | DELETE 18, MOVE 35, ADD 15 |

详细记录见项目 docs/ 目录。
