# 自研加魔改小程序

1.Token认证
    // wx.request({  //登录后这么写
    //   url: 'url',
    //   data:{access_token:wx.getStorageSync('key')}
    // })

2.多个页面传参 比如login 和signup就可以 还有search 和 view 具体的商品spu

      传参主要是三种：
      1.简单值传参如：id=1，string = asdfg之类，其中字符不包含特殊字符如？、=之类
      2.含特殊字符传参如一个地址http://r.photo.store.qq.com/psb?/V10VqIG41I6D36/r5rQV.oz3tu1uuNvJjkDIzwhKi6nUfZaaLEH9UnNUCk!/r/dBkBAAAAAAAA
      3.对象类型传参如一个数组，image【】。
      第一种的话比较简单比如
    
      这个是源页面的js文件他需要在wxml文件里面进行属性绑定
    
      enlargr11: function (event) {
          var id = event.currentTarget.dataset.id;
          console.log("id"+id);
          wx.navigateTo({
            url: '../toimg/toimg?id='+id,
          })
        },
      <image class="slide-image" mode="aspectFit" src="{{item.imageUrl}}" bindtap="enlargr" 
                data-id="{{item.imgid}}"/>//这里需要注意照片大小问题
      这里我在js的data里面是定义了一个imageUrls数组里面有imid和imageUrl两个内容如
    
      imageUrls: [{
              "imageUrl": "https://img0.baidu.com/it/u=154603817,3028123296&fm=26&fmt=auto",
              "imgid": 0
            }]
      然后目的页面需要在初始渲染时进行接收，代码如
    
      ​
      onLoad2: function (options) { //传imageurl的下标
          var pid = options.id;
          console.log("pid" + pid);
          this.data.id = pid;//前面那个this.data.就是说是引用什么data里面定义的id
          this.setData({
    
          })
          console.log("id " + id);//打印id
        },
    
      ​
      第二种稍微复杂有点如：
    
      因为在微信小程序里面encodeURIComponent进行转化操作（主要是我也不知道应该怎么称呼）
    
      enlargr: function (event) { //直接传参src地址的
          var imagesrc = event.currentTarget.dataset.src;
          console.log(imagesrc);
          //var tt = JSON.stringify(imagesrc);
          //console.log(tt);
          var src = encodeURIComponent(imagesrc);
          console.log("src")
          console.log(src);
          wx.navigateTo({
            //url: '../toimg/toimg?imgsrc='+src,
            url: '../toimg/toimg?imgsrc='+src,
          })
        },
      然后此时wxml里面的属性绑定需要做一些修改如
    
      <image class="slide-image" mode="aspectFit" src="{{item.imageUrl}}" bindtap="enlargr" 
                data-src="{{item.imageUrl}}"/>//这里需要注意照片大小问题
      目的页面为：然后接受时肯定要解密，使用decodeURIComponent
    
      onLoad: function (options) { //这个是尝试直接传参路径
          var t = options.imgsrc;
          console.log(t);
    
          var src = decodeURIComponent(t);
          console.log("src");
          console.log(src);
          this.data.imgsrc = src;
          this.setData({
            //imagesrc: src,
          })
          console.log(this.data.imgsrc)
        },
      第三种就复杂了
    
      原来上是先将其转化为json格式，然后考虑是否有特殊字符，就是需不需要加密就是加上encodeURIComponent和decodeURIComponent进行包装一下，如：源页面
    
      enlargr2:function(e){
          console.log(e.currentTarget.dataset.item);
          let str=JSON.stringify(e.currentTarget.dataset.item);
        console.log(str);
        var data0 = encodeURIComponent(e.currentTarget.dataset.item);
            let data=JSON.stringify(data0);
    
            var data1 = JSON.stringify(e.currentTarget.dataset.item);
            var data2 = encodeURIComponent(data1);
    
            wx.navigateTo({
            url: '../toimg/toimg?data='+data2,
            })
    
    
        },
    
      对应的wxml里面也需要做一些修改，就是属性绑定哪里需要改为item，如
    
      ​
      <image class="slide-image" mode="aspectFit" src="{{item.imageUrl}}" bindtap="enlargr" 
                data-item="{{item}}"/>//这里需要注意照片大小问题
    
      ​
      目的页面就是，如
    
      onLoad3: function (options) {
          console.log(options.data);
          var data = options.data;
          var datat = decodeURIComponent(options.data);
          console.log(datat);
          //var data3 = JSON.stringify(data);
          //var data4 = JSON.parse(data1);
          //var data5 = JSON.parse(options.data);
          //var data6 = decodeURIComponent(data5);
    
          this.data.imageUrlts = datat;
    
          console.log(this.data.imagesrc);
          this.setData({
                })
    
          console.log(this.data.imageUrlts);
        },
    
      上面的话我是没有在接受时从json转化回来，但是结果还是正确的，接受页面的json.parse和json.stringify有什么区别我没查，如果有需要可以自行了解。
    
      总结一下：
    
      主要是关于带特殊字符的传参，需要进行加密解码既encodeURIComponent和decodeURIComponent（个人叫法），然后就是是否为对象类型，就是需不需要json格式转化。对于源页面js文件里面调用navigateTo进行带参数跳转还有其他跳转方式参考微信官方文档，
    
      wx.navigateTo({
    
            url: '../toimg/toimg?data='+data2,
    
            })
    
      url那里好像不止一种写法我个人是怎么写的，就是‘跳转页面url？数据名=’+数据内容，

  原文链接：https://blog.csdn.net/weixin_50398435/article/details/124107889

3.通常的请求方式

      /**
        * 封装wx.request请求
        * method： 请求方式
        * url: 请求地址
        * data： 要传递的参数
        * callback： 请求成功回调函数
        * errFun： 请求失败回调函数
        * token: token值
        **/
          // wxRequest(method, url, data, callback, errFun, token) {
          //   wx.request({
          //     url: url+'/api',
          //     method: method,
          //     data: data,
          //     header: {
          //       // application/x-www-form-urlencoded
          //       'content-type': 'application/json;charset=UTF-8',
          //       'Accept': 'application/json',
          //       'token': token
          //     },
          //     dataType: 'json',
          //     success: function (res) {
          //       callback(res);
          //     },
          //     fail: function (err) {
          //       errFun(err);
          //     }
          //   })
          // },