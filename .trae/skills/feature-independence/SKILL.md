---
name: "feature-independence"
description: "功能独立性规则。管理'开始推荐'、'大家还喜欢'、'搜索'、'食物大全'四个核心功能的数据源、筛选范围和行为约束，确保各功能互不干扰。Invoke when modifying recommendation logic, search behavior, catalog display, or data source references."
references:
  - "AGENTS.md (项目全局规则 - 功能独立性规则)"
---

# 功能独立性规则

> **规则来源**: `AGENTS.md` 的"功能独立性规则（核心架构约束）"章节是本规则的权威来源。本 SKILL 是对该规则的细化说明和修改指南。

管理"开始推荐"、"大家还喜欢"、"搜索"、"食物大全"四个核心功能的数据源、筛选范围和行为约束。

## 核心原则

**各功能互不干扰**：修改任一功能的行为时，不得影响其他功能的独立性和数据源。

## 数据源架构

```
full.json ──→ state.fullData ──→ state.filteredItems ──→ getRecommendationItems()
                   │                    │                         │
                   ├→ 搜索功能           ├→ 统计数字               ├→ 开始推荐（纯随机）
                   ├→ 食物大全           └→ （不含常见/全部过滤）   └→ 大家还喜欢（相似推荐）
                   └→ 统计总数
```

### 数据源说明

| 变量 | 数据来源 | 用途 |
|------|----------|------|
| `state.fullData` | full.json 完整数据 | 搜索、食物大全、统计总数 |
| `state.ingredientsData` | 初始为 common.json，懒加载后为 full.json | 筛选器渲染 |
| `state.filteredItems` | `state.fullData.items` + 搜索词 + 用户筛选 | 统计数字、推荐候选基础 |
| `getRecommendationItems()` | `state.filteredItems` + 常见/全部 + 推荐模式 | 开始推荐、大家还喜欢 |

## 各功能行为规范

### 1. "开始推荐"功能

**核心约束：纯随机，完全独立于历史推荐结果。**

- **数据流**：`state.filteredItems` → `getRecommendationItems()` → 纯随机选取
- **筛选条件**：常见/全部 + 推荐模式 + 菜系 + 时段 + 食材类型 + 餐品类型 + 健康标签 + 过敏原排除 + 搜索关键词
- **禁止行为**：
  - ❌ 不得使用 `pickRelatedItem()` 进行相似推荐
  - ❌ 不得基于 `state.lastResult` 过滤或排序候选
  - ❌ 不得避免重复推荐同一条目
- **实现位置**：`handleSelect()` 函数

### 2. "大家还喜欢"功能

**核心约束：基于当前推荐条目的相似推荐，且仅此模块使用相似推荐逻辑。**

- **数据流**：`getRecommendationItems()` → `getRelatedScore()` 排序 → 选取相似度最高的条目
- **相似度基准**：`state.currentResult`（当前推荐结果）
- **筛选条件**：与"开始推荐"相同的筛选范围
- **禁止行为**：
  - ❌ 不得影响"开始推荐"的推荐逻辑
  - ❌ 不得使用 `state.lastResult`（应使用 `state.currentResult`）
- **实现位置**：`getRelatedItems()` 函数

### 3. "食物大全"功能

**核心约束：始终展示 full.json 全部条目，不区分任何状态或属性。**

- **数据源**：`state.fullData.items`（必须使用 fullData，不得使用 ingredientsData）
- **排序**：按名称拼音排序
- **禁止行为**：
  - ❌ 不得应用常见/全部过滤
  - ❌ 不得应用推荐模式过滤
  - ❌ 不得应用用户筛选条件
  - ❌ 不得应用搜索关键词过滤
- **实现位置**：`handleCatalog()` 函数

### 4. 搜索功能

**核心约束：基于 full.json 全部条目检索，不受常见/全部筛选限制。**

- **数据源**：`state.fullData.items`（必须使用 fullData，不得使用 ingredientsData）
- **过滤条件**：仅搜索关键词匹配菜品名称
- **禁止行为**：
  - ❌ 不得应用常见/全部过滤
  - ❌ 不得应用推荐模式过滤
  - ❌ 不得应用菜系、时段等其他筛选条件
- **实现位置**：`showSearchDropdown()` 和 `selectFromSearchDropdown()` 函数

## 修改指南

### 修改"开始推荐"逻辑

1. 在 `handleSelect()` 中修改推荐逻辑
2. 确保使用 `getRecommendationItems()` 获取候选列表
3. 确保最终选取为纯随机（`Math.floor(Math.random() * items.length)`）
4. 不得引入 `pickRelatedItem()` 或 `state.lastResult`
5. 设置 `state.currentResult` 供"大家还喜欢"使用

### 修改"大家还喜欢"逻辑

1. 在 `getRelatedItems()` 中修改相似推荐逻辑
2. 确保使用 `getRecommendationItems()` 获取候选列表（与"开始推荐"同范围）
3. 确保基于 `state.currentResult` 计算相似度
4. 不得修改 `handleSelect()` 的推荐逻辑

### 修改搜索逻辑

1. 在 `showSearchDropdown()` 和 `selectFromSearchDropdown()` 中修改
2. 确保使用 `state.fullData?.items || state.ingredientsData.items`
3. 不得引入 `state.showAllMode` 或 `state.recommendMode` 的过滤

### 修改"食物大全"逻辑

1. 在 `handleCatalog()` 中修改
2. 确保使用 `state.fullData?.items || state.ingredientsData.items`
3. 不得引入任何过滤条件

### 修改数据加载逻辑

1. 在 `lazyLoadFullData()` 中确保同时设置 `state.fullData` 和 `state.ingredientsData`
2. 加载完成后始终调用 `updateFilteredItems()` 和 `updateStats()`
3. 如果食物大全已打开，刷新目录内容

## 常见错误与预防

| 错误 | 后果 | 预防 |
|------|------|------|
| 在 `handleSelect()` 中使用 `pickRelatedItem()` | 推荐结果受历史影响 | 使用纯随机选取 |
| 在 `updateFilteredItems()` 中应用常见/全部过滤 | 搜索和统计受影响 | 将过滤移至 `getRecommendationItems()` |
| 在搜索中使用 `state.ingredientsData.items` | 搜索范围可能为 common 子集 | 使用 `state.fullData?.items` |
| 在食物大全中使用 `state.ingredientsData.items` | 目录可能为 common 子集 | 使用 `state.fullData?.items` |
| `lazyLoadFullData()` 仅在 `showAllMode` 时更新 | 全部模式下数据不刷新 | 始终更新 |
