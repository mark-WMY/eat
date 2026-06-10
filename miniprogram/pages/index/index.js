const app = getApp()

Page({
  data: {
    // 分类列表
    cuisineList: [],
    mealTypeList: [],
    foodTypeList: [],
    dishTypeList: [],

    // 选中状态
    selectedFilters: {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: []
    },

    // 当前结果
    currentResult: null,
    currentResultTags: [],

    // 统计数据
    filteredCount: 0,
    totalCount: 0,

    // 上一次选择
    lastResultId: null
  },

  onLoad() {
    this.loadIngredientsData()
  },

  // 加载食材数据
  loadIngredientsData() {
    wx.request({
      url: 'data/ingredients.json',
      success: (res) => {
        if (res.data) {
          this.ingredientsData = res.data
          this.initFilterList()
        }
      },
      fail: () => {
        console.error('加载食材数据失败')
      }
    })
  },

  // 初始化筛选列表
  initFilterList() {
    const data = this.ingredientsData

    // 转换菜系列表
    const cuisineList = Object.values(data.categories.cuisine).map(item => ({
      ...item,
      selected: false
    }))

    // 转换用餐时段列表
    const mealTypeList = Object.values(data.categories.mealType).map(item => ({
      ...item,
      selected: false
    }))

    // 转换食材类型列表
    const foodTypeList = Object.values(data.categories.foodType).map(item => ({
      ...item,
      selected: false
    }))

    // 转换餐品类型列表
    const dishTypeList = data.categories.dishType ? Object.values(data.categories.dishType).map(item => ({
      ...item,
      selected: false
    })) : []

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      totalCount: data.items.length,
      filteredCount: data.items.length
    })

    this.updateFilteredItems()
  },

  // 处理筛选点击
  onFilterTap(e) {
    const { id, type } = e.currentTarget.dataset
    let { cuisineList, mealTypeList, foodTypeList, dishTypeList, selectedFilters } = this.data

    if (type === 'cuisine') {
      // 多选模式
      const item = cuisineList.find(i => i.id === id)
      if (item) {
        item.selected = !item.selected
        if (item.selected) {
          selectedFilters.cuisine.push(id)
        } else {
          selectedFilters.cuisine = selectedFilters.cuisine.filter(i => i !== id)
        }
      }
    } else if (type === 'mealType') {
      // 单选模式
      mealTypeList.forEach(item => {
        item.selected = item.id === id && !item.selected
      })
      selectedFilters.mealType = mealTypeList.find(i => i.selected)?.id || null
    } else if (type === 'foodType') {
      // 多选模式
      const item = foodTypeList.find(i => i.id === id)
      if (item) {
        item.selected = !item.selected
        if (item.selected) {
          selectedFilters.foodType.push(id)
        } else {
          selectedFilters.foodType = selectedFilters.foodType.filter(i => i !== id)
        }
      }
    } else if (type === 'dishType') {
      // 多选模式
      const item = dishTypeList.find(i => i.id === id)
      if (item) {
        item.selected = !item.selected
        if (item.selected) {
          selectedFilters.dishType.push(id)
        } else {
          selectedFilters.dishType = selectedFilters.dishType.filter(i => i !== id)
        }
      }
    }

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      selectedFilters
    })

    this.updateFilteredItems()
  },

  // 更新筛选后的食材列表
  updateFilteredItems() {
    const items = this.ingredientsData.items
    const filters = this.data.selectedFilters

    this.filteredItems = items.filter(item => {
      // 菜系筛选（多选，任一匹配即可）
      if (filters.cuisine.length > 0) {
        const hasCuisine = filters.cuisine.some(c => item.categories.includes(c))
        if (!hasCuisine) return false
      }

      // 用餐时段筛选（单选）
      if (filters.mealType) {
        if (!item.categories.includes(filters.mealType)) return false
      }

      // 食材类型筛选（多选，任一匹配即可）
      if (filters.foodType.length > 0) {
        const hasFoodType = filters.foodType.some(f => item.categories.includes(f))
        if (!hasFoodType) return false
      }

      // 餐品类型筛选（多选，任一匹配即可）
      if (filters.dishType.length > 0) {
        const hasDishType = filters.dishType.some(d => item.categories.includes(d))
        if (!hasDishType) return false
      }

      return true
    })

    this.setData({
      filteredCount: this.filteredItems.length
    })
  },

  // 处理选择
  onSelect() {
    if (this.filteredItems.length === 0) {
      this.setData({
        currentResult: { name: '没有符合条件的食材' },
        currentResultTags: []
      })
      return
    }

    // 随机选择，避免连续重复
    let availableItems = this.filteredItems.filter(
      item => item.id !== this.data.lastResultId
    )

    if (availableItems.length === 0) {
      availableItems = this.filteredItems
    }

    const randomIndex = Math.floor(Math.random() * availableItems.length)
    const result = availableItems[randomIndex]

    // 获取标签名称
    const tagNames = this.getTagNames(result.categories)

    this.setData({
      currentResult: result,
      currentResultTags: tagNames,
      lastResultId: result.id
    })
  },

  // 获取标签名称
  getTagNames(categoryIds) {
    const data = this.ingredientsData
    const names = []

    categoryIds.forEach(id => {
      // 查找菜系
      for (const key in data.categories.cuisine) {
        if (data.categories.cuisine[key].id === id) {
          names.push(data.categories.cuisine[key].name)
          break
        }
      }
      // 查找用餐时段
      for (const key in data.categories.mealType) {
        if (data.categories.mealType[key].id === id) {
          names.push(data.categories.mealType[key].name)
          break
        }
      }
      // 查找食材类型
      for (const key in data.categories.foodType) {
        if (data.categories.foodType[key].id === id) {
          names.push(data.categories.foodType[key].name)
          break
        }
      }
      // 查找餐品类型
      if (data.categories.dishType) {
        for (const key in data.categories.dishType) {
          if (data.categories.dishType[key].id === id) {
            names.push(data.categories.dishType[key].name)
            break
          }
        }
      }
    })

    return names
  },

  // 处理重置
  onReset() {
    const { cuisineList, mealTypeList, foodTypeList, dishTypeList } = this.data

    cuisineList.forEach(item => item.selected = false)
    mealTypeList.forEach(item => item.selected = false)
    foodTypeList.forEach(item => item.selected = false)
    if (dishTypeList) {
      dishTypeList.forEach(item => item.selected = false)
    }

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      selectedFilters: {
        cuisine: [],
        mealType: null,
        foodType: [],
        dishType: []
      },
      currentResult: null,
      currentResultTags: [],
      lastResultId: null
    })

    this.updateFilteredItems()
  }
})
