#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import os
import Image
import lxml

headers = {
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

index = s.get('http://www.hbnu.edu.cn/', headers=headers)
soup = BeautifulSoup(index.content,'lxml')
value1=soup.find('input',id='__VIEWSTATE')#['value']
value2=soup.find('input',id='__EVENTVALIDATION')#['value']

payload['txtUserName']=raw_input("UserName:")
payload['TextBox2']=raw_input("Password:")
payload['txtSecretCode']=raw_input("checkcode:")

payload['__VIEWSTATE']=value1       
payload['__EVENTVALIDATION']=value2 
payload['RadioButtonList1']= '%D1%A7%C9%FA' 

post1=s.post('http://jwgl1.hbnu.edu.cn/(S(bwjxdsvyr3x3gs55v40kiy55))', data=payload, headers=headers)

data={
    'btn_zcj':'%C0%FA%C4%EA%B3%C9%BC%A8',#学年成绩：btn_xn 历年成绩：btn_zcj
    'ddlXN':'',
    'ddlXQ':'',
    '__EVENTVALIDATION': '',
    '__EVENTTARGET':'',   
    '__EVENTARGUMENT' :'',
    '__VIEWSTATE':'',
    'hidLanguage':'',
    'ddl_kcxz':'',
}

#注意！先获取框架源代码，提取__EVENTARGUMENT和__VIEWSTATE值后作为post内容进行下一步
get_source=s.get('http://jwgl1.hbnu.edu.cn/(S(i3l3eqqqkeopakum2cs1kwbj))/xscj_gc.aspx?xh=2016115020530&xm=%CF%F2%BD%FA%BB%A2&gnmkdm=N121605',headers=headers).content

soup=BeautifulSoup(get_source,'lxml')
value3=soup.find('input',id='__VIEWSTATE')#['value']
value4=soup.find('input',id='__EVENTVALIDATION')#['value']
data['__VIEWSTATE']=value3
data['__EVENTVALIDATION']=value4

get_score=s.post('http://jwgl1.hbnu.edu.cn/(S(i3l3eqqqkeopakum2cs1kwbj))/xscj_gc.aspx?xh=2016115020530&xm=%CF%F2%BD%FA%BB%A2&gnmkdm=N121605', data=data, headers=headers)
print (get_score.content)
