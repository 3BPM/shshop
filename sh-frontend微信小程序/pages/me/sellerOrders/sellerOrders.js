const app =getApp()
Page({


  data: {
    status:0
  },

  onLoad: function (options) {

    this.getOrderList()

    console.log(app.globalData.openid)

  },
  choooType(event){
    console.log(event.currentTarget.dataset.type)
    let status = event.currentTarget.dataset.type
    this.setData({
      status
    })
    this.getOrderList()

  },
  getOrderList(){
    wx.cloud.database().collection('shop_orders')
    .where({
      status:Number(this.data.status),
      sellerId:app.globalData.openid,
    })
    .orderBy('time','desc')
    .get()
    .then(res=>{
      console.log(res)
      this.setData({
        orderList:res.data
      })
    })
  },

  pay(event){
    let index = event.currentTarget.dataset.index
    console.log(index)
    wx.showModal({
      title:'提示',
      content:'是否支付商品价格' + this.data.orderList[index].totalMoney + '元',
      confirmText:'支付'
    })
    .then(res=>{
      console.log(res)

      if(res.confirm == true){
        wx.cloud.database().collection('shop_orders').doc(this.data.orderList[index]._id)
        .update({
          data:{
            status:0
          }
        })
        .then(result=>{
          console.log(result)
          wx.showToast({
            title: '支付成功',
          })
          this.getOrderList()

          //添加商品销量  减去对应库存数量
          this.addSaleNumber(index)


        })
      }else{

        wx.showToast({
          icon:'error',
          title: '支付失败',
        })
        
      }
   
      
    })

  },

  cancel(event){
    let index = event.currentTarget.dataset.index
    console.log(index)

    wx.showModal({
      title:'提示',
      content:'是否取消此订单',
      confirmText:'确定'
    })
    .then(res=>{
      if(res.confirm == true){
        wx.cloud.database().collection('shop_orders').doc(this.data.orderList[index]._id)
        .update({
          data:{
            status:-2
          }
        })
        .then(result=>{
          console.log(result)
          wx.showToast({
            title: '取消成功',
          })
          //退款
          this.refund()
          this.getOrderList()
        })
      }else{

      }


    })


  },
  //退款
  refund(){

  },
  confirm(event){
    let index = event.currentTarget.dataset.index
    console.log(index)
    
    wx.showModal({
      title:'提示',
      content:'确认已收货吗',
      confirmText:'确定'
    })
    .then(res=>{
      if(res.confirm == true){
        wx.cloud.database().collection('shop_orders').doc(this.data.orderList[index]._id)
        .update({
          data:{
            status:2
          }
        })
        .then(result=>{
          console.log(result)
          wx.showToast({
            title: '保存成功',
          })
          this.getOrderList()
        })
      }else{

      }

    })


  },
  toComment(event){
    wx.navigateTo({
      url: '/pages/me/myOders/comment/comment?id=' + event.currentTarget.dataset.id +'&goodName=' + event.currentTarget.dataset.title +'&orderId=' + event.currentTarget.dataset.orderid,
    })
  },
  //添加商品销量  减去对应库存数量
  addSaleNumber(index){

    for(let l in this.data.orderList[index].goods){

      wx.cloud.database().collection('shop_goods')
      .doc(this.data.orderList[index].goods[l]._id)
      .update({
        data:{
          saleNumber:wx.cloud.database().command.inc(this.data.orderList[index].goods[l].number),
          stockNumber:wx.cloud.database().command.inc(-this.data.orderList[index].goods[l].number)
        }
      })
      .then(res=>{
        console.log(res)
      })

    }

  },



  //商家点击发货
  fahuo(event){
    let index = event.currentTarget.dataset.index
    console.log(index)

    wx.showModal({
      title:'提示',
      content:'是否确认发货',
      confirmText:'确定'
    })
    .then(res=>{
      if(res.confirm == true){
        wx.cloud.database().collection('shop_orders').doc(this.data.orderList[index]._id)
        .update({
          data:{
            status:1
          }
        })
        .then(result=>{
          console.log(result)
          wx.showToast({
            title: '保存成功',
          })
         
          this.getOrderList()
        })
      }
    })


  },

 
})