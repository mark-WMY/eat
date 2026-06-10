/**
 * 食材随机选择器 - 主逻辑
 */

(function() {
  'use strict';

  // 状态管理
  const state = {
    ingredientsData: null,
    selectedFilters: {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: []
    },
    currentResult: null,
    lastResult: null,
    filteredItems: []
  };

  // DOM 元素
  const elements = {};

  // 初始化
  async function init() {
    await loadIngredients();
    bindEvents();
    renderFilters();
    updateFilteredItems();
    updateStats();
  }

  // 加载食材数据
  async function loadIngredients() {
    try {
      const response = await fetch('js/ingredients.json');
      const data = await response.json();
      state.ingredientsData = data;
    } catch (error) {
      console.error('加载食材数据失败:', error);
      elements.resultName.textContent = '数据加载失败';
    }
  }

  // 缓存DOM元素
  function cacheElements() {
    elements.filterCuisine = document.getElementById('filter-cuisine');
    elements.filterMealType = document.getElementById('filter-meal-type');
    elements.filterFoodType = document.getElementById('filter-food-type');
    elements.filterDishType = document.getElementById('filter-dish-type');
    elements.resultSection = document.getElementById('result-section');
    elements.resultName = document.getElementById('result-name');
    elements.resultTags = document.getElementById('result-tags');
    elements.btnSelect = document.getElementById('btn-select');
    elements.btnReset = document.getElementById('btn-reset');
    elements.statsCount = document.getElementById('stats-count');
    elements.statsTotal = document.getElementById('stats-total');
  }

  // 绑定事件
  function bindEvents() {
    elements.btnSelect.addEventListener('click', handleSelect);
    elements.btnReset.addEventListener('click', handleReset);
  }

  // 渲染筛选器
  function renderFilters() {
    const data = state.ingredientsData;
    if (!data) return;

    // 渲染菜系筛选（多选）
    renderFilterGroup(
      elements.filterCuisine,
      Object.values(data.categories.cuisine),
      'cuisine'
    );

    // 渲染用餐时段（单选）
    elements.filterMealType.classList.add('single-select');
    renderFilterGroup(
      elements.filterMealType,
      Object.values(data.categories.mealType),
      'mealType',
      true
    );

    // 渲染食材类型（多选）
    renderFilterGroup(
      elements.filterFoodType,
      Object.values(data.categories.foodType),
      'foodType'
    );

    // 渲染餐品类型（多选）
    if (elements.filterDishType && data.categories.dishType) {
      renderFilterGroup(
        elements.filterDishType,
        Object.values(data.categories.dishType),
        'dishType'
      );
    }
  }

  // 渲染单个筛选组
  function renderFilterGroup(container, items, type, singleSelect = false) {
    container.innerHTML = items.map(item => `
      <span class="filter-tag" data-id="${item.id}" data-type="${type}">
        ${item.name}
      </span>
    `).join('');

    container.querySelectorAll('.filter-tag').forEach(tag => {
      tag.addEventListener('click', () => handleFilterClick(tag, type, singleSelect));
    });
  }

  // 处理筛选点击
  function handleFilterClick(tag, type, singleSelect) {
    const id = tag.dataset.id;
    const container = tag.parentElement;

    if (singleSelect) {
      // 单选模式
      if (tag.classList.contains('active')) {
        tag.classList.remove('active');
        state.selectedFilters[type] = null;
      } else {
        container.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');
        state.selectedFilters[type] = id;
      }
    } else {
      // 多选模式
      tag.classList.toggle('active');
      const index = state.selectedFilters[type].indexOf(id);
      if (index > -1) {
        state.selectedFilters[type].splice(index, 1);
      } else {
        state.selectedFilters[type].push(id);
      }
    }

    updateFilteredItems();
    updateStats();
  }

  // 更新筛选后的食材列表
  function updateFilteredItems() {
    const items = state.ingredientsData.items;
    const filters = state.selectedFilters;

    state.filteredItems = items.filter(item => {
      // 菜系筛选（多选，任一匹配即可）
      if (filters.cuisine.length > 0) {
        const hasCuisine = filters.cuisine.some(c => item.categories.includes(c));
        if (!hasCuisine) return false;
      }

      // 用餐时段筛选（单选）
      if (filters.mealType) {
        if (!item.categories.includes(filters.mealType)) return false;
      }

      // 食材类型筛选（多选，任一匹配即可）
      if (filters.foodType.length > 0) {
        const hasFoodType = filters.foodType.some(f => item.categories.includes(f));
        if (!hasFoodType) return false;
      }

      // 餐品类型筛选（多选，任一匹配即可）
      if (filters.dishType.length > 0) {
        const hasDishType = filters.dishType.some(d => item.categories.includes(d));
        if (!hasDishType) return false;
      }

      return true;
    });
  }

  // 处理选择按钮
  function handleSelect() {
    if (state.filteredItems.length === 0) {
      elements.resultName.textContent = '没有符合条件的食材';
      elements.resultTags.innerHTML = '';
      return;
    }

    // 随机选择，避免重复
    let availableItems = state.filteredItems.filter(
      item => item.id !== state.lastResult?.id
    );

    if (availableItems.length === 0) {
      availableItems = state.filteredItems;
    }

    const randomIndex = Math.floor(Math.random() * availableItems.length);
    state.currentResult = availableItems[randomIndex];
    state.lastResult = state.currentResult;

    // 渲染结果
    renderResult();
  }

  // 渲染结果
  function renderResult() {
    const item = state.currentResult;
    if (!item) return;

    // 隐藏占位符，显示结果卡片
    const placeholder = elements.resultSection.querySelector('.result-placeholder');
    const resultCard = document.getElementById('result-card');

    if (placeholder) {
      placeholder.style.display = 'none';
    }
    if (resultCard) {
      resultCard.style.display = 'block';
    }

    // 获取食材名称
    elements.resultName.textContent = item.name;

    // 获取分类标签
    const tagNames = getTagNames(item.categories);
    elements.resultTags.innerHTML = tagNames
      .map(name => `<span class="result-tag">${name}</span>`)
      .join('');

    // 添加动画效果
    elements.resultSection.classList.add('show-result');
  }

  // 获取标签名称
  function getTagNames(categoryIds) {
    const data = state.ingredientsData;
    const names = [];

    categoryIds.forEach(id => {
      // 查找菜系
      for (const key in data.categories.cuisine) {
        if (data.categories.cuisine[key].id === id) {
          names.push(data.categories.cuisine[key].name);
          break;
        }
      }
      // 查找用餐时段
      for (const key in data.categories.mealType) {
        if (data.categories.mealType[key].id === id) {
          names.push(data.categories.mealType[key].name);
          break;
        }
      }
      // 查找食材类型
      for (const key in data.categories.foodType) {
        if (data.categories.foodType[key].id === id) {
          names.push(data.categories.foodType[key].name);
          break;
        }
      }
      // 查找餐品类型
      if (data.categories.dishType) {
        for (const key in data.categories.dishType) {
          if (data.categories.dishType[key].id === id) {
            names.push(data.categories.dishType[key].name);
            break;
          }
        }
      }
    });

    return names;
  }

  // 处理重置
  function handleReset() {
    state.selectedFilters = {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: []
    };
    state.currentResult = null;
    state.lastResult = null;

    // 清除所有选中状态
    document.querySelectorAll('.filter-tag').forEach(tag => {
      tag.classList.remove('active');
    });

    // 重置结果区域
    const placeholder = elements.resultSection.querySelector('.result-placeholder');
    const resultCard = document.getElementById('result-card');

    if (placeholder) {
      placeholder.style.display = 'block';
    }
    if (resultCard) {
      resultCard.style.display = 'none';
    }

    elements.resultName.textContent = '';
    elements.resultTags.innerHTML = '';
    elements.resultSection.classList.remove('show-result');

    // 更新统计
    updateFilteredItems();
    updateStats();
  }

  // 更新统计信息
  function updateStats() {
    const total = state.ingredientsData?.items?.length || 0;
    const filtered = state.filteredItems.length;

    elements.statsCount.textContent = filtered;
    elements.statsTotal.textContent = total;
  }

  // 页面加载完成后初始化
  document.addEventListener('DOMContentLoaded', () => {
    cacheElements();
    init();
  });

})();
