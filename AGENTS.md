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

### 数据库维护完整流程

当用户提出"对食材数据进行系统性更新/维护"、"添加/清理食材条目"等5项任务（ADD、SYNC、REVIEW、CONDITIONAL DELETE、DELETE FICTIONAL）时，必须加载 `.trae/skills/food-db-maintenance/SKILL.md` 并按标准流程执行。

#### 五项任务定义

| 任务 | 操作 | 范围 | 依据 |
|------|------|------|------|
| 任务1 ADD | 添加常见菜品到 common | common + full | 真实存在 + ≥3省覆盖 |
| 任务2 SYNC | 同步 common 到 full | common ⊆ full | common 是 full 的子集 |
| 任务3 REVIEW | 审查 common，移除不常见（MOVE到full） | common → full | 仅保留全国常见（≥3省） |
| 任务4 CONDITIONAL DELETE | 仅虚构条目从full删除，真实条目只从common移 | full + common | 现实中不存在才删 |
| 任务5 DELETE FICTIONAL | 删除 full 中虚构条目 | full (+ common 同步) | 现实中不存在 |

#### DELETE 判定规则

从 full 删除的条目（必须同时满足）:
1. 现实中确实不存在（AI生成、虚构、错别字）
2. 或不是具体菜品（品类标签、水状态、通用描述）

以下情况不删除，仅从 common 移至 full:
- 真实存在但地域性强（MOVE）
- 真实存在但为特定品牌（MOVE）
- 真实存在但为场景形式（MOVE）

#### MOVE 判定规则

从 common 移至 full 的条目（符合任一即可）:
1. 仅 1-2 省覆盖的地域性菜品
2. 前缀/后缀冗余（基础菜名已存在）
3. 具体品牌名（非通用品类）
4. 场景形式（宴席、套餐等）

详见 `food-db-maintenance/SKILL.md`。

## 功能独立性规则（核心架构约束）

> **此规则是系统架构的核心约束，任何代码修改都不得违反。**

### 各功能的数据源与筛选范围

| 功能 | 数据源 | 受常见/全部影响 | 受推荐模式影响 | 受用户筛选影响 | 受历史推荐影响 |
|------|--------|----------------|----------------|----------------|----------------|
| 开始推荐 | `state.filteredItems` → `getRecommendationItems()` | ✅ 是 | ✅ 是 | ✅ 是 | ❌ 否 |
| 大家还喜欢 | `getRecommendationItems()` + 相似度 | ✅ 是 | ✅ 是 | ✅ 是 | ✅ 基于当前条目 |
| 搜索功能 | `state.fullData.items` | ❌ 否 | ❌ 否 | ❌ 仅搜索关键词 | ❌ 否 |
| 食物大全 | `state.fullData.items` | ❌ 否 | ❌ 否 | ❌ 否 | ❌ 否 |
| 统计数字 | `state.filteredItems` / `state.fullData.items` | ❌ 否 | ❌ 否 | ✅ 是（筛选条件+搜索词） | ❌ 否 |

### "开始推荐"功能规则

1. **纯随机推荐**：`handleSelect()` 必须从 `getRecommendationItems()` 返回的候选列表中**纯随机选取**，不得使用 `pickRelatedItem()` 或基于 `state.lastResult` 的相似推荐逻辑。
2. **仅依赖用户手动选择的筛选条件**：推荐候选列表由用户主动选择的筛选条件决定，包括：常见/全部、推荐模式（好吃的/全部/小吃零食甜点饮品）、菜系、时段、食材类型、餐品类型、健康标签、过敏原排除。
3. **完全独立于历史推荐结果**：不得基于上一条推荐条目的属性进行相似推荐，不得避免重复推荐同一条目。

### "大家还喜欢"功能规则

1. **基于当前推荐条目的相似推荐**：`getRelatedItems()` 使用 `getRelatedScore()` 计算与 `state.currentResult` 的相似度，返回相似度最高的条目。
2. **仅此模块使用相似推荐逻辑**：`pickRelatedItem()` 和 `getRelatedScore()` 仅用于"大家还喜欢"模块及其刷新按钮，不得用于"开始推荐"。
3. **遵循推荐模式筛选**：相似推荐的候选列表也经过 `getRecommendationItems()` 过滤，与"开始推荐"使用相同的筛选范围。

### "食物大全"功能规则

1. **始终展示全部条目**：`handleCatalog()` 必须使用 `state.fullData.items`（full.json 完整数据），不得使用 `state.ingredientsData.items`（可能为 common 子集）。
2. **不区分任何状态或属性**：不受常见/全部、推荐模式、用户筛选条件、搜索关键词的任何影响。
3. **按拼音排序**：所有条目按名称的拼音排序展示。

### 搜索功能规则

1. **基于 full.json 检索**：`showSearchDropdown()` 和 `selectFromSearchDropdown()` 必须使用 `state.fullData.items`，不得使用 `state.ingredientsData.items`。
2. **不受常见/全部筛选限制**：搜索结果覆盖系统全部食物数据，无论用户选择"常见"还是"全部"模式。
3. **仅按搜索关键词过滤**：搜索不应用菜系、时段等其他筛选条件，仅匹配菜品名称。

### 数据加载规则

1. **`state.fullData`**：始终持有 full.json 的完整数据，供搜索、食物大全和统计总数使用。
2. **`state.ingredientsData`**：初始为 common.json 数据（快速首屏渲染），后台懒加载后被 full.json 替代。用于筛选器渲染。
3. **`state.filteredItems`**：基于 `state.fullData.items`（或回退到 `state.ingredientsData.items`）+ 搜索关键词 + 用户筛选条件生成。**不包含**常见/全部过滤和推荐模式过滤。
4. **`getRecommendationItems()`**：在 `state.filteredItems` 基础上叠加常见/全部过滤和推荐模式过滤，仅用于"开始推荐"和"大家还喜欢"。

## 推荐范围三段式切换规则

页面头部"有什么好吃的?"标题右侧设有三段式切换按钮，控制"开始推荐"功能的筛选范围。

### 三种推荐模式

| 模式 | 按钮文本 | 标题文本 | 推荐范围 |
|------|----------|----------|----------|
| `food`（默认） | 好吃的 | 有什么好吃的? | 仅食物类，自动剔除酒水、饮品等非食物类项目 |
| `all` | 全部 | 有什么推荐的? | 全部内容类型，包含食物、酒水、饮品等所有类别 |
| `snack` | 小吃零食甜点饮品 | 有什么解馋的? | 仅非主食类，包括小吃、零食、甜点和各类饮品 |

### 分类 ID 定义

- **饮品/酒水类**（`food` 模式剔除）：`food_alcohol`、`food_tea`、`food_coffee`、`food_fruit_tea`、`dish_beverage`
- **小吃/甜点/饮品类**（`snack` 模式仅展示）：`food_snack`、`food_dessert`、`food_alcohol`、`food_tea`、`food_coffee`、`food_fruit_tea`、`dish_snack`、`dish_dessert`、`dish_beverage`

### URL 参数持久化

推荐模式通过 URL 参数 `rec` 持久化：`?rec=food`（默认，省略）、`?rec=all`、`?rec=snack`。

## 引用的规则文件

Agent 在执行相关任务时，必须同时加载以下文件：

| 文件 | 说明 |
|------|------|
| `AGENTS.md`（本文件） | 全局规则中心，条目添加规则、功能独立性规则、推荐范围切换规则 |
| `.trae/skills/food-db-cleaner/SKILL.md` | 条目删除/移动规则及执行流程 |
| `.trae/skills/food-db-maintenance/SKILL.md` | 数据库5项维护完整流程指南（ADD/SYNC/MOVE/DELETE） |
| `.trae/skills/recommend-mode/SKILL.md` | 推荐范围三段式切换功能说明 |
| `.trae/skills/feature-independence/SKILL.md` | 功能独立性规则说明（开始推荐/大家还喜欢/搜索/食物大全的行为约束） |
| `.workbuddy/memory/2026-06-15.md` | 历史操作记录（早期清理任务），供决策参考 |
| `.workbuddy/memory/2026-06-18.md` | 历史操作记录（批量添加任务），供决策参考 |
