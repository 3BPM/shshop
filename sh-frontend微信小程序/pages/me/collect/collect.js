const app = getApp()
Page({

  data: {

  },

  onLoad(options) {
    console.log(app.globalData.openid)
    wx.cloud.database().collection('shop_collects')
    .where({
      _openid:app.globalData.openid
    })
    .orderBy('time','desc')
    .get()
    .then(res=>{
      this.setData({
        goodList:res.data
      })
    })

  },
  toGoodDetail(event){
    console.log(event.currentTarget.dataset)
    let id = event.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/goodDetail/goodDetail?id=' + id ,
    })
  },
  cancelCollect(event){
    console.log(event.currentTarget.dataset)
    wx.cloud.database().collection('shop_collects')
      .doc(event.currentTarget.dataset.id)
      .remove()
      .then(result=>{
        wx.showToast({
          title: '取消成功',
        })
        this.onLoad()
      })
  }
})