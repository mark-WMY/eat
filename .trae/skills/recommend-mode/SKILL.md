---
name: "recommend-mode"
description: "推荐范围三段式切换功能。管理'好吃的'、'全部'、'小吃零食甜点饮品'三种推荐模式的筛选逻辑、标题切换和 tooltip 说明。Invoke when modifying recommendation range, toggle button behavior, or category filtering rules."
references:
  - "AGENTS.md (项目全局规则 - 推荐范围三段式切换规则)"
  - ".trae/skills/feature-independence/SKILL.md (功能独立性规则)"
---

# 推荐范围三段式切换

> **规则来源**: `AGENTS.md` 的"推荐范围三段式切换规则"章节是本规则的权威来源。本 SKILL 是对该规则的细化说明。
>
> **关联规则**: 推荐模式的过滤逻辑在 `getRecommendationItems()` 中实现，该函数同时应用常见/全部过滤。详见 `.trae/skills/feature-independence/SKILL.md` 中的数据源架构。

管理页面头部"有什么好吃的?"标题右侧的三段式切换按钮，控制"开始推荐"功能的筛选范围。

## 三种推荐模式

### 1. `food` 模式（默认）

- **按钮文本**：好吃的
- **标题文本**：有什么好吃的?
- **推荐范围**：仅食物类条目，自动剔除酒水、饮品等非食物类项目
- **过滤逻辑**：排除包含以下任一分类 ID 的条目
  - `food_alcohol`（酒水）
  - `food_tea`（茶水）
  - `food_coffee`（咖啡）
  - `food_fruit_tea`（果茶）
  - `dish_beverage`（饮品）

### 2. `all` 模式

- **按钮文本**：全部
- **标题文本**：有什么推荐的?
- **推荐范围**：全部内容类型，包含食物、酒水、饮品等所有常见类别
- **过滤逻辑**：无推荐模式额外过滤（但仍应用常见/全部过滤）

### 3. `snack` 模式

- **按钮文本**：小吃零食甜点饮品
- **标题文本**：有什么解馋的?
- **推荐范围**：仅非主食类内容，包括小吃、零食、甜点和各类饮品
- **过滤逻辑**：仅保留包含以下任一分类 ID 的条目
  - `food_snack`（小吃）
  - `food_dessert`（甜点）
  - `food_alcohol`（酒水）
  - `food_tea`（茶水）
  - `food_coffee`（咖啡）
  - `food_fruit_tea`（果茶）
  - `dish_snack`（小吃）
  - `dish_dessert`（甜点）
  - `dish_beverage`（饮品）

## 影响范围

| 功能 | 是否受推荐模式影响 | 说明 |
|------|-------------------|------|
| 开始推荐 | ✅ 是 | 推荐结果仅从当前模式筛选后的条目中选取 |
| 大家还喜欢 | ✅ 是 | 关联推荐也遵循当前推荐模式 |
| 搜索功能 | ❌ 否 | 搜索始终在全部条目中搜索 |
| 食物大全 | ❌ 否 | 始终显示所有条目，不区分任何状态或属性 |
| 统计数字 | ❌ 否 | 反映搜索+筛选条件的结果，不受推荐模式影响 |
| 重置条件 | ❌ 否 | 重置不会改变推荐模式 |

## 技术实现

### 核心函数

- `getRecommendationItems()`：在 `state.filteredItems` 基础上先应用常见/全部过滤，再根据 `state.recommendMode` 过滤，返回推荐候选列表。仅用于"开始推荐"和"大家还喜欢"。
- `handleRecommendModeChange(mode)`：处理模式切换，更新按钮状态、标题、tooltip，并自动重新推荐
- `applyRecommendModeUI()`：同步推荐模式相关的 UI 状态（按钮选中、标题文本、tooltip 内容）
- `updateRecommendTitle(mode)`：带过渡动画的标题切换
- `updateRecommendTooltip(mode)`：更新 tooltip 内容，解释当前模式和其他模式

### URL 参数持久化

推荐模式通过 URL 参数 `rec` 持久化：

- `?rec=food` 或无参数：好吃的模式（默认）
- `?rec=all`：全部模式
- `?rec=snack`：小吃零食甜点饮品模式

### 配置对象

`RECOMMEND_MODES` 常量定义了每种模式的标题、标签、tooltip 说明和其他模式说明文本。修改文案时只需更新此对象。

## 修改指南

### 添加新的推荐模式

1. 在 `RECOMMEND_MODES` 对象中添加新模式配置
2. 在 `getRecommendationItems()` 函数中添加新模式的过滤逻辑
3. 在 `index.html` 中添加对应的按钮元素
4. 更新 `AGENTS.md` 中的模式表格

### 修改分类过滤规则

1. 更新 `BEVERAGE_CATEGORY_IDS` 或 `SNACK_CATEGORY_IDS` 常量
2. 更新 `AGENTS.md` 中的分类 ID 定义
3. 更新本 SKILL 文件中的分类 ID 列表

### 修改标题或 tooltip 文案

1. 更新 `RECOMMEND_MODES` 常量中对应模式的 `title`、`label`、`tooltip` 或 `tooltipOthers` 字段
2. 更新 `AGENTS.md` 中的模式表格（如标题文本变化）
