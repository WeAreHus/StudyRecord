# 模拟方正教务系统web应用

---
![](https://camo.githubusercontent.com/392a32588691a8418368a51ff33a12d41f11f0a9/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d322e372d6666363962342e737667)

该项目为模拟湖北师范大学旧正方教务系统的web应用，通过爬虫爬取学生信息并在前端界面做以展示。在功能上更加直观全面，用户只需个人学号密码即可获取个人成绩与课程信息，无须验证码登录，并且在系统首页能够以折线图的形式来展示学生个人的平均绩点走向，同时能够将个人成绩以微信推送与邮件发送给用户。

### 功能描述
---
模拟登陆湖北师范大学就教务系统，爬取学生课程与考试成绩并在前端界面中展示

系统功能：平均绩点折线图，成绩查询，课程查询，微信推送成绩信息和邮件推送成绩信息

### 运行效果部分展示
---
![登陆](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/qO4EPt8MgdOSl3knp*AwplMtwtC7qlrRbNtZiyVO0go!/b/dDYBAAAAAAAA&ek=1&kp=1&pt=0&bo=PAe7AzwHuwMDEDU!&tl=1&vuin=2018982763&tm=1535270400&sce=60-4-3&rf=viewer_311)
![主页](http://a2.qpic.cn/psb?/V13uRwZ427WzZu/7qpDE95.RPvGzU.BhHIyAM2vnMNP7Ga6u.6EWIq4SPo!/b/dDUBAAAAAAAA&ek=1&kp=1&pt=0&bo=PQe9Az0HvQMRECc!&tl=1&vuin=2018982763&tm=1535270400&sce=50-1-1&rf=viewer_311)
![成绩](http://a4.qpic.cn/psb?/V13uRwZ427WzZu/m2DOMcF8LZ3cALHpX3iY*FyBRDRiDDq6QWHvnffPXck!/b/dDcBAAAAAAAA&ek=1&kp=1&pt=0&bo=PAczAzwHMwMRECc!&tl=3&vuin=2018982763&tm=1535270400&sce=60-4-3&rf=viewer_311)
![课程](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/kQjxaXIYleww0vD.K9mcIVrrBpWgS4zF.qu0pCywk9I!/b/dEIBAAAAAAAA&ek=1&kp=1&pt=0&bo=PAe7AzwHuwMRECc!&tl=1&vuin=2018982763&tm=1535270400&sce=50-1-1&rf=viewer_311)


### 技术依赖
---
Web 应用框架：`Flask`

数据库：`MySQL`

ORM框架：`sqlalchemy`

爬虫：`request BeautifulSoup`

图像识别：[ZFCheckCode](https://github.com/sctpan/CheckCodeRecognition)

前端折线图：`pyecharts`

邮件发送：`smtplib`

微信发送：`itchat`

### 数据库结构
---
![ER图物理模型](http://a3.qpic.cn/psb?/V13uRwZ427WzZu/ld1yoDJ9Vn78Ovt0CBEbweBfgj*MTqd393ItNgZ8nko!/b/dFYBAAAAAAAA&ek=1&kp=1&pt=0&bo=4AMkAuADJAIDEDU!&tl=1&vuin=2018982763&tm=1535277600&sce=60-4-3&rf=viewer_311)

### 安装依赖库
---
通过本命令安装有关依赖库：
`pip install -r requirements.txt`

### 注意事项
---
使用前先修改config.py中的数据库信息

项目启动：`python view.py`

### 项目目录
---
```
|-- README.md
|-- __init__.py
|-- checkcode.gif
|-- config.py            
|-- exts.py
|-- manage.py
|-- matplot.py
|-- migrations				
|   |-- README
|   |-- alembic.ini
|   |-- env.py
|   |-- script.py.mako
|   `-- versions
|       |-- 12a59ed15a6f_.py
|       `-- 6c5f34ab290c_.py
|-- models.py
|-- requirements.txt
|-- sendemail.py
|-- spider.py
|-- static
|   |-- css
|   |   |-- admin.css
|   |   |-- amazeui.min.css
|   |   `-- app.css
|   |-- fonts
|   |   |-- FontAwesome.otf
|   |   |-- fontawesome-webfont.eot
|   |   |-- fontawesome-webfont.ttf
|   |   |-- fontawesome-webfont.woff
|   |   `-- fontawesome-webfont.woff2
|   |-- images
|   |   |-- app-icon72x72@2x.png
|   |   |-- favicon.png
|   |   `-- logo.png
|   `-- js
|       |-- amazeui.min.js
|       |-- app.js
|       |-- echarts.min.js
|       |-- iscroll.js
|       `-- jquery.min.js
|-- templates
|   |-- base.html
|   |-- login.html
|   |-- score.html
|   |-- sendemail.html
|   |-- student.html
|   `-- time_table.html
`-- view.py
```

### 项目设计学习过程
-----
> * 学习计算机网络，了解HTTP协议
> * 安装mysql数据库，熟悉基本操作语句
> * 学习HTML+CSS 完成简单界面设计
> * 学习flask框架，通过MySQLdb连接数据库操作，完成简单web应用
> * 接触爬虫学习，突破湖师正方教务处系统，模拟登录成功，获取个人学生成绩（重点）
> * 了解学习微信推送和邮件推送相关的第三方库,实现微信推送和邮件推送功能
> * 在github上找到识别验证码的API,成功突破自动识别验证码功能
> * 了解学习了Python matplotlib库,完成制作折线图,同时了解学习了pyecharts库,自动生成html文件实现折线图功能
> * 将所学习的所有功能实现汇总,完成设计出学生教务处系统

### 暂未完成的任务
---
实现微信发送成绩


### 开发人员
---
项目开发：[Xiang Jinhu](https://github.com/chirsxjh)，[Chen Wei](https://github.com/Cris0525)，[Fu Tongyong](https://github.com/CANYOUFINDIT)

项目指导：[Li Xipeng](https://github.com/hahaps)