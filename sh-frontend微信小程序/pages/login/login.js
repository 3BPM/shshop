// pages/login/login.js
const app = getApp();
Page({
  //  * 页面的初始数据
  data: {
    uid:'',
    issignin: false,
    zhanghao: '',
    mima: '',
    token: '',
    loginOK: false
  },
  onLoad: function (options) {
    console.log("是注册页面吗"+options.s)
    this.setData({
      issignin: options.s
    }, function () {
      setTimeout(function () {
        // 页面已经渲染完成，可以进行其他操作
      }, 0)
    })
  },
  //  * 生命周期函数--监听页面显示
  onShow() {
    
  },

  //获取输入的账号
  getZhanghao(event) {
    this.setData({
      zhanghao: event.detail.value
    })

  },
  //获取输入的密码
  getMima(event) {
    this.setData({
      mima: event.detail.value
    })
  },

  login() {
    if (!this.checkinput()) return
    this.serverlogin()
  },
  signup() {
    if (!this.checkinput()) return
    var that=this
    wx.request({
      url: 'http://116.63.12.26/api/auth/signup/',
      method: "POST",
      data: {
        username: this.data.zhanghao,
        password: this.data.mima,
        email: "example@email.com"
      },
      success(res) {
        console.log("注册结果")
        console.log(res)
        console.log(res.statusCode)
        if (res.statusCode === 201) {
          that.serverlogin()
        }
        else {
          wx.showToast({
            icon: 'none',
            title: '注册失败',
          })
        }
      }
    })


  },
  serverlogin: function () {
    var that=this
    wx.request({
      url: 'http://116.63.12.26/api/auth/login/',
      method: "POST",
      data: {
        username: this.data.zhanghao,
        password: this.data.mima
      },
      header: { 'content-type': 'application/x-www-form-urlencoded' },
      success(res) {
        let token = res.data.token
        let uid=res.data.uid
        app.globalData.uid=uid

        if (res.statusCode === 200) {
          console.log('登录成功')
          wx.showToast({
            title: '登录成功',
          })
          app.globalData.loginOK = true
          app.globalData.token = token
          wx.setStorageSync('uid', uid);
          console.log("app登录状态"+app.globalData.loginOK+"token"+app.globalData.token)
          that.getinfo(uid);
          setTimeout(function () {
            wx.switchTab({
              url: '/pages/me/me',
            })
          }, 100)
        }
        else {
          console.log('登录失败')
          wx.showToast({
            icon: 'none',
            title: '账号或密码不正确',
          })
        }

      },
      fail(res) {
        console.log("大失败", res)
      }
    })
  },
   getinfo(u){
    console.log("uid是"+u)
    wx.request({
      url: 'http://116.63.12.26/api/user/info/',
      data: {
        owner: u
      }, 
      success: function(res) {
        console.log("获取sh站user成功")
        console.log(res.data[0].avatar)
        console.log(res.data)
        wx.setStorageSync('avatar', res.data[0].avatar)
        wx.setStorageSync('nickname',res.data[0].nickname)
      }
    })

  }
  ,
  checkinput() {
    let zhanghao = this.data.zhanghao
    let mima = this.data.mima
    console.log('账号', zhanghao, '密码', mima)
    if (zhanghao.length < 4) {
      wx.showToast({
        icon: 'none',
        title: '账号至少4位',
      })
      return false
    }
    if (mima.length < 4) {
      wx.showToast({
        icon: 'none',
        title: '密码至少4位',
      })
      return false
    }
    return true
  }
})
