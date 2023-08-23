Page({
  data: {
  },
  onLoad: function (options) {

  },
  onShow(){

  },

  toNewGood(){
    wx.navigateTo({
      url: '/pages/index/newGood/newGood',
    })
  },
  toSP(){
    wx.navigateTo({
      url: '/pages/me/myGoods/myGoods',
    })
  },
  toShequ(){
    wx.navigateTo({
      url: '/pages/commity/shequ',
    })
  },
  toHuishou(){
    wx.navigateTo({
      url: '/pages/index/huishou/huishou',
    })
  },
  toTianbao(){
    wx.navigateTo({
      url: '/pages/index/tianbao/tiaobao',
    })
  }
})