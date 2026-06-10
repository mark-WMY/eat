App({
  onLaunch() {
    // 加载食材数据
    this.loadIngredientsData();
  },

  ingredientsData: null,

  loadIngredientsData() {
    wx.request({
      url: 'data/ingredients.json',
      success: (res) => {
        if (res.data) {
          this.ingredientsData = res.data;
        }
      },
      fail: () => {
        console.error('加载食材数据失败');
      }
    });
  }
})
