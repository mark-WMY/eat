const app = getApp()

const COMMON_CUISINE_IDS = new Set([
  'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
  'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
  'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
  'cuisine_guizhou'
])

Page({
  data: {
    cuisineList: [],
    mealTypeList: [],
    foodTypeList: [],
    dishTypeList: [],
    healthTagsList: [],
    allergensList: [],

    selectedFilters: {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: [],
      healthTags: [],
      allergens: []
    },

    currentResult: null,
    currentResultTags: [],

    filteredCount: 0,
    totalCount: 0,

    lastResultId: null,
    showAllMode: false
  },

  onLoad() {
    this.loadIngredientsData()
  },

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

  initFilterList() {
    const data = this.ingredientsData

    const cuisineList = Object.values(data.categories.cuisine).map(item => ({
      ...item,
      selected: false
    }))

    const mealTypeList = Object.values(data.categories.mealType).map(item => ({
      ...item,
      selected: false
    }))

    const foodTypeList = Object.values(data.categories.foodType).map(item => ({
      ...item,
      selected: false
    }))

    const dishTypeList = data.categories.dishType ? Object.values(data.categories.dishType).map(item => ({
      ...item,
      selected: false
    })) : []

    const healthTagsList = data.categories.healthTags ? Object.values(data.categories.healthTags).map(item => ({
      ...item,
      selected: false
    })) : []

    const allergensList = data.categories.allergens ? Object.values(data.categories.allergens).map(item => ({
      ...item,
      selected: false
    })) : []

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      healthTagsList,
      allergensList,
      totalCount: data.items.length,
      filteredCount: data.items.length
    })

    this.updateFilteredItems()
  },

  onToggleCommon() {
    const showAllMode = !this.data.showAllMode
    this.setData({ showAllMode })
    this.updateFilteredItems()
  },

  onFilterTap(e) {
    const { id, type } = e.currentTarget.dataset
    let {
      cuisineList, mealTypeList, foodTypeList, dishTypeList,
      healthTagsList, allergensList, selectedFilters
    } = this.data

    const listMap = {
      cuisine: cuisineList,
      mealType: mealTypeList,
      foodType: foodTypeList,
      dishType: dishTypeList,
      healthTags: healthTagsList,
      allergens: allergensList
    }

    if (type === 'mealType') {
      mealTypeList.forEach(item => {
        item.selected = item.id === id && !item.selected
      })
      selectedFilters.mealType = mealTypeList.find(i => i.selected)?.id || null
    } else {
      const list = listMap[type]
      if (list) {
        const item = list.find(i => i.id === id)
        if (item) {
          item.selected = !item.selected
          if (item.selected) {
            selectedFilters[type].push(id)
          } else {
            selectedFilters[type] = selectedFilters[type].filter(i => i !== id)
          }
        }
      }
    }

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      healthTagsList,
      allergensList,
      selectedFilters
    })

    this.updateFilteredItems()
  },

  updateFilteredItems() {
    const items = this.ingredientsData.items
    const filters = this.data.selectedFilters
    const showAllMode = this.data.showAllMode

    this.filteredItems = items.filter(item => {
      if (!showAllMode) {
        const hasCommonCuisine = item.categories.some(c => COMMON_CUISINE_IDS.has(c))
        if (!hasCommonCuisine) return false
      }

      if (filters.cuisine.length > 0) {
        const hasCuisine = filters.cuisine.some(c => item.categories.includes(c))
        if (!hasCuisine) return false
      }

      if (filters.mealType) {
        if (!item.categories.includes(filters.mealType)) return false
      }

      if (filters.foodType.length > 0) {
        const hasFoodType = filters.foodType.some(f => item.categories.includes(f))
        if (!hasFoodType) return false
      }

      if (filters.dishType.length > 0) {
        const hasDishType = filters.dishType.some(d => item.categories.includes(d))
        if (!hasDishType) return false
      }

      if (filters.healthTags.length > 0) {
        const hasHealthTag = filters.healthTags.some(h => item.categories.includes(h))
        if (!hasHealthTag) return false
      }

      if (filters.allergens.length > 0) {
        const hasAllergen = filters.allergens.some(a => item.categories.includes(a))
        if (hasAllergen) return false
      }

      return true
    })

    this.setData({
      filteredCount: this.filteredItems.length
    })
  },

  onSelect() {
    if (this.filteredItems.length === 0) {
      this.setData({
        currentResult: { name: '没有符合条件的食材' },
        currentResultTags: []
      })
      return
    }

    let availableItems = this.filteredItems.filter(
      item => item.id !== this.data.lastResultId
    )

    if (availableItems.length === 0) {
      availableItems = this.filteredItems
    }

    const randomIndex = Math.floor(Math.random() * availableItems.length)
    const result = availableItems[randomIndex]
    const tagNames = this.getTagNames(result.categories)

    this.setData({
      currentResult: result,
      currentResultTags: tagNames,
      lastResultId: result.id
    })
  },

  getTagNames(categoryIds) {
    const data = this.ingredientsData
    const names = []

    categoryIds.forEach(id => {
      for (const groupKey in data.categories) {
        const group = data.categories[groupKey]
        for (const key in group) {
          if (group[key].id === id) {
            names.push(group[key].name)
            break
          }
        }
      }
    })

    return names
  },

  onReset() {
    const {
      cuisineList, mealTypeList, foodTypeList, dishTypeList,
      healthTagsList, allergensList
    } = this.data

    cuisineList.forEach(item => item.selected = false)
    mealTypeList.forEach(item => item.selected = false)
    foodTypeList.forEach(item => item.selected = false)
    if (dishTypeList) dishTypeList.forEach(item => item.selected = false)
    if (healthTagsList) healthTagsList.forEach(item => item.selected = false)
    if (allergensList) allergensList.forEach(item => item.selected = false)

    this.setData({
      cuisineList,
      mealTypeList,
      foodTypeList,
      dishTypeList,
      healthTagsList,
      allergensList,
      selectedFilters: {
        cuisine: [],
        mealType: null,
        foodType: [],
        dishType: [],
        healthTags: [],
        allergens: []
      },
      currentResult: null,
      currentResultTags: [],
      lastResultId: null
    })

    this.updateFilteredItems()
  }
})
