const app =getApp()
const util = require('../../utils/util.js')
Page({

  data: {
    orderIdList:[]
  },

  onLoad: function (options) {

    // if(app.globalData.orderList.length<10){
    //   wx.navigateBack({
    //     delta: 0,
    //     success(){
    //       wx.showToast({
    //         icon:'error',
    //         title: '数量小于10',
    //       })
    //     }
    //   })
    // }

    console.log(app.globalData.orderList)
    this.setData({
      orderList:app.globalData.orderList
    })
    this.total()

    //读取缓存里的地址
    let address = wx.getStorageSync('address')
    this.setData({
      phone:address.telNumber,
      name:address.userName,
      address:address.provinceName + address.cityName + address.countyName + address.detailInfo
    })
    
  },
  add(event){
    console.log(event.currentTarget.dataset.index)
    let index = event.currentTarget.dataset.index

    //库存判断
    if(this.data.orderList[index].number + 1 > this.data.orderList[index].stockNumber){
      wx.showToast({
        icon:'error',
        title: '库存不足',
      })
      return
    }
    
    this.data.orderList[index].number = this.data.orderList[index].number + 1
    //console.log(this.data.orderList)
    this.setData({
      orderList: this.data.orderList
    })


    //计算合计
    this.total()
  },
  reduce(event){

    console.log(event.currentTarget.dataset.index)
    let index = event.currentTarget.dataset.index
    if(this.data.orderList[index].number != 1){
      this.data.orderList[index].number = this.data.orderList[index].number - 1
    }else{
      wx.showToast({
        title: '当前数量已经不能减少了',
        icon:'none'
      })
    }
    this.setData({
      orderList: this.data.orderList
    })


    //计算合计
    this.total()
  },
  //计算合计价格
  total(){
    let sum = 0;
    let totalNumber = 0
    for(let index in this.data.orderList){

      sum = sum + this.data.orderList[index].price * this.data.orderList[index].number
      
      totalNumber = totalNumber + this.data.orderList[index].number


    }
    this.setData({
      sum: sum.toFixed(2),
      totalNumber
    })


  },
  addAddress(){
    let that = this;
    wx.chooseAddress({
      success: (result) => {

        console.log(result)
        that.setData({
          phone:result.telNumber,
          name:result.userName,
          address:result.provinceName + result.cityName + result.countyName + result.detailInfo
        })
        wx.setStorageSync('address', result)
      },
    })
  },
  getNote(event){
    console.log(event.detail.value)
    this.setData({
      note:event.detail.value
    })
  },
  addOrder(){

    console.log(util.formatTime(new Date))
    let time = util.formatTime(new Date)
    //每一个商品产生一个订单
    for(let l in this.data.orderList){
      wx.cloud.database().collection('shop_orders').add({
        data:{
          name:this.data.name,
          phone:this.data.phone,
          address:this.data.address,
          goods:[this.data.orderList[l]],
          totalMoney:this.data.orderList[l].price,
          time:time,
          note:this.data.note,
          status: -1,
          sellerId:this.data.orderList[l]._openid
          //-2: 取消订单
          //-1：待支付
          // 0: 待发货
          // 1：待收货 +已发货 ；
          // 2：待评价 ；
          // 3：已完成
        }
      }).then(res=>{
        console.log(res._id)
        
       
        let orderId = res._id
        this.data.orderIdList.push(orderId)
        this.setData({
          orderIdList:this.data.orderIdList
        })
  
        if(l == this.data.orderList.length-1){
          //调起微信支付
          this.pay()
    
          //调起虚拟支付
          this.xuniPay()
        }
  
      })
    }
    

  },
  xuniPay(){
    let that = this;
    wx.showModal({
      title:'提示',
      content:'是否支付商品价格' + this.data.sum + '元',
      confirmText:'支付'
    })
    .then(res=>{
      console.log(res)

      if(res.confirm == true){
        //循环更新每个订单的支付状态
        for(let l in this.data.orderIdList){
          wx.cloud.database().collection('shop_orders').doc(this.data.orderIdList[l])
          .update({
            data:{
              status:0
            }
          })
          .then(result=>{
            console.log(result)

            if(l == this.data.orderIdList.length-1){
              //从购物车里面清除购物车里面的商品
              that.clearCartList()

              //添加商品销量  减去对应库存数量
              that.addSaleNumber()

              wx.navigateBack({
                delta: 0,
                success(){
                  wx.showToast({
                    title: '支付成功',
                  })
                }
              })
            }
            
          })
        }
        
      }else{
        wx.navigateBack({
          delta: 0,
          success(){
            wx.showToast({
              icon:'error',
              title: '支付失败',
            })
          }
        })
        
      }
   
      
    })
  },
  clearCartList(){

    for(let i in app.globalData.cartList){

      for(let j in app.globalData.orderList){

        if(app.globalData.orderList[j]._id == app.globalData.cartList[i]._id){
          app.globalData.cartList.splice(i,1)
        }

      }

    }
    wx.setStorageSync('cartList', app.globalData.cartList)


  },
  //添加商品销量  减去对应库存数量
  addSaleNumber(){

    for(let l in app.globalData.orderList){

      wx.cloud.database().collection('shop_goods')
      .doc(app.globalData.orderList[l]._id)
      .update({
        data:{
          saleNumber:wx.cloud.database().command.inc(app.globalData.orderList[l].number),
          stockNumber:wx.cloud.database().command.inc(-app.globalData.orderList[l].number)
        }
      })
      .then(res=>{
        console.log(res)
      })

    }

  },
  pay(){

  }
})