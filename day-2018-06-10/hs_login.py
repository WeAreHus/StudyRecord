#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
from PIL import Image


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection':'keep-alive',
    'Content-Length': '23472',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'jwgl1.hbnu.edu.cn',
    'Origin': 'http://jwgl1.hbnu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'http://jwgl1.hbnu.edu.cn/(S(dbawgs45zpzce455l3uuyhia))/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }


payload={'__VIEWSTATE':'',
        'txtUserName':'',
        'TextBox2':'',
        'txtSecretCode':'',
        'RadioButtonList1':'',
        'Button1':'',
        'lbLanguage':'',
        'hidPdrs':'',
        'hidsc':'',
        '__EVENTVALIDATION':'',
        }



s=requests.Session()
index=s.get('http://www.hbnu.edu.cn/', headers=headers)
img=s.get('http://jwgl1.hbnu.edu.cn/(S(bwjxdsvyr3x3gs55v40kiy55))/CheckCode.aspx?', stream=True, headers=headers)
with open('checkcode.gif','wb') as f:
    f.write(img.content)
image=Image.open('checkcode.gif')
image.show()



soup = BeautifulSoup(index.content,'lxml')
value1=soup.find('input',id='__VIEWSTATE')#['value']
value2=soup.find('input',id='__EVENTVALIDATION')#['value']

payload['txtUserName']=raw_input("请输入您的学号:")
payload['TextBox2']=raw_input("请输入您的密码:")
payload['txtSecretCode']=raw_input("请输入验证码:")

payload['__VIEWSTATE']=value1       
payload['__EVENTVALIDATION']=value2 
payload['RadioButtonList1']= '%D1%A7%C9%FA' 

post1=s.post('http://jwgl1.hbnu.edu.cn/(S(alubo345so0mcw45hovasp2b))/xscj_gc.aspx?xh=2016115060726&xm=%u9648%u5a01&gnmkdm=N121605', data=payload, headers=headers)



#get_score=s.post('http://jwgl1.hbnu.edu.cn/(S(2sjomd55nxdrck3dumi55555))/default2.aspx',  headers=headers)
#print (get_score.content.decode('gbk'))

#base_url = ("http://jwgl1.hbnu.edu.cn/(S(alubo345so0mcw45hovasp2b))/xscj_gc.aspx?xh=2016115060726&xm=陈威&gnmkdm=N121605")

#get_score = s.get(base_url,headers = headers)
html = post1.content.decode('gbk')
print(html)

soup = BeautifulSoup(html,'lxml')
x = soup.find_all('span', id_='xftj')
for i in x:
    score = i.get_text()
    print(score)


