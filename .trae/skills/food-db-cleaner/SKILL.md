---
name: "food-db-cleaner"
description: "审查中餐数据库，确保common只保留全国常见食物。Invoke when cleaning food database, removing regional items, or validating food availability."
references:
  - "AGENTS.md (项目全局规则)"
---

# 餐食数据库清理工具

> **规则来源**: `AGENTS.md` 是本项目的全局规则文件，定义了食材数据库的核心规则。本 SKILL 是对 AGENTS.md 中删除/移动规则的细化执行指南。操作前请先阅读 `AGENTS.md`。

审查 `ingredients_common.json` 和 `ingredients_full.json`，确保"常见"条目在全国范围内可轻松购买。

## 核心规则

### DELETE（删除）
- 虚构/不存在食物（AI生成、错别字）
- 非菜品（水果、调味品、品牌名、宴席形式）
- 重复条目（同食物不同名称）

### MOVE（移至 full）
仅限 **1-2省** 的地域性食物：
- 城市/县前缀（如：武汉热干面、长沙糖油粑粑）
- 极其地域性食材（如：撒撇、炸乳扇、饵块）
- 小众外国菜（如：印度咖喱鸡、墨西哥馅饼）

### KEEP（保留）
覆盖 **≥3省** 的食物：
- 全国知名菜品（宫保鸡丁、麻婆豆腐、红烧肉）
- 全国连锁品类（兰州拉面、沙县小吃、螺蛳粉）
- 常见外国菜（寿司、披萨、汉堡、咖喱饭）
- 通用主食/饮品（米饭、面条、豆浆、油条）

### ADD（添加）

添加新条目时必须遵守以下规则：

1. **同步添加**：`common` 中添加的条目必须同步添加到 `full` 中，确保数据完整。
2. **真实存在**：所有条目（common 和 full）必须是真实存在的菜品，禁止添加虚构或 AI 生成的菜品。
3. **≥3省覆盖**：`common` 的条目必须是在国内超过三个省份都真实存在/可轻松购买的菜品。

## 谐音属性

为常见歧义名称添加 `searchAliases`：
```json
"attributes": {
  "searchAliases": ["抄手", "云吞", "扁食"]
}
```

常见谐音：
- 馄饨 ↔ 抄手 ↔ 云吞 ↔ 扁食
- 煎饼果子 ↔ 煎饼馃子
- 胡辣汤 ↔ 糊辣汤
- 锅包肉 ↔ 锅爆肉
- 味噌 ↔ 味增

## 文件结构

```
js/
  ingredients_common.json  # 常见食物（2500+条）
  ingredients_full.json    # 全量食物（5600+条）
```

## 执行流程

1. 提取 common 条目列表
2. 按规则分类：DELETE / MOVE / KEEP
3. 执行删除和移动
4. 添加谐音属性
5. 验证 JSON 有效性
6. 清理临时脚本文件