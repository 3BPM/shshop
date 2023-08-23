var app = getApp();
Page({

  data: {
    goodList: [],
    bannerList: []
  },


  onLoad: function (options) {
    this.getBanners()
    this.getGoodsList()
    //获取分类
    // this.getTypeList()
  },
  onShow() {
  },
  //获取轮播图数据库记录
  getBanners() {
    wx.request({
      url: 'http://116.63.12.26/api/public/banner/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        console.log("对getBanner的调用")
        this.setData({ bannerList: res.data})
      }
    })
  },
  toBannerDetail(event) {
    console.log("点击了")
    console.log(event.currentTarget.dataset)
    let url = event.currentTarget.dataset.url
    if (url.substring(0, 4) != "http") {
      url = app.globalData.url + url
    }
    console.log(url)
    wx.navigateTo({
      url: '/pages/index/htmlpage/hp?name=' + url,
    })
  },

  getGoodsList() {
    wx.request({
      url: 'http://116.63.12.26/api/goodskuspu/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        console.log("获取全部spusku的调用")
        this.setData({ goodList: res.data.reverse()  })
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

  toSearch() {
    wx.navigateTo({
      url: '/pages/index/search/search',
    })
  },
  tofunc() {
    wx.navigateTo({
      url: '/pages/index/funcPage/functions',
    })
  },



})