Page({

  /**
   * 页面的初始数据
   */
  data: {
    urlvale: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    let that = this
    that.setData({
      urlvale:options.name
    })
  }
})
