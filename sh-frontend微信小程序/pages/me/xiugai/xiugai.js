Page({
  data: {
    avatarUrl: '', // 用户当前头像的URL
  },

  onLoad: function (options) {
    this.setData({ avatarUrl: wx.getStorageSync('avatar') }); // 从本地缓存获取用户头像URL，并设置Data中
  },

  chooseImage: function () {
    const that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        that.setData({ avatarUrl: res.tempFilePaths[0] }); // 设置选中图片的临时文件路径
      },
    });
  },

  submit: function () {
    const that = this;
    wx.uploadFile({
      url: 'http://116.63.12.26/api/auth/upimg/', // 你的服务器端API接口地址
      filePath: that.data.avatarUrl,
      name: 'avatar',
      formData: {
        'nickname': wx.getStorageSync('nickname'), // 将用户昵称作为查询条件
      },
      success: function (res) {
        // 上传成功，更新本地缓存中的头像URL
        wx.setStorageSync('avatar', that.data.avatarUrl);
        // 提示用户上传成功
        wx.showToast({
          title: '头像更新成功',
          icon: 'success',
          duration: 2000,
        });
        wx.navigateTo({
          url: '/pages/me/me',
        });
      },
      fail: function (error) {
        console.error('上传失败', error);
      },
    });
  },
});