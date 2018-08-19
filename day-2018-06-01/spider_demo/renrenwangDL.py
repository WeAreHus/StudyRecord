#-*-coding:utf-8-*-
# 了解模拟登录的方法和流程

import requests

# 1. 创建session对象，可以用来发送请求，同时保存Cookie值
ssion = requests.session()

# 2. 构建请求报头
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

# 3. 处理登录需要的参数
formdata = {"email" : "472484497@qq.com", "password" : "meng1103."}

# 4. 发送post请求，并传递表单数据，如果登录成功，则自动保存Cookie
# 这一步就是模拟登陆，发送post请求
ssion.post("http://www.renren.com/PLogin.do", data = formdata)

# 5. 发送访问需要登录权限的页面的请求（因为之前的模拟登录成功，保存了Cookie)
response = ssion.get("http://www.renren.com/327550029/profile", headers = headers)

# 6. 打印响应内容
print(response.content.decode("utf-8"))
