const app = getApp()
Page({
  data: {
    goodList:[]
  },
  onLoad: function (options) {
    console.log("lllllllllllllllllllllllllllllllllllllllllllllllllthisis mygood")

    this.getGoodsList(app.globalData.uid)
  },
  onShow(options) {
  },

  getGoodsList(ownerid) {
    console.log('第一次应该是正常的'+ownerid)
    wx.request({
      url: 'http://116.63.12.26/api/auth/article/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        console.log("获取全部article的调用")
        let goodall = res.data
        var good = [];
        for (var i = 0; i < goodall.length; i++) {
           console.log(ownerid)
          // console.log(goodall[i].spu)
           console.log(goodall[i].owner)
          if (goodall[i].owner == ownerid) {
            console.log("确实")
            good.push(goodall[i]);
          }
        }
        console.log(goodall)
        console.log(good)
        this.setData({goodList:good})
      }
    })

  },
  toadetail(event) {
    console.log("点击了")
    console.log(event.currentTarget.dataset.id)
    let id = event.currentTarget.dataset.id
    let url='http://116.63.12.26/article/'+id
    wx.navigateTo({
      url: '/pages/index/htmlpage/hp?name=' + url,
    })
  },
})