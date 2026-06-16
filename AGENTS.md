# 项目全局规则文件

> 本文件是项目的**全局规则中心**，所有 Agent 在执行任务前必须加载本文件及以下引用的所有规则文件。

## 食材数据库规则

### 条目添加规则

往 `js/ingredients_common.json` 和 `js/ingredients_full.json` 添加新条目时，必须遵守以下规则：

1. **同步添加**：`common` 中添加的条目必须同步添加到 `full` 中，`common` 是 `full` 的子集。
2. **真实存在**：所有条目（common 和 full）必须是真实存在的菜品，禁止添加虚构、AI 生成或编造的菜品。
3. **≥3省覆盖**：`common` 的条目必须是在国内超过三个省份都能找到/可轻松购买的全国性菜品，地域性过强的菜品只应放入 `full`。

### 条目删除/移动规则

参见 `.trae/skills/food-db-cleaner/SKILL.md`。

## 引用的规则文件

Agent 在执行相关任务时，必须同时加载以下文件：

| 文件 | 说明 |
|------|------|
| `AGENTS.md`（本文件） | 全局规则中心，条目添加规则 |
| `.trae/skills/food-db-cleaner/SKILL.md` | 条目删除/移动规则及执行流程 |
| `.workbuddy/memory/2026-06-15.md` | 历史操作记录，供决策参考 |
