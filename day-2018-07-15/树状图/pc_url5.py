#-*- coding: UTF-8 -*-
#import io
import requests
from bs4 import BeautifulSoup
from lxml import etree
import json


base_url = ('http://www.hbnu.edu.cn/')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

}
response = requests.get(base_url,headers = headers)
html = response.content.decode('utf-8')

data = etree.HTML(html)
result = etree.tostring(data)
#print(result.decode('utf-8'))
html_data = data.xpath('/html/body/div[4]/div/div[2]/div[1]/ul/li[2]/a/@href')
#print(html_data)
for i in html_data:
    print('爬取的第一级URL：'+i)
    print('    ⬇')

response1 = requests.get( i ,headers = headers)
html1 = response1.content.decode('utf-8')

data1 = etree.HTML(html1)
result1 = etree.tostring(data1)
html_data1 = data1.xpath('/html/body/div[1]/div[3]/div[2]/div[2]/ul/li[1]/a/@href')
for i1 in html_data1:
    #print(i1)
    url1 = i[0:28]+i1
print('爬取的第二级URL：'+url1)
print('    ⬇')

response2 = requests.get(url1,headers = headers)
html2 = response2.content.decode('utf-8')

data2 = etree.HTML(html2)
result2 = etree.tostring(data2)
html_data2 = data2.xpath('/html/body/div[1]/div[3]/div[1]/ul[2]/li[1]/a/@href')
for i2 in html_data2:
    #print(i2)
    url2 = i[0:28]+i2
print('爬取的第三级URL：'+url2)
print('    ⬇')

response3 = requests.get(url2,headers = headers)
html3 = response3.content.decode('utf-8')

data3 = etree.HTML(html3)
result3 = etree.tostring(data3)
html_data3 = data3.xpath('/html/body/div[1]/div[2]/ul/li[6]/a/@href')
for i3 in html_data3:
    url3 = i[0:28]+i3
print('爬取的第四级URL：'+url3)
print('    ⬇')

response4 = requests.get(url3,headers = headers)
html4 = response4.content.decode('utf-8')

data4 = etree.HTML(html4)
result4 = etree.tostring(data4)
html_data4 = data4.xpath('/html/body/div/div[3]/div[1]/ul/li[1]/a/@href')
for i4 in html_data4:
    url4 = i[0:28]+i4
print('爬取的第五级URL：'+url4)

file = open('test.json','w',encoding='utf-8')

url_1 = {'url_01':i}
url_2 = {'url_02':url1}
url_3 = {'url_03':url2}
url_4 = {'url_04':url3}
url_5 = {'url_05':url4}
data1 = [url_1,url_2,url_3,url_4,url_5]
#print(data1)
json.dump(data1,file,ensure_ascii=False)
print("写入成功！")
file.close()


