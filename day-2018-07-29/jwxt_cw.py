#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
from PIL import Image
import pdb


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://jwgl1.hbnu.edu.cn/(S(nxuiogv1kq4coqvvhltax145))/default2.aspx?'
}

#构造表单字典
payload={'__VIEWSTATE':'',
        'txtUserName':'',
        'Textbox1':'',
        'TextBox2':'',
        'txtSecretCode':'',
        'RadioButtonList1':'',
        'Button1':'',
        'lbLanguage':'',
        'hidPdrs':'',
        'hidsc':'',
        '__EVENTVALIDATION':'',
        }



baseurl = 'http://jwgl1.hbnu.edu.cn'
s=requests.Session()

#获取重定向之后的url，目的是中间那段随机生成的数字
def location():
    html = s.get(baseurl, headers=headers, allow_redirects=False )
    return html.headers['location']

loc = location()
#print loc
loginurl = baseurl + loc
#print loginurl
codeu = loginurl[0:54]
codeurl = codeu + '/CheckCode.aspx?'
#print codeurl

#获取验证码
def getcode():
    img=s.get(codeurl, stream=True, headers=headers)
    with open('checkcode.gif','wb') as f:
        f.write(img.content)
    image=Image.open('checkcode.gif')
    image.show()


#获取表单字典数据
index = s.get(loginurl, headers=headers)
soup = BeautifulSoup(index.content,'lxml')
value1=soup.find('input',id='__VIEWSTATE')['value']
value2=soup.find('input',id='__EVENTVALIDATION')['value']

payload['txtUserName']=raw_input("请输入您的学号:")
payload['TextBox2']=raw_input("请输入您的密码:")
getcode()
payload['txtSecretCode']=raw_input("请输入验证码:")
payload['RadioButtonList1']=u"学生".encode('gb2312','replace')
payload['__VIEWSTATE']=value1       
payload['__EVENTVALIDATION']=value2 
payload['RadioButtonList1']= '%D1%A7%C9%FA' 

#登录教务系统
loginresponse = s.post(loginurl, data=payload, headers=headers)
#print loginresponse.url
html = loginresponse.content.decode('gbk')


data1 = {'__VIEWSTATE': '',
         'ddlXN':'', 
         'ddlXQ': '',
         'Button1':'',
         '__EVENTVALIDATION':''
        }
xscj_url = codeu + '/xscj_gc.aspx?xh=2016115020429&xm=%B3%C2%CD%FE&gnmkdm=N121605'
#print xscj_url
xscj = s.get(xscj_url,headers = headers)
soup1 = BeautifulSoup(xscj.content,'lxml')
value3 = soup1.find('input',id='__VIEWSTATE')['value']
value4 = soup1.find('input',id='__EVENTVALIDATION')['value']

data1['__VIEWSTATE']=value3
data1['__EVENTVALIDATION']=value4
data1['Button1']=u"学生".encode('gb2312','replace')
xscj_response = s.post(xscj_url,headers = headers,data = data1)
html1 = xscj_response.content.decode('gbk')

print html1







