# 基于flask实现前后端不分离web项目

## 更新日志
### 2019年1月更新概况
#### 用户认证模块（1.1~1.7基本完成) 
- flask项目结构创建，添加用户登录、注册、注销功能（2020.1.3完成）
- flask项目结构完善及添加注册账号邮箱激活账号、未登录访问首页跳转登录页面验证功能（2020.1.4完成）
- 添加session会话保持用户登录状态功能（2020.1.6完成）
- 添加密码重置功能（2020.1.6完成）
- 添加记住密码功能，完善session会话改为配合第三方flask-session存储cookie至redis，并设置记住密码过期时间（2020.1.7完成）
- 添加提交表单错误提示功能（2020.1.7完成）
- 添加验证码验证功能,通过session保存至redis并设置验证码过期时间（2020.1.7完成）
- 添加表单提交出错时记住填写的错误信息（2020.1.7完成）
- 添加数据库密文存储账号密码功能（2020.1.7完成）

## 使用的flask插件
- jinja2（flask自带的模板语法引擎，用于渲染web网页）
- Werkzeug（flask自带的WSGI工具包，用于收发web请求）
- Flask-SQLAlchemy(第三方的ORM框架，用于操作数据库)
- Flask-blueprint(第三方用于分模块开发的蓝图插件，用于管理不同功能模块的请求路由接口函数)
- Flask-Mail（第三方的邮件服务器插件，用于提供收发邮件服务）
- PyMySQL（第三方的mysql数据库连接引擎，提供flask框架与mysql数据库间的通信）
- itsdangerous（第三方的生成临时身份令牌工具，用于提供网络传输的加解密安全验证服务）
- session(flask自带缓存插件，将cookie存储至浏览器)
- flask-session(第三方缓存插件，将cookie存储于服务器端，需配合session使用)
- pillow(第三方图像库，用于实现图像归档和处理功能)
- hashlib(python自带的哈希库，用于提供数据完整性校验服务)


## 工具
- chrome（用于访问网页）
- EditThisCookie Chrome（用于查看和清除浏览器当前页面保存的cookie信息，包括session_id、过期时间等）
- postman（用于模拟网页发送http表单请求）
- pycharm（用于编写python代码）
- Navicat Premium 12（mysql客户端，用于查看mysql数据存储情况）
- RedisDesktopManager（redis客户端，用于查看redis数据存储情况）
- redis-4.0.6（redis服务端，用于提供redis存储服务）
- MySQL Community Server-5.7.28（mysql服务端，用于提供mysql存储服务）
- VMware Workstation 12 Pro（虚拟机，用于提供虚拟的linux操作系统，实现windows下安装linux环境）
- CentOS Linux release 7.7.1908 （linux操作系统的发行版本，用于提供linux操作系统环境）
- Xshell 5(用于提供远程命令行连接，以方便的操作linux系统)
- github（用于提交和更新代码）

