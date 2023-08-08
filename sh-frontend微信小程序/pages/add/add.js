const util = require('../../utils/util.js')
const app = getApp()
Page({


  data: {
    detail_image:[], //商品详情图片
    cover_image:[] //商品封面图片
  },


  onLoad(options) {
    console.log(app.globalData.userInfo)
  },
  onShow(){
    this.getTypeList()
  },

  //获取分类
  getTypeList(){
    wx.request({
      url: 'http://116.63.12.26/api/goods/category/',
      method: 'GET',
      success: (res) => {
        console.log(res)
        this.setData({
          typeList: res.data
        })
      }
    })
  },
  getType(event){
    console.log(event.currentTarget.dataset.index)
    this.setData({
      currentIndex:event.currentTarget.dataset.index,
      typeId:this.data.typeList[event.currentTarget.dataset.index]._id
    })
  },

  //添加商品到数据库
  addGood(event){
    console.log(event)
    let good = event.detail.value

    if(!good.title){
      wx.showToast({
        icon:'error',
        title: '名称为空',
      })
      return
    }
    if(!good.price){
      wx.showToast({
        icon:'error',
        title: '价格为空',
      })
      return
    }
    if(!good.stockNumber){
      wx.showToast({
        icon:'error',
        title: '数量为空',
      })
      return
    }
    if(!this.data.typeId){
      wx.showToast({
        icon:'error',
        title: '请选择类型',
      })
      return
    }
    if(!good.contact){
      wx.showToast({
        icon:'error',
        title: '联系为空',
      })
      return
    }
    if(this.data.cover_image.length==0){
      wx.showToast({
        icon:'error',
        title: '封面图片为空',
      })
      return
    }

    wx.cloud.database().collection('shop_goods')
    .add({
      data:{
        title:good.title,
        price:Number(good.price),
        type:this.data.typeId,
        cover:this.data.cover_image[0],
        images:this.data.detail_image,
        text:good.text,
        isHome:false,
        status:true,
        stockNumber:Number(good.stockNumber),
        saleNumber:0,
        contact:good.contact,
        time:util.formatTime(new Date()),
        //卖家信息
        avatarUrl:app.globalData.userInfo.avatarUrl,
        nickName:app.globalData.userInfo.nickName,

      }
    })
    .then(res=>{
      console.log(res)
      wx.showToast({
        title: '发布成功',
      })
      this.setData({
        title:'',
        price:'',
        typeId:'',
        currentIndex:-1,
        cover_image:[],
        detail_image:[],
        text:'',
        stockNumber:'',
        contact:'',
      })
    })



  },
  //选择详情图片
  chooseDetailImage(){
    var that = this;
    wx.chooseImage({
      count: 9 - that.data.detail_image.length,
      sizeType:['original','compressed'],
      sourceType:['album','camera'],
      success(res){
        console.log(res)
        that.data.tempImgList = res.tempFilePaths
        //上传图片
        that.uploadImageDetail()
      }
    })
  },
  //上传详情图片到云存储
  uploadImageDetail(){
    var that = this;
    for(let l in this.data.tempImgList){
      wx.cloud.uploadFile({
        cloudPath:`goodImage/${Math.random()}_${Date.now()}.${this.data.tempImgList[l].match(/\.(\w+)$/)[1]}`,
        filePath: this.data.tempImgList[l],
        success(res){
          console.log(res.fileID)
          that.data.detail_image.push(res.fileID)
          that.setData({
            detail_image:that.data.detail_image
          })
        }
      })
    }
  },
  //删除详情图片
  deleteDetailImage(event){
    console.log(event.currentTarget.dataset.index)
    this.data.detail_image.splice(event.currentTarget.dataset.index,1)
    this.setData({
      detail_image:this.data.detail_image
    })
  },
 

   //选择封面图片
   chooseCoverImage(){
    var that = this;
    wx.chooseImage({
      count: 9 - that.data.cover_image.length,
      sizeType:['original','compressed'],
      sourceType:['album','camera'],
      success(res){
        console.log(res)
        that.data.tempImgList = res.tempFilePaths
        //上传图片
        that.uploadImageCover()
      }
    })
  },
  //上传封面图片到云存储
  uploadImageCover(){
    var that = this;
    for(let l in this.data.tempImgList){
      wx.cloud.uploadFile({
        cloudPath:`goodImage/${Math.random()}_${Date.now()}.${this.data.tempImgList[l].match(/\.(\w+)$/)[1]}`,
        filePath: this.data.tempImgList[l],
        success(res){
          console.log(res.fileID)
          that.data.cover_image.push(res.fileID)
          that.setData({
            cover_image:that.data.cover_image
          })
        }
      })
    }
  },
  //删除封面图片
  deleteCoverImage(event){
    console.log(event.currentTarget.dataset.index)
    this.data.cover_image.splice(event.currentTarget.dataset.index,1)
    this.setData({
      cover_image:this.data.cover_image
    })
  },
})