const app = getApp()
Page({

  data: {
    //全选的状态
    allChoose:false
  },

  onLoad: function (options) {

  },
  onShow(){

    console.log(app.globalData.cartList)
    this.setData({
      cartList:app.globalData.cartList
    })

    //计算合计
    this.total()
  },
  add(event){
    console.log(event.currentTarget.dataset.index)
    let index = event.currentTarget.dataset.index
    this.data.cartList[index].number = this.data.cartList[index].number + 1
    //console.log(this.data.cartList)
    this.setData({
      cartList: this.data.cartList
    })
    //更新全局里和缓存里的的购物车列表数据
    app.globalData.cartList = this.data.cartList 
    wx.setStorageSync('cartList', this.data.cartList )

    //计算合计
    this.total()
  },
  reduce(event){

    console.log(event.currentTarget.dataset.index)
    let index = event.currentTarget.dataset.index
    if(this.data.cartList[index].number != 1){
      this.data.cartList[index].number = this.data.cartList[index].number - 1


      this.setData({
        cartList: this.data.cartList
      })
      //更新全局里和缓存里的的购物车列表数据
      app.globalData.cartList = this.data.cartList 
      wx.setStorageSync('cartList', this.data.cartList)
  
      //计算合计
      this.total()
    }else{

      wx.showModal({
        title:'提示',
        content:'确认从购物车删除此商品吗',
        confirmText:'确定'
      })
      .then(res=>{
        if(res.confirm == true){

          this.data.cartList.splice(index,1)

          this.setData({
            cartList: this.data.cartList
          })
          //更新全局里和缓存里的的购物车列表数据
          app.globalData.cartList = this.data.cartList 
          wx.setStorageSync('cartList', this.data.cartList)
      
          //计算合计
          this.total()
          
        }
      })


    }
    
  },
  chooseGood(event){
    console.log(event.currentTarget.dataset.index)
    let index = event.currentTarget.dataset.index
    this.data.cartList[index].choose = !this.data.cartList[index].choose
    this.setData({
      cartList: this.data.cartList
    })
    //更新全局里和缓存里的的购物车列表数据
    app.globalData.cartList = this.data.cartList 
    wx.setStorageSync('cartList', this.data.cartList)

    //计算合计
    this.total()
  },
  toGoodDetail(event){
    console.log(event.currentTarget.dataset)
    let id = event.currentTarget.dataset.id
    wx.navigateTo({
      url: '/pages/goodDetail/goodDetail?id=' + id ,
    })
  },
  //全选
  chooseAll(){

    this.setData({
      allChoose:!this.data.allChoose
    })
    if(this.data.allChoose == true){
      for(let index in this.data.cartList){
        this.data.cartList[index].choose = true
      }
      
    }else{
      for(let index in this.data.cartList){
        this.data.cartList[index].choose = false
      }
    }
    this.setData({
      cartList:this.data.cartList
    })
    //更新全局里和缓存里的的购物车列表数据
    app.globalData.cartList = this.data.cartList 
    wx.setStorageSync('cartList', this.data.cartList)

    //计算合计
    this.total()
  },
  //计算合计价格
  total(){
    let sum = 0;
    for(let index in this.data.cartList){

      if(this.data.cartList[index].choose == true){
        sum = sum + this.data.cartList[index].price * this.data.cartList[index].number
      }

    }
    this.setData({
      sum: sum.toFixed(2)
    })


  },
  //跳入订单页面
  toOrder(){


    let orderList = []
    for(let index in this.data.cartList){
      if(this.data.cartList[index].choose == true){
        orderList.push(this.data.cartList[index])
      }
    } 
    
    app.globalData.orderList = orderList

    if(app.globalData.orderList.length == 0){
      wx.showToast({
        icon:'error',
        title: '请选择商品',
      })
      return
    }

    wx.navigateTo({
      url: '/pages/order/order',
    })
  }
})