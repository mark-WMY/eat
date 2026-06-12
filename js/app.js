(function() {
  'use strict';

  const COMMON_CUISINE_IDS = new Set([
    'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
    'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
    'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
    'cuisine_guizhou'
  ]);

  const CUISINE_RENDER_ORDER = [
    'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
    'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
    'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
    'cuisine_guizhou', 'cuisine_other',
    'cuisine_japanese', 'cuisine_korean', 'cuisine_thai', 'cuisine_vietnamese',
    'cuisine_indian', 'cuisine_singapore', 'cuisine_malaysian',
    'cuisine_italian', 'cuisine_french', 'cuisine_spanish', 'cuisine_german',
    'cuisine_british', 'cuisine_greek', 'cuisine_american', 'cuisine_mexican',
    'cuisine_brazilian', 'cuisine_western', 'cuisine_middle_eastern', 'cuisine_african'
  ];

  const FOREIGN_CUISINE_IDS = new Set([
    'cuisine_japanese', 'cuisine_korean', 'cuisine_thai', 'cuisine_vietnamese',
    'cuisine_indian', 'cuisine_singapore', 'cuisine_malaysian',
    'cuisine_italian', 'cuisine_french', 'cuisine_spanish', 'cuisine_german',
    'cuisine_british', 'cuisine_greek', 'cuisine_american', 'cuisine_mexican',
    'cuisine_brazilian', 'cuisine_western', 'cuisine_middle_eastern', 'cuisine_african'
  ]);

  const state = {
    ingredientsData: null,
    selectedFilters: {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: [],
      healthTags: [],
      allergens: []
    },
    showAllMode: false,
    currentResult: null,
    lastResult: null,
    filteredItems: []
  };

  const elements = {};

  let searchTimeout;
  let currentSearchKeyword = '';

  async function init() {
    await loadIngredients();
    cacheElements();
    bindEvents();
    renderFilters();
    updateFilteredItems();
    updateStats();
  }

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

  function cacheElements() {
    elements.filterCuisine = document.getElementById('filter-cuisine');
    elements.filterMealType = document.getElementById('filter-meal-type');
    elements.filterFoodType = document.getElementById('filter-food-type');
    elements.filterDishType = document.getElementById('filter-dish-type');
    elements.filterHealthTags = document.getElementById('filter-health-tags');
    elements.filterAllergens = document.getElementById('filter-allergens');
    elements.toggleCommon = document.getElementById('toggle-common');
    elements.resultSection = document.getElementById('result-section');
    elements.resultName = document.getElementById('result-name');
    elements.resultTags = document.getElementById('result-tags');
    elements.btnSelect = document.getElementById('btn-select');
    elements.btnReset = document.getElementById('btn-reset');
    elements.btnCatalog = document.getElementById('btn-catalog');
    elements.searchInput = document.getElementById('search-input');
    elements.searchBtn = document.getElementById('search-btn');
    elements.searchClear = document.getElementById('search-clear');
    elements.catalogModal = document.getElementById('catalog-modal');
    elements.catalogClose = document.getElementById('catalog-close');
    elements.catalogList = document.getElementById('catalog-list');
    elements.statsCount = document.getElementById('stats-count');
    elements.statsTotal = document.getElementById('stats-total');
  }

  function bindEvents() {
    elements.btnSelect.addEventListener('click', handleSelect);
    elements.btnReset.addEventListener('click', handleReset);
    elements.btnCatalog.addEventListener('click', handleCatalog);
    elements.catalogClose.addEventListener('click', closeCatalog);
    elements.catalogModal.addEventListener('click', (e) => {
      if (e.target === elements.catalogModal) {
        closeCatalog();
      }
    });

    elements.toggleCommon.addEventListener('click', handleToggleCommon);

    elements.searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      const keyword = e.target.value.trim();
      elements.searchClear.style.display = keyword ? 'flex' : 'none';
      searchTimeout = setTimeout(() => {
        currentSearchKeyword = keyword.toLowerCase();
        updateFilteredItems();
        updateStats();
      }, 300);
    });

    if (elements.searchBtn) {
      elements.searchBtn.addEventListener('click', () => {
        handleSelect();
      });
    }

    elements.searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        handleSelect();
      }
    });

    elements.searchClear.addEventListener('click', () => {
      elements.searchInput.value = '';
      elements.searchClear.style.display = 'none';
      currentSearchKeyword = '';
      updateFilteredItems();
      updateStats();
      elements.searchInput.focus();
    });
  }

  function handleToggleCommon() {
    state.showAllMode = !state.showAllMode;
    elements.toggleCommon.classList.toggle('active');
    updateFilteredItems();
    updateStats();
  }

  function renderFilters() {
    const data = state.ingredientsData;
    if (!data) return;

    renderCuisineFilter();
    renderFilterGroup(elements.filterMealType, Object.values(data.categories.mealType), 'mealType', true);
    elements.filterMealType.classList.add('single-select');
    renderFilterGroup(elements.filterFoodType, Object.values(data.categories.foodType), 'foodType');
    renderFilterGroup(elements.filterDishType, Object.values(data.categories.dishType), 'dishType');
    renderFilterGroup(elements.filterHealthTags, Object.values(data.categories.healthTags), 'healthTags');
    renderFilterGroup(elements.filterAllergens, Object.values(data.categories.allergens), 'allergens');
  }

  function renderCuisineFilter() {
    const data = state.ingredientsData;
    if (!data || !data.categories.cuisine) return;

    const container = elements.filterCuisine;
    const cuisineMap = data.categories.cuisine;
    const sortedItems = CUISINE_RENDER_ORDER
      .map(id => Object.values(cuisineMap).find(c => c.id === id))
      .filter(Boolean);

    const hiddenIds = new Set();
    sortedItems.forEach((item, index) => {
      if (FOREIGN_CUISINE_IDS.has(item.id)) {
        hiddenIds.add(item.id);
      }
    });

    container.innerHTML = sortedItems.map(item => `
      <span class="filter-tag${hiddenIds.has(item.id) ? ' hidden-tag' : ''}" data-id="${item.id}" data-type="cuisine">
        ${item.name}
      </span>
    `).join('') + '<button class="show-all-btn">查看全部</button>';

    container.querySelectorAll('.filter-tag').forEach(tag => {
      tag.addEventListener('click', () => handleFilterClick(tag, 'cuisine', false));
    });

    const showAllBtn = container.querySelector('.show-all-btn');
    const hiddenTags = container.querySelectorAll('.filter-tag.hidden-tag');
    if (hiddenTags.length === 0) {
      showAllBtn.style.display = 'none';
    }
    showAllBtn.addEventListener('click', () => {
      hiddenTags.forEach(t => t.classList.add('show'));
      showAllBtn.style.display = 'none';
    });
  }

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

  function handleFilterClick(tag, type, singleSelect) {
    const id = tag.dataset.id;
    const container = tag.parentElement;

    if (singleSelect) {
      if (tag.classList.contains('active')) {
        tag.classList.remove('active');
        state.selectedFilters[type] = null;
      } else {
        container.querySelectorAll('.filter-tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');
        state.selectedFilters[type] = id;
      }
    } else {
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

  function updateFilteredItems() {
    const items = state.ingredientsData.items;
    const filters = state.selectedFilters;

    state.filteredItems = items.filter(item => {
      if (currentSearchKeyword) {
        if (!item.name.toLowerCase().includes(currentSearchKeyword)) {
          return false;
        }
      }

      if (!state.showAllMode) {
        const hasCommonCuisine = item.categories.some(c => COMMON_CUISINE_IDS.has(c));
        if (!hasCommonCuisine) return false;
      }

      if (filters.cuisine.length > 0) {
        const hasCuisine = filters.cuisine.some(c => item.categories.includes(c));
        if (!hasCuisine) return false;
      }

      if (filters.mealType) {
        if (!item.categories.includes(filters.mealType)) return false;
      }

      if (filters.foodType.length > 0) {
        const hasFoodType = filters.foodType.some(f => item.categories.includes(f));
        if (!hasFoodType) return false;
      }

      if (filters.dishType.length > 0) {
        const hasDishType = filters.dishType.some(d => item.categories.includes(d));
        if (!hasDishType) return false;
      }

      if (filters.healthTags.length > 0) {
        const hasHealthTag = filters.healthTags.some(h => item.categories.includes(h));
        if (!hasHealthTag) return false;
      }

      if (filters.allergens.length > 0) {
        const hasAllergen = filters.allergens.some(a => item.categories.includes(a));
        if (hasAllergen) return false;
      }

      return true;
    });
  }

  function handleSelect() {
    if (state.filteredItems.length === 0) {
      elements.resultName.textContent = '没有符合条件的食材';
      elements.resultTags.innerHTML = '';
      return;
    }

    // Show result card immediately so rolling animation is visible on first click
    const placeholder = elements.resultSection.querySelector('.result-placeholder');
    const resultCard = document.getElementById('result-card');
    if (placeholder) placeholder.style.display = 'none';
    if (resultCard) resultCard.style.display = 'block';
    elements.resultSection.classList.add('show-result');

    elements.btnSelect.disabled = true;
    elements.btnSelect.textContent = '选择中...';

    let count = 0;
    const maxCount = 20;
    const interval = setInterval(() => {
      const randomItem = state.filteredItems[
        Math.floor(Math.random() * state.filteredItems.length)
      ];
      elements.resultName.textContent = randomItem.name;
      elements.resultName.classList.add('rolling');

      // Update tags during rolling too
      const tagNames = getTagNames(randomItem.categories);
      elements.resultTags.innerHTML = tagNames
        .map(name => `<span class="result-tag">${name}</span>`)
        .join('');

      count++;

      if (count >= maxCount) {
        clearInterval(interval);
        elements.resultName.classList.remove('rolling');

        let availableItems = state.filteredItems.filter(
          item => item.id !== state.lastResult?.id
        );

        if (availableItems.length === 0) {
          availableItems = state.filteredItems;
        }

        const randomIndex = Math.floor(Math.random() * availableItems.length);
        state.currentResult = availableItems[randomIndex];
        state.lastResult = state.currentResult;

        renderResult();
        elements.btnSelect.disabled = false;
        elements.btnSelect.textContent = '开始推荐';
      }
    }, 100);
  }

  function renderResult() {
    const item = state.currentResult;
    if (!item) return;

    const placeholder = elements.resultSection.querySelector('.result-placeholder');
    const resultCard = document.getElementById('result-card');

    if (placeholder) {
      placeholder.style.display = 'none';
    }
    if (resultCard) {
      resultCard.style.display = 'block';
    }

    elements.resultName.textContent = item.name;

    const tagNames = getTagNames(item.categories);
    elements.resultTags.innerHTML = tagNames
      .map(name => `<span class="result-tag">${name}</span>`)
      .join('');

    elements.resultSection.classList.add('show-result');
  }

  function getTagNames(categoryIds) {
    const data = state.ingredientsData;
    const names = [];

    categoryIds.forEach(id => {
      for (const groupKey in data.categories) {
        const group = data.categories[groupKey];
        for (const key in group) {
          if (group[key].id === id) {
            names.push(group[key].name);
            break;
          }
        }
      }
    });

    return names;
  }

  function handleReset() {
    state.selectedFilters = {
      cuisine: [],
      mealType: null,
      foodType: [],
      dishType: [],
      healthTags: [],
      allergens: []
    };
    state.currentResult = null;
    state.lastResult = null;
    currentSearchKeyword = '';

    document.querySelectorAll('.filter-tag').forEach(tag => {
      tag.classList.remove('active');
    });

    elements.searchInput.value = '';
    elements.searchClear.style.display = 'none';

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

    updateFilteredItems();
    updateStats();
  }

  function updateStats() {
    const total = state.ingredientsData?.items?.length || 0;
    const filtered = state.filteredItems.length;

    elements.statsCount.textContent = filtered;
    elements.statsTotal.textContent = `${total} 种食材`;
  }

  function handleCatalog() {
    if (!state.ingredientsData) return;

    const sortedItems = [...state.ingredientsData.items].sort((a, b) => {
      return a.name.localeCompare(b.name, 'zh-CN');
    });

    elements.catalogList.innerHTML = sortedItems.map(item => `
      <div class="catalog-item" data-name="${item.name}">
        ${item.name}
      </div>
    `).join('');

    elements.catalogModal.classList.add('show');
  }

  function closeCatalog() {
    elements.catalogModal.classList.remove('show');
  }

  document.addEventListener('DOMContentLoaded', () => {
    cacheElements();
    init();
  });

})();
