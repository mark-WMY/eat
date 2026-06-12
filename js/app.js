(function() {
  'use strict';

  const COMMON_CUISINE_IDS = new Set([
    'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
    'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
    'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
    'cuisine_guizhou', 'cuisine_other', 'cuisine_henan', 'cuisine_shaanxi',
    'cuisine_shanxi', 'cuisine_gansu', 'cuisine_xinjiang', 'cuisine_hubei',
    'cuisine_chongqing', 'cuisine_jilin', 'cuisine_guangxi'
  ]);

  const CUISINE_RENDER_ORDER = [
    'cuisine_chuan', 'cuisine_lu', 'cuisine_yue', 'cuisine_su', 'cuisine_zhe',
    'cuisine_min', 'cuisine_xiang', 'cuisine_anhui', 'cuisine_yu', 'cuisine_beijing',
    'cuisine_shanghai', 'cuisine_dongbei', 'cuisine_northwest', 'cuisine_yunnan',
    'cuisine_guizhou', 'cuisine_henan', 'cuisine_shaanxi', 'cuisine_shanxi',
    'cuisine_gansu', 'cuisine_xinjiang', 'cuisine_hubei', 'cuisine_chongqing',
    'cuisine_jilin', 'cuisine_guangxi', 'cuisine_other',
    'cuisine_japanese', 'cuisine_korean', 'cuisine_thai', 'cuisine_vietnamese',
    'cuisine_indian', 'cuisine_singapore', 'cuisine_malaysian',
    'cuisine_italian', 'cuisine_french', 'cuisine_spanish', 'cuisine_german',
    'cuisine_british', 'cuisine_greek', 'cuisine_american', 'cuisine_mexican',
    'cuisine_brazilian', 'cuisine_western', 'cuisine_middle_eastern', 'cuisine_african'
  ];

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
  let moreRecsItems = [];

  async function init() {
    await loadIngredients();
    cacheElements();
    bindEvents();
    renderFilters();
    const hasURLParams = loadFromURL();
    if (hasURLParams) applyLoadedFilters();
    updateFilteredItems();
    updateStats();
    handleSelect();
  }

  async function loadIngredients() {
    try {
      const response = await fetch('js/ingredients_common.json');
      const data = await response.json();
      state.ingredientsData = data;
      lazyLoadFullData();
    } catch (error) {
      console.error('加载食材数据失败:', error);
      elements.resultName.textContent = '数据加载失败';
    }
  }

  async function lazyLoadFullData() {
    try {
      const response = await fetch('js/ingredients_full.json');
      const fullData = await response.json();
      if (fullData && fullData.items) {
        state.ingredientsData = fullData;
        if (state.showAllMode) {
          updateFilteredItems();
          updateStats();
          if (elements.catalogModal.classList.contains('show')) {
            handleCatalog();
          }
        }
      }
    } catch (error) {
      console.log('全量数据后台加载完成');
    }
  }

  function cacheElements() {
    elements.filterCuisine = document.getElementById('filter-cuisine');
    elements.filterMealType = document.getElementById('filter-meal-type');
    elements.filterFoodType = document.getElementById('filter-food-type');
    elements.filterDishType = document.getElementById('filter-dish-type');
    elements.filterHealthTags = document.getElementById('filter-health-tags');
    elements.filterAllergens = document.getElementById('filter-allergens');
    elements.allergenTooltip = document.getElementById('allergen-tooltip');
    elements.tooltipClose = document.getElementById('tooltip-close');
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
    elements.searchDropdown = document.getElementById('search-dropdown');
    elements.catalogModal = document.getElementById('catalog-modal');
    elements.catalogSearch = document.getElementById('catalog-search');
    elements.catalogClose = document.getElementById('catalog-close');
    elements.catalogList = document.getElementById('catalog-list');
    elements.statsCount = document.getElementById('stats-count');
    elements.statsTotal = document.getElementById('stats-total');
    elements.moreRecBtn = document.getElementById('more-rec-btn');
    elements.moreRecRefresh = document.getElementById('more-rec-refresh');
    elements.moreRecClose = document.getElementById('more-rec-close');
    elements.moreRecPanel = document.getElementById('more-rec-panel');
    elements.moreRecGrid = document.getElementById('more-rec-grid');
    elements.resultSlider = document.getElementById('result-slider');
    elements.resultBlurOverlay = document.getElementById('result-blur-overlay');
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

      // Show dropdown immediately (no debounce for dropdown)
      showSearchDropdown(keyword);

      searchTimeout = setTimeout(() => {
        currentSearchKeyword = keyword.toLowerCase();
        updateFilteredItems();
        updateStats();
        updateURL();
      }, 300);
    });

    elements.searchInput.addEventListener('blur', () => {
      setTimeout(() => {
        elements.searchDropdown.classList.remove('show');
      }, 200);
    });

    elements.searchInput.addEventListener('focus', () => {
      const keyword = elements.searchInput.value.trim();
      if (keyword) {
        showSearchDropdown(keyword);
      }
    });

    elements.searchDropdown.addEventListener('click', (e) => {
      const itemEl = e.target.closest('.search-dropdown-item');
      if (!itemEl) return;
      const name = itemEl.dataset.name;
      selectFromSearchDropdown(name);
    });

    if (elements.searchBtn) {
      elements.searchBtn.addEventListener('click', () => {
        hideSearchDropdown();
        handleSelect();
      });
    }

    elements.searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        hideSearchDropdown();
        handleSelect();
      }
    });

    elements.searchClear.addEventListener('click', () => {
      elements.searchInput.value = '';
      elements.searchClear.style.display = 'none';
      currentSearchKeyword = '';
      elements.searchDropdown.classList.remove('show');
      updateFilteredItems();
      updateStats();
      updateURL();
      elements.searchInput.focus();
    });

    elements.catalogSearch.addEventListener('input', (e) => {
      const keyword = e.target.value.trim().toLowerCase();
      const items = elements.catalogList.querySelectorAll('.catalog-item');
      items.forEach(item => {
        item.style.display = item.dataset.name.toLowerCase().includes(keyword) ? '' : 'none';
      });
    });

    // Tooltip close button
    elements.tooltipClose.addEventListener('click', (e) => {
      e.stopPropagation();
      hideAllergenTooltip();
    });

    // 更多推荐按钮
    elements.moreRecBtn.addEventListener('click', showMoreRecs);
    elements.moreRecRefresh.addEventListener('click', refreshMoreRecs);
    elements.moreRecClose.addEventListener('click', closeMoreRecs);

    // More-rec item click to expand
    elements.moreRecGrid.addEventListener('click', (e) => {
      const item = e.target.closest('.more-rec-item');
      if (item) {
        item.classList.toggle('expanded');
      }
    });
  }

  function handleToggleCommon() {
    state.showAllMode = !state.showAllMode;
    elements.toggleCommon.classList.toggle('active');
    updateFilteredItems();
    updateStats();
    updateURL();
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

    container.innerHTML = sortedItems.map(item => `
      <span class="filter-tag" data-id="${item.id}" data-type="cuisine">
        ${item.name}
      </span>
    `).join('');

    container.querySelectorAll('.filter-tag').forEach(tag => {
      tag.addEventListener('click', () => handleFilterClick(tag, 'cuisine', false));
    });

    addExpandIfNeeded(container);
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

    addExpandIfNeeded(container);
  }

  var truncState = {};

  function getTruncLimit() {
    return window.innerWidth <= 600 ? 44 : 150;
  }

  function applyTruncation(container) {
    const key = container.id || 'unknown';
    const limit = getTruncLimit();
    const tags = Array.from(container.querySelectorAll('.filter-tag'));
    tags.forEach(t => t.style.removeProperty('display'));

    if (container.scrollHeight <= limit) {
      if (truncState[key]) {
        truncState[key].dotBtn.remove();
        truncState[key].labelBtn.remove();
        delete truncState[key];
      }
      return false;
    }

    // Hide tags from the end until height fits (leave room for "...")
    var lastHidden = tags.length;
    for (var i = tags.length - 1; i >= 0; i--) {
      tags[i].style.display = 'none';
      lastHidden = i;
      void container.offsetHeight;
      if (container.scrollHeight <= limit) break;
    }

    // Create "..." dot button (flex item inside .filter-tags)
    var dotBtn = document.createElement('button');
    dotBtn.className = 'filter-expand-btn';
    dotBtn.textContent = '...';

    // Create label button ("查看全部"/"折叠起来")
    var label = container.parentElement.querySelector('.filter-label');
    var labelBtn = document.createElement('button');
    labelBtn.className = 'filter-expand-label-btn';
    labelBtn.textContent = '查看全部';

    function doExpand() {
      var isExpanded = container.classList.toggle('expanded');
      if (isExpanded) {
        tags.forEach(function(t) { t.style.removeProperty('display'); });
        dotBtn.style.display = 'none';
        labelBtn.textContent = '折叠起来';
      } else {
        dotBtn.style.display = '';
        for (var i = tags.length - 1; i >= 0; i--) {
          tags[i].style.display = 'none';
          void container.offsetHeight;
          if (container.scrollHeight <= limit) break;
        }
        labelBtn.textContent = '查看全部';
      }
    }

    dotBtn.addEventListener('click', doExpand);
    labelBtn.addEventListener('click', doExpand);

    container.appendChild(dotBtn);
    if (label) label.appendChild(labelBtn);

    // If "..." itself overflows, hide one more tag
    void container.offsetHeight;
    if (container.scrollHeight > limit && lastHidden > 0) {
      tags[lastHidden - 1].style.display = 'none';
    }

    truncState[key] = { dotBtn: dotBtn, labelBtn: labelBtn, tags: tags, limit: limit };
    return true;
  }

  function addExpandIfNeeded(container) {
    setTimeout(function() { applyTruncation(container); }, 100);
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
    updateURL();
    
    // Show tooltip when allergen filter is first used
    if (type === 'allergens' && state.selectedFilters.allergens.length > 0) {
      showAllergenTooltip();
    }
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

  function getRelatedScore(item, reference) {
    if (!reference) return 1;
    const refCats = new Set(reference.categories || []);
    const itemCats = new Set(item.categories || []);
    let score = 0;
    for (const c of itemCats) {
      if (refCats.has(c)) score++;
    }
    return score;
  }

  function pickRelatedItem(candidates, reference) {
    if (candidates.length === 0) return null;
    if (candidates.length === 1 || !reference) {
      return candidates[Math.floor(Math.random() * candidates.length)];
    }
    const scores = candidates.map(item => ({
      item,
      score: getRelatedScore(item, reference),
    }));
    const maxScore = Math.max(...scores.map(s => s.score));
    const pool = maxScore === 0
      ? candidates
      : scores.filter(s => s.score === maxScore).map(s => s.item);
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function handleSelect() {
    if (state.filteredItems.length === 0) {
      const placeholder = elements.resultSection.querySelector('.result-placeholder');
      const resultCard = document.getElementById('result-card');
      if (placeholder) placeholder.style.display = 'none';
      if (resultCard) resultCard.style.display = 'block';
      elements.resultSection.classList.add('show-result');
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
          item => (item.id || item.name) !== (state.lastResult?.id || state.lastResult?.name)
        );

        if (availableItems.length === 0) {
          availableItems = state.filteredItems;
        }

        state.currentResult = pickRelatedItem(availableItems, state.lastResult);
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
    closeMoreRecs();
  }

  function getRelatedItems(count) {
    const ref = state.currentResult;
    if (!ref || !state.ingredientsData) return [];
    const scored = state.ingredientsData.items
      .filter(item => (item.id || item.name) !== (ref.id || ref.name))
      .map(item => ({
        item,
        score: getRelatedScore(item, ref),
      }))
      .sort((a, b) => b.score - a.score);
    const top = scored.filter(s => s.score > 0);
    const pool = top.length >= count ? top : scored;
    const result = [];
    const used = new Set();
    while (result.length < count && result.length < pool.length) {
      const pick = pool[Math.floor(Math.random() * pool.length)];
      const key = pick.item.id || pick.item.name;
      if (!used.has(key)) {
        used.add(key);
        result.push(pick.item);
      }
    }
    return result;
  }

  function showMoreRecs() {
    if (!state.currentResult) return;
    moreRecsItems = getRelatedItems(4);
    renderMoreRecs();
    elements.moreRecPanel.style.display = 'block';
    elements.resultSlider.classList.add('show-more');
  }

  function refreshMoreRecs() {
    moreRecsItems = getRelatedItems(4);
    renderMoreRecs();
  }

  function closeMoreRecs() {
    elements.resultSlider.classList.remove('show-more');
    elements.moreRecPanel.style.display = 'none';
  }

  function renderMoreRecs() {
    const items = elements.moreRecGrid.querySelectorAll('.more-rec-item');
    items.forEach((el, i) => {
      const item = moreRecsItems[i];
      if (item) {
        el.querySelector('.more-rec-name').textContent = item.name;
        const tagsContainer = el.querySelector('.more-rec-tags');
        if (tagsContainer) {
          const tagNames = getTagNames(item.categories);
          tagsContainer.innerHTML = tagNames
            .map(name => `<span class="result-tag">${name}</span>`)
            .join('');
        }
        el.classList.remove('expanded');
        el.style.display = '';
      } else {
        el.style.display = 'none';
      }
    });
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

  function showSearchDropdown(keyword) {
    const dropdown = elements.searchDropdown;
    if (!keyword) {
      dropdown.classList.remove('show');
      return;
    }
    const kw = keyword.toLowerCase();
    const allItems = state.ingredientsData.items;
    const matches = [];
    for (let i = 0; i < allItems.length && matches.length < 15; i++) {
      if (allItems[i].name.toLowerCase().includes(kw)) {
        matches.push(allItems[i]);
      }
    }
    if (matches.length === 0) {
      dropdown.classList.remove('show');
      return;
    }
    dropdown.innerHTML = matches
      .map(item => `<div class="search-dropdown-item" data-name="${item.name}">${item.name}</div>`)
      .join('');
    dropdown.classList.add('show');
  }

  function hideSearchDropdown() {
    elements.searchDropdown.classList.remove('show');
  }

  function selectFromSearchDropdown(name) {
    hideSearchDropdown();
    const item = state.ingredientsData.items.find(i => i.name === name);
    if (!item) return;

    elements.searchInput.value = name;
    elements.searchClear.style.display = 'flex';
    currentSearchKeyword = name.toLowerCase();
    updateFilteredItems();
    updateStats();
    updateURL();

    // Show selected item in result card
    state.currentResult = item;
    state.lastResult = item;
    renderResult();
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
    hideSearchDropdown();

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
    closeMoreRecs();

    updateFilteredItems();
    updateStats();
    updateURL();
  }

  function updateStats() {
    const total = state.ingredientsData?.items?.length || 0;
    const filtered = state.filteredItems.length;

    elements.statsCount.textContent = filtered;
    elements.statsTotal.textContent = `${total} 种食材`;
  }

  // ========== URL 参数同步 ==========

  function buildURLParams() {
    const params = new URLSearchParams();
    const f = state.selectedFilters;

    if (f.cuisine.length > 0) params.set('cuisine', f.cuisine.join(','));
    if (f.mealType) params.set('meal', f.mealType);
    if (f.foodType.length > 0) params.set('food', f.foodType.join(','));
    if (f.dishType.length > 0) params.set('dish', f.dishType.join(','));
    if (f.healthTags.length > 0) params.set('health', f.healthTags.join(','));
    if (f.allergens.length > 0) params.set('allergen', f.allergens.join(','));
    if (state.showAllMode) params.set('all', '1');
    if (currentSearchKeyword) params.set('q', currentSearchKeyword);

    return params;
  }

  function updateURL() {
    const params = buildURLParams();
    const newURL = params.toString()
      ? `${window.location.pathname}?${params.toString()}`
      : window.location.pathname;
    window.history.replaceState(null, '', newURL);
  }

  function loadFromURL() {
    const params = new URLSearchParams(window.location.search);
    const f = state.selectedFilters;
    let hasParams = false;

    const cuisine = params.get('cuisine');
    if (cuisine) {
      f.cuisine = cuisine.split(',').filter(Boolean);
      hasParams = true;
    }

    const meal = params.get('meal');
    if (meal) {
      f.mealType = meal;
      hasParams = true;
    }

    const food = params.get('food');
    if (food) {
      f.foodType = food.split(',').filter(Boolean);
      hasParams = true;
    }

    const dish = params.get('dish');
    if (dish) {
      f.dishType = dish.split(',').filter(Boolean);
      hasParams = true;
    }

    const health = params.get('health');
    if (health) {
      f.healthTags = health.split(',').filter(Boolean);
      hasParams = true;
    }

    const allergen = params.get('allergen');
    if (allergen) {
      f.allergens = allergen.split(',').filter(Boolean);
      hasParams = true;
    }

    if (params.get('all') === '1') {
      state.showAllMode = true;
      hasParams = true;
    }

    const q = params.get('q');
    if (q) {
      currentSearchKeyword = q.toLowerCase();
      elements.searchInput.value = q;
      elements.searchClear.style.display = 'flex';
      hasParams = true;
    }

    return hasParams;
  }

  function applyLoadedFilters() {
    // Activate filter tags based on state.selectedFilters
    const f = state.selectedFilters;
    document.querySelectorAll('.filter-tag').forEach(tag => {
      const id = tag.dataset.id;
      const type = tag.dataset.type;

      if (type === 'mealType') {
        if (id === f.mealType) tag.classList.add('active');
        else tag.classList.remove('active');
      } else if (f[type] && f[type].includes(id)) {
        tag.classList.add('active');
      }
    });

    // Apply show all mode: active = common mode
    if (state.showAllMode) {
      elements.toggleCommon.classList.remove('active');
    } else {
      elements.toggleCommon.classList.add('active');
    }

    updateFilteredItems();
    updateStats();
    
    // Show tooltip if allergens were loaded from URL
    if (f.allergens.length > 0) {
      showAllergenTooltip();
    }
  }

  function showAllergenTooltip() {
    const tooltip = elements.allergenTooltip;
    if (!tooltip) return;
    
    // Check if we can show tooltip again: 5 minutes (5 * 60 * 1000 = 300000ms)
    const lastShown = localStorage.getItem('allergen_tooltip_last_shown');
    const now = Date.now();
    const cooldown = 5 * 60 * 1000; // 5 minutes
    
    if (lastShown && (now - parseInt(lastShown, 10)) < cooldown) {
      // Still in cooldown, don't show
      return;
    }
    
    tooltip.classList.add('show');
    localStorage.setItem('allergen_tooltip_last_shown', now.toString());
    // Auto-hide after 8 seconds
    setTimeout(() => {
      hideAllergenTooltip();
    }, 8000);
  }

  function hideAllergenTooltip() {
    const tooltip = elements.allergenTooltip;
    if (!tooltip) return;
    tooltip.classList.remove('show');
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
    elements.catalogSearch.value = '';
    const items = elements.catalogList.querySelectorAll('.catalog-item');
    items.forEach(item => item.style.display = '');
  }

  document.addEventListener('DOMContentLoaded', () => {
    cacheElements();
    init();
    initSwipe();
  });

  function initSwipe() {
    const slider = elements.resultSlider;
    let startX = 0;
    let isDragging = false;

    slider.addEventListener('touchstart', (e) => {
      if (elements.moreRecPanel.style.display === 'none') return;
      startX = e.touches[0].clientX;
      isDragging = true;
    }, { passive: true });

    slider.addEventListener('touchend', (e) => {
      if (!isDragging) return;
      isDragging = false;
      const diff = e.changedTouches[0].clientX - startX;
      if (Math.abs(diff) > 50) {
        if (diff > 0 && elements.resultSlider.classList.contains('show-more')) {
          closeMoreRecs();
        } else if (diff < 0 && !elements.resultSlider.classList.contains('show-more')) {
          showMoreRecs();
        }
      }
    }, { passive: true });

    // Mouse drag for desktop
    slider.addEventListener('mousedown', (e) => {
      if (elements.moreRecPanel.style.display === 'none') return;
      startX = e.clientX;
      isDragging = true;
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
    });

    document.addEventListener('mouseup', (e) => {
      if (!isDragging) return;
      isDragging = false;
      const diff = e.clientX - startX;
      if (Math.abs(diff) > 50) {
        if (diff > 0 && elements.resultSlider.classList.contains('show-more')) {
          closeMoreRecs();
        } else if (diff < 0 && !elements.resultSlider.classList.contains('show-more')) {
          showMoreRecs();
        }
      }
    });
  }

})();
