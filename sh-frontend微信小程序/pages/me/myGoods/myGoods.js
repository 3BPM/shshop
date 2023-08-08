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
      url: 'http://116.63.12.26/api/goodskuspu/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        console.log("获取全部spusku的调用")
        let goodall = res.data
        var good = [];
        for (var i = 0; i < goodall.length; i++) {
           console.log(ownerid)
          // console.log(goodall[i].spu)
           console.log(goodall[i].spu.owner)
          if (goodall[i].spu.owner == ownerid) {
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
  toGoodDetail(event) {
    console.log("点击了")
    console.log(event.currentTarget.dataset.index.spu.id)
    let id = event.currentTarget.dataset.index.spu.id
    let url='http://116.63.12.26/goods/spu/'+id
    wx.navigateTo({
      url: '/pages/index/htmlpage/hp?name=' + url,
    })
  },
})