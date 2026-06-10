# 食材随机选择器 - 技术架构文档

## 1. 技术选型

### 1.1 网页版
- **框架**：原生 HTML5 + CSS3 + JavaScript（轻量化，无需构建）
- **样式**：自定义CSS，使用CSS变量管理主题
- **动画**：CSS动画 + 原生JS
- **数据结构**：本地JSON文件存储食材数据

### 1.2 小程序版
- **框架**：原生微信小程序
- **数据**：本地数据文件

---

## 2. 项目结构

### 2.1 网页版结构
```
eatWhat/
├── index.html          # 主页面
├── css/
│   └── style.css       # 样式文件
├── js/
│   ├── app.js          # 主逻辑
│   └── ingredients.json # 食材库数据
└── assets/
    └── img/            # 图片资源
```

### 2.2 小程序结构
```
miniprogram/
├── app.js
├── app.json
├── app.wxss
├── pages/
│   └── index/
│       ├── index.js
│       ├── index.wxml
│       └── index.wxss
└── data/
    └── ingredients.json
```

---

## 3. 食材库数据结构

### 3.1 ingredients.json 结构
```json
{
  "categories": {
    "cuisine": {
      "川菜": { "id": "cuisine_chuan", "name": "川菜", "children": [...] },
      "渝菜": { "id": "cuisine_yu", "name": "渝菜", "children": [...] },
      "徽菜": { "id": "cuisine_anhui", "name": "徽菜(皖)", "children": [...] },
      "西餐": { "id": "cuisine_western", "name": "西餐", "children": [...] },
      "新加坡餐": { "id": "cuisine_singapore", "name": "新加坡餐", "children": [...] }
    },
    "mealType": {
      "早餐": { "id": "meal_breakfast" },
      "午餐": { "id": "meal_lunch" },
      "晚餐": { "id": "meal_dinner" },
      "夜宵": { "id": "meal_midnight" }
    },
    "foodType": {
      "荤菜": { "id": "food_meat" },
      "素菜": { "id": "food_vegetarian" },
      "汤": { "id": "food_soup" },
      "粥": { "id": "food_congee" },
      "煲": { "id": "food_stew" },
      "饭": { "id": "food_rice" },
      "米饭": { "id": "food_rice_dish" },
      "面食": { "id": "food_noodles" },
      "杂粮": { "id": "food_wholegrain" }
    }
  },
  "items": [
    {
      "id": "item_00001",
      "name": "回锅肉",
      "categories": ["cuisine_chuan", "meal_lunch", "meal_dinner", "food_meat", "food_rice"]
    }
  ]
}
```

### 3.2 多级分层实现
- 使用树形结构存储分类层级
- 每个节点包含 `id`、`name`、`children`
- 叶子节点可直接关联食材

---

## 4. 核心算法

### 4.1 筛选算法
```
1. 获取所有食材列表
2. 根据选中的菜系筛选（包含任一即保留）
3. 根据选中的用餐时段筛选（包含即保留）
4. 根据选中的食材类型筛选（包含任一即保留）
5. 返回符合条件的食材列表
```

### 4.2 随机选择算法
```
1. 获取符合条件的食材列表
2. 生成随机索引：Math.floor(Math.random() * list.length)
3. 返回对应食材
4. 记录已选食材，避免连续重复
```

---

## 5. 界面设计

### 5.1 网页版布局
```
┌─────────────────────────────────────┐
│            标题区域                   │
├─────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌────────┐ │
│  │  菜系   │ │ 用餐时段│ │食材类型│ │
│  │ 多选标签│ │ 单选标签 │ │ 多选标签│ │
│  └─────────┘ └─────────┘ └────────┘ │
├─────────────────────────────────────┤
│        [ 开始选择 ] 按钮             │
├─────────────────────────────────────┤
│           结果展示区                  │
│         (选中食材卡片)                │
└─────────────────────────────────────┘
```

### 5.2 视觉风格
- **主题色**：温暖的橙色系 (#FF6B35)
- **背景色**：浅米色 (#FFF8F0)
- **强调色**：深棕色 (#4A3728)
- **字体**：Noto Sans SC（中文优化）

---

## 6. 数据存储

### 6.1 本地存储
- 食材数据存储在 JSON 文件中
- 无需后端，纯前端应用
- 可轻松扩展数据规模

### 6.2 状态管理
- 当前筛选条件
- 上一次选择结果
- 用户偏好设置（可选）
