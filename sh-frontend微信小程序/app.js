// app.js
App({
  onLaunch() {

   if(wx.getStorageSync('userInfo')){
      this.globalData.userInfo = wx.getStorageSync('userInfo')
   }
  },
  getUserInfo() {

  },
  globalData: {
      uid:1,
      userInfo: null,
      loginOK:false,
      token:'',
      url: 'http://116.63.12.26/' ,//这个地方写你的url接口地址
      openid: null,

    //购物车列表
    cartList: [],

    //订单列表
    orderList: null
  }
})


//新品推荐
//社区交流
//二手回收商

