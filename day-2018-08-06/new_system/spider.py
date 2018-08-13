#-*-coding:utf-8-*-
import os
import pdb
import urllib2

import requests
from bs4 import BeautifulSoup
from lxml import etree
from PIL import Image
from ZFCheckCode import recognizer, trainner

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://jwgl1.hbnu.edu.cn/(S(nxuiogv1kq4coqvvhltax145))/default2.aspx?'
}

baseurl = 'http://jwgl1.hbnu.edu.cn'
s=requests.Session()
html = s.get(baseurl, headers=headers, allow_redirects=False )
loc = html.headers['location']
loginurl = baseurl + loc
codeu = loginurl[0:54]
codeurl = codeu + '/CheckCode.aspx?'

# 获取验证码并自动识别
def checkcode():
    img=s.get(codeurl, stream=True, headers=headers)
    with open('checkcode.gif','wb') as f:
        f.write(img.content)
    trainner.update_model() 
    code = recognizer.recognize_checkcode('/home/fty/new-system/checkcode.gif')
    #print(code)
    return code



def spider_login(id, passwd):
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
    
    #获取表单字典数据
    index = s.get(loginurl, headers=headers)
    soup = BeautifulSoup(index.content,'lxml')
    value1=soup.find('input',id='__VIEWSTATE')['value']
    value2=soup.find('input',id='__EVENTVALIDATION')['value']
    payload['txtUserName']=id
    payload['TextBox2']=passwd
    code = checkcode()
    payload['txtSecretCode']= code
    payload['RadioButtonList1']=u"学生".encode('gb2312','replace')
    payload['__VIEWSTATE']=value1       
    payload['__EVENTVALIDATION']=value2 
    payload['RadioButtonList1']= '%D1%A7%C9%FA' 

    loginresponse = s.post(loginurl, data=payload, headers=headers)
    content = loginresponse.content.decode('gb2312')
    soup = BeautifulSoup(content, 'lxml')
    uname=soup.find('span', id='xhxm')
    xsxm =  uname.text

    # 返回学生姓名
    return xsxm




def getgrades(id, name):

    payload1={'__VIEWSTATE':'',
          'ddlXN':'', 
          'ddlXQ':'' ,
          'Button1':'',
          '__EVENTVALIDATION':'',

}
    #url2 = spider_login(id, passwd)
    name = name[0:9]
    cname = urllib2.quote(name.encode('gb2312'))
    xingming = urllib2.quote(cname) 

    req_url = codeu + '/xscj_gc.aspx?xh=' + str(id) + '&xm=' + xingming + '&gnmkdm=N121603'
    req2 = s.get(req_url, headers=headers)

    soup = BeautifulSoup(req2.content,'lxml')
    value3=soup.find('input',id='__VIEWSTATE')['value']
    value4=soup.find('input',id='__EVENTVALIDATION')['value']
    payload1['__VIEWSTATE']=value3
    payload1['__EVENTVALIDATION']=value4
    pos = s.post(req_url, data=payload1, headers=headers)
    grades = pos.content.decode('gbk')
    
    return grades

def parser(id, grades):
    
    # 根据HTML网页字符串创建BeautifulSoup
    soup = BeautifulSoup(
        grades,  # HTML文档字符串
        'html.parser',  # HTML解析器
    )

    tables = soup.findAll('table')
    filename = '/home/fty/new-system/templates/score/'+ str(id) +'.html'
    #filename = '/home/fty/new-system/templates/score/'+ id +'.html'
    with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        tab = tables[0]
        list = [6, 10, 14, 16]
        f.write("{% extends 'student.html' %}")
        f.write('\n')
        f.write("{% block page_name %}成绩{% endblock %}")
        f.write('\n')
        f.write('{% block body_part2 %}')
        f.write('\n')
        f.write('<table>')
        for tr in tab.findAll('tr'):
            count = 0 
            f.write('<tr>')
            for td in tr.findAll('td'):
                count = count + 1
                if (count not in list):
                    f.write('<td>')
                    f.write('&ensp;')
                    f.write(td.getText().encode('utf-8'))
                    f.write('</td>')
            f.write('</tr>')
            f.write('\n')
        f.write('</table>')
        f.write('\n')
        f.write('{% endblock %}')
    





'''a = raw_input('学号：')
b = raw_input('密码：')
name = '付同永同学'
'''
# 将unicode编码编码成utf8
#getname = spider_login(a, b).encode('utf8')
# 将utf8解码成unicode
#name = name.decode('utf8')
