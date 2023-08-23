
Page({


  data: {

  },


  onLoad: function (options) {

  },
  getValue(event){
    console.log(event.detail.value)
    let inputValue = event.detail.value
    this.setData({
      inputValue
    })
    

  },
  search(){
    wx.request({
      url: 'http://116.63.12.26/api/goods/spu/',
      method: 'GET',
      success: (res)=> {
      console.log(res)
      this.setData({goodList:res.data})
      }
      })
   
  },
  toGoodDetail(event){
    console.log(event.currentTarget.dataset)
    let id = event.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/goodDetail/goodDetail?id=' + id ,
    })
  },
  
})