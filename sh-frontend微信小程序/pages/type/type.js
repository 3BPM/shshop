
Page({
  data: {
    currentType: 0,
    goodList: [],
    allGoodList: [],//all goods
    typeList: [],
  },

  onLoad: function (options) {
    console.log('llllllllllllllllllllllllllllllllllll这是type')
    this.getGoodsList()
    this.getTypeList()

  },
  onShow() {
  },
  //获取分类
  getTypeList() {
    wx.request({
      url: 'http://116.63.12.26/api/goods/category/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        this.setData({
          typeList: res.data
        })
        //this.getTypeGoodsList_first(res.data[0]._id)
      }
    })
  },
  getGoodsList() {
    wx.request({
      url: 'http://116.63.12.26/api/goodskuspu/',
      method: 'GET',
      success: (res) => {
        console.log(res.data)
        console.log("获取全部spusku的调用")
        this.setData({ allGoodList: res.data })
      }
    })
  },
  getTypeGoodsList(event) {
    //获取对应分类下面的商品列表
    console.log('看呀')
    console.log(this.data.allGoodList)
    console.log(this.data.typeList)
    console.log(event.currentTarget.dataset.index)
    console.log(this.data.typeList[event.currentTarget.dataset.index])

    let index = event.currentTarget.dataset.index
    let typeid = this.data.typeList[index]["id"]
    console.log(typeid)
    var good = [];

    for (var i = 0; i < this.data.allGoodList.length; i++) {
      if (this.data.allGoodList[i].spu.id === typeid) {
        good.push(this.data.allGoodList[i]);
      }
    }
    console.log(good)

    this.setData({
      currentType: index,
      goodList: good
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