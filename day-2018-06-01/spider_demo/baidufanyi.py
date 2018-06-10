#-*-coding:utf-8-*-
import json
import requests


# 发送post请求的url地址
baes_url = "http://fanyi.baidu.com/v2transapi"

# 请求报头
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

# 用户输入的需要翻译的字符串
keyword = raw_input("请输入需要翻译的字符串:")

# post请求发送时，传递的表单数据
formdata = {
    "from" : "auto",
    "to" : "auto",
    "query" : keyword,
    "transtype" : "translang",
    "simple_means_flag" : "3"
}

# 发送post请求，同时传递表单数据（在data参数里指定）
response = requests.post(baes_url, data = formdata, headers = headers)


result = response.content.decode("utf-8")

content = json.loads(result)


# json.loads() 将json字符串转为Python数据类型

# 通过字典的键值对进行取值，取出最后的翻译结果
print(content["trans_result"]["data"][0]["dst"])

