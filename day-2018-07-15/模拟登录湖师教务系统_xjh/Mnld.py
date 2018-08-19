#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
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
print loginresponse.url
html = loginresponse.content.decode('gbk')

def getInfor(response):
    content = response.content.decode('gb2312')
    soup = BeautifulSoup(content, 'lxml')
    #pdb.set_trace()
    uname=soup.find('span', id='xhxm')
    return uname

print ('欢迎进入教务系统')
stuname = getInfor(loginresponse)
print stuname.text

'''
cjurl = codeu +'/xscj_gc.aspx?xh=2016115020530&xm=%CF%F2%BD%FA%BB%A2&gnmkdm=N121605'
def getgrades():
  req_url =  req_url = codeu + '/xscj_gc.aspx?xh=' + payload['txtUserName'] + '&xm=' +stuname.text[0:9] + '&gnmkdm=N121603'
  pos = s.get(req_url, headers=headers)
  
'''


