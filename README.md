# SH校园二手商城项目（基于BaykeShop拜客商城）

## 介绍

本项目是软工校园二手市场选题，与原bayke项目 https://gitee.com/bayke/bayke-shop 相比，主要有：

* 增加了用户发布商品功能。

* 添加了drf后端与并做了一个微信小程序，达到了多端统一，并且在微信小程序中可以查看用户发布的商品和求购消息。

* 修改了商店资讯文章功能，变为所有用户都可发布求购消息

* 修改了原sku商品规格，变为一个二手校园商品校区的标签

* 完善了一部分后端，如添加用户余额管理用户信息管理，删除了支付宝支付
* (主要问题是小程序端的restframeworkapi没有比较好的安全措施，还是比较简陋的)

```
git fetch --all &&  git reset --hard origin/master && git pull
#云端覆盖本地命令
```

## 运行环境

> python > 3.8 & django4.1 & Mysql8.0 & redis

### 创建虚拟环境

```
cd sh-shop
python3 -m venv venv
```

### 激活虚拟环境

```
Windows: venv\Scripts\activate
Liunx: source venv/bin/activate
```

### 安装依赖

```
pip install -r requirements.txt
```

### 本地运行配置Mysql数据库

> 项目默认配置了Mysql数据库和redis缓存，需要你自行在运行项目前，配置安装好Mysql数据库及redis！
>
> **注意：clone到本地之后，先删除.idea和.vscode文件夹再进行后续操作**

- 配置Mysql数据库
  sh settings,py里面

  ```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "sh",  # 数据库名字
        "USER": "xxxx",  # 用户名
        "HOST": "localhost",  # ip
        "PORT": "3306"
    }
  }
  ```

- redis默认无密码，你也不要配置密码，如果非要配置请在`sh/settings.py`中的redis配置修改

  ```
  CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',
    }
  }
  ```

### 同步数据库

*pycharm常见问题的解决办法*

在PowerShell：因为在此系统上禁止运行脚本，解决方法 - sinler中可以知道问题的根源在于win10默认的执行策略是不载入任何配置文件，不运行任何脚本。这一点可以通过命令行查看

以管理员身份运行PowerShell
输入get-ExecutionPolicy（如果返回Restriced，则继续下述的步骤）
输入set-ExecutionPolicy RemoteSigned
输入Y按下回车
效果：`PS C:\windows\system32> Get-ExecutionPolicy
Restricted`

```bash
python manage.py makemigrations
python manage.py migrate
```

### 创建超级管理员&&初始化项目

```python
python manage.py createsuperuser
python manage.py push
python manage.py push -test
python manage.py push -nb
#pushnb 这条命令要保证上一个环境生成并拷过来的/1.json的正确性
#python manage.py dumpdata myapp --output=1.json
#python manage.py dumpdata myapp --natural-foreign --natural-primary --output=1.json
#python manage.py dumpdata myapp.MyModel --format=yaml --output=mydata.yaml
```

目前未实现 没啥用。。。

### 运行项目

```
python manage.py runserver 0:80
```

### 云端常用操作

```
#查看端口占用
netstat -antulp | grep 80
#云端运行
nohup python manage.py runserver 0:80 >djangolog
查看进程PID
ps -ef |grep nohup
ps -ef |grep python
#强制终止，死循环或无响应状态也能够终止它。
kill -9
```

| UID  | PID    | PPID   | C   | STIME | TTY    | TIME     | CMD                     |
| ---- | ------ | ------ | --- | ----- | ------ | -------- | ----------------------- |
| root | 728258 | 706968 | 0   | 04:30 | pts/82 | 00:00:00 | grep --color=auto nohup |

- `UID`：进程的用户 ID。
- `PID`：进程的 ID。
- `PPID`：父进程的 ID。
- `C`：进程占用的 CPU 使用率。
- `STIME`：进程启动时间。
- `TTY`：进程所在的终端。
- `TIME`：进程占用 CPU 的时间。
- `CMD`：进程的命令行

### 查看项目

前端
http://116.63.12.26

后台：
[登录 | 二手商城](http://116.63.12.26/shadmin/)

文档

[接口测试平台API文档](http://116.63.12.26/docs)

后台账号及密码是你在第五步创建的！

```
https://git.weixin.qq.com/wx_wx897244a5a4ecf9f0/sh-frontend
微信仓库
```

### 包含一个drf教程

http://116.63.12.26/media/drf.html

### 包含一个cloudflare 和莫脚本建的伪站

https://www.mingzr.eu.org/