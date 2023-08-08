var app = getApp();
Page({
  data: {
    loginOK: false,
    nickname:'',
    avatar:'',
    id:1,
  },
  onLoad: function (options) {
  },

  onShow() {
    if (app.globalData.loginOK) {
      let a=wx.getStorageSync('avatar')
      let b=wx.getStorageSync('nickname')
      this.setData({
        loginOK: app.globalData.loginOK,
        avatar:a,
        nickname:b
      })
      console.log(this.data.loginOK)
      console.log("哈哈哈我show了，目前精神状态login")
      console.log(a)
      console.log(b)



    }

  },


  toMyOrder() {
    wx.navigateTo({
      url: '/pages/me/myOders/myOrders',
    })
  },


  login() {
    wx.navigateTo({
      url: '/pages/login/login',
    })
  },
  signup() {
    wx.navigateTo({
      url: '/pages/login/login?s=true',
    })
  },
  loinOut() {


    wx.setStorageSync('token', null)
    this.setData({
      loginOK: false
    })


  },

  toxiugai() {
    wx.navigateTo({
      url: '/pages/me/xiugai/xiugai',
    })
  },
 

  toCollect() {
    wx.navigateTo({
      url: '/pages/me/collect/collect',
    })
  },
  toSellerOrders() {
    wx.navigateTo({
      url: '/pages/me/sellerOrders/sellerOrders',
    })
  },
  toMyGoods() {
    wx.navigateTo({
      url: '/pages/me/myGoods/myGoods',
    })
  },
  tomyArticle() {
    wx.navigateTo({
      url: '/pages/me/myArticle/myArticle',
    })
  }

})