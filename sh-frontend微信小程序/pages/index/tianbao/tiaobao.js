// pages/login/login.js
import Base64 from "../../../utils/base64.js";
const app = getApp();
Page({
  //  * 页面的初始数据
  data: {

    xuehao: '',
    mima: '',
    token: '',
    loginOK: false
  },
  onLoad: function (options) {
    console.log("是注册页面吗" + options.s)
  },
  //  * 生命周期函数--监听页面显示
  onShow() {
    let user = wx.getStorageSync('user')
    let token = wx.getStorageSync('key')
    if (user && token) {
      this.setData({
        loginOK: true,
        name: user.name
      })
    } else {
      this.setData({
        loginOK: false
      })
    }
  },

  //获取输入的账号
  getZhanghao(event) {
    this.setData({
      xuehao: event.detail.value
    })
  },
  //获取输入的密码
  getMima(event) {
    this.setData({
      mima: event.detail.value
    })
  },

  qd() {

    wx.request({
      url: 'http://bjxyxsxx.buaa.edu.cn/bjxy/qdqj/addQdInfo.do',
      method: 'POST',
      data: {
        stuNum: '20185647',
        key: '',
        address: '中国北京市朝阳区双营路',
      },
      header: {
        'content-type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive'
      },
      success(res) {
        let status = res.data
        if (res.statusCode === 200) {
          console.log('签到成功')
        }
        else {
          console.log('登录失败')
          wx.showToast({
            title: '不正确',
          })
        }
        console.log(res)
      },
      fail(res) {
        console.log("大失败", res)
      }
    })
  },
  login() {
    var password = this.data.mima;
    let str = "ABCDEFG";
    let base64 = new Base64()
    //加密base64.encode
    let jiami = base64.encode(str)
    console.log("base64输出 " + jiami); // 输出 %2BOlLRbEaIKk%3D
    wx.request({
      url: 'http://bjxyxsxx.buaa.edu.cn/bjxy/app/stuLogin.do',
      method: 'GET',
      data: {
        sblb: '0',
        key: '1B52D9163104E2EA9B5A295EB3843FE9D15133FE',
        phoneNum: '13661032719',
        phoneIMEI: '1B52D9163104E2EA9B5A295EB3843FE9D15133FE',
        pwd: '%2BOlLRbEaIKk%3D',
        deviceToken: 'AjA9a1NQadKW6tt0JWV7SwajvMSkaKBLI-9ekdbGch0w'
      },
      header: { 'content-type': 'application/x-www-form-urlencoded' },
      success(res) {
        let status = res.data
        if (res.statusCode === 200) {
          console.log('登录成功')
          console.log(status)
          wx.showToast({
            title: '登录成功',
          })
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

})
