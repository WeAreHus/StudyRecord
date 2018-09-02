# -*-coding:utf-8-*-
import os
import pdb
import urllib2

import requests
from bs4 import BeautifulSoup
from lxml import etree
from PIL import Image
from ZFCheckCode import recognizer, trainner

from models import Score, Student, Subject, db

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Referer': 'http://jwgl1.hbnu.edu.cn/(S(nxuiogv1kq4coqvvhltax145))/default2.aspx?'
}

baseurl = 'http://jwgl1.hbnu.edu.cn'
s = requests.Session()
html = s.get(baseurl, headers=headers, allow_redirects=False)
loc = html.headers['location']
loginurl = baseurl + loc
codeu = loginurl[0:54]
codeurl = codeu + '/CheckCode.aspx?'

# 获取验证码并自动识别


def checkcode():
    img = s.get(codeurl, stream=True, headers=headers)
    with open('checkcode.gif', 'wb') as f:
        f.write(img.content)
    code = recognizer.recognize_checkcode('/home/fty/new-system/checkcode.gif')
    # print(code)
    return code

# 模拟登陆
def spider_login(id, passwd):
    # 构造表单字典
    payload = {'__VIEWSTATE': '',
               'txtUserName': '',
               'Textbox1': '',
               'TextBox2': '',
               'txtSecretCode': '',
               'RadioButtonList1': '',
               'Button1': '',
               'lbLanguage': '',
               'hidPdrs': '',
               'hidsc': '',
               '__EVENTVALIDATION': '',
               }

    # 获取表单字典数据
    index = s.get(loginurl, headers=headers)
    soup = BeautifulSoup(index.content, 'lxml')
    value1 = soup.find('input', id='__VIEWSTATE')['value']
    value2 = soup.find('input', id='__EVENTVALIDATION')['value']
    payload['txtUserName'] = id
    payload['TextBox2'] = passwd
    code = checkcode()
    payload['txtSecretCode'] = code
    payload['RadioButtonList1'] = u"学生".encode('gb2312', 'replace')
    payload['__VIEWSTATE'] = value1
    payload['__EVENTVALIDATION'] = value2
    payload['RadioButtonList1'] = '%D1%A7%C9%FA'

    loginresponse = s.post(loginurl, data=payload, headers=headers)
    content = loginresponse.content.decode('gb2312')
    soup = BeautifulSoup(content, 'lxml')
    uname = soup.find('span', id='xhxm')
    xsxm = uname.text

    # 返回学生姓名
    return xsxm

# 获取成绩


def getgrades(id, name):

    payload1 = {'__VIEWSTATE': '',
                'ddlXN': '',
                'ddlXQ': '',
                'Button1': '',
                '__EVENTVALIDATION': '',

                }
    #url2 = spider_login(id, passwd)
    name = name[0:9]
    cname = urllib2.quote(name.encode('gb2312'))
    xingming = urllib2.quote(cname)

    req_url = codeu + '/xscj_gc.aspx?xh=' + \
        str(id) + '&xm=' + xingming + '&gnmkdm=N121603'
    req2 = s.get(req_url, headers=headers)

    soup = BeautifulSoup(req2.content, 'lxml')
    value3 = soup.find('input', id='__VIEWSTATE')['value']
    value4 = soup.find('input', id='__EVENTVALIDATION')['value']
    payload1['__VIEWSTATE'] = value3
    payload1['__EVENTVALIDATION'] = value4
    pos = s.post(req_url, data=payload1, headers=headers)
    grades = pos.content.decode('gbk')

    return grades

# 获取课程表


def get_timetable(id, name, year, term):

    payload2 = {'__EVENTTARGET': 'xqd',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VIEWSTATE': '',
                'xnd': '',
                'xqd': '',
                '__EVENTVALIDATION': ''
                }
    name = name[0:9]
    cname = urllib2.quote(name.encode('gb2312'))
    xingming = urllib2.quote(cname)

    kbcx_url = codeu + '/xskbcx.aspx?xh=' + \
        str(id)+'&xm='+xingming+'&gnmkdm=N121603'
    kbcx = s.get(kbcx_url, headers=headers)

    soup_kb = BeautifulSoup(kbcx.content, 'lxml')
    value5 = soup_kb.find('input', id='__VIEWSTATE')['value']
    value6 = soup_kb.find('input', id='__EVENTVALIDATION')['value']

    payload2['__VIEWSTATE'] = value5
    payload2['xnd'] = year
    payload2['xqd'] = term
    payload2['__EVENTVALIDATION'] = value6

    kbcx_response = s.post(kbcx_url, data=payload2, headers=headers)
    timetable = kbcx_response.content.decode('gbk')

    return timetable

# 成绩解析


def parser(stu_id, html):
    # 根据HTML网页字符串创建BeautifulSoup
    soup = BeautifulSoup(
        html,  # HTML文档字符串
        'html.parser',  # HTML解析器
    )
    stu = Student.query.filter(Student.id == stu_id).first()
    tables = soup.findAll('table')
    tab = tables[0]
    count = 1
    lists = []
    for tr in tab.findAll('tr'):
        if count != 1:
            td = tr.findAll('td')
            for text in td:
                score = text.getText().strip()
                if score == '':
                    score = None
                lists.append(score)
            # 判断课程是否已存在于Subject表中
            sub_obj = Subject.query.filter(Subject.class_name==lists[3]).first()
            # 不存在则新插入该课程
            if sub_obj == None:
                sub = Subject(lists[0], lists[1], lists[2], lists[3], lists[4],
                            lists[6], lists[5], lists[9], lists[12], lists[14], lists[15])
                db.session.add(sub)
                db.session.commit()
            # 判断学生没有拥有该课程
            if sub_obj not in stu.subject:
                sub = Subject.query.filter(Subject.class_name==lists[3]).first()
                stu.subject.append(sub)
                db.session.add(stu)
                sub = Subject.query.filter(Subject.class_name == lists[3]).first()
                score = Score(lists[8], lists[7], sub.id,stu_id, lists[10], lists[11], lists[13])
                db.session.add(score)
                db.session.commit()
            # 如果拥有该课程，则更新数据
            else:
                for cla in stu.subject:
                    if cla == sub_obj:
                        cla.score[0].score = lists[8]
                        cla.score[0].GPA = lists[7]
                        cla.score[0].resit_score = lists[10]
                        cla.score[0].restudy_score = lists[11]
                        cla.score[0].note = lists[13]
                        cla.minor_tab = lists[9]
                        cla.resit_tab = lists[14]
                        db.session.commit()
                        break
            lists = []
        count = count + 1
        
# 解析课程表


def parser_timetable(timetable):
    soup = BeautifulSoup(
        timetable,
        'html.parser',
    )
    html = '''
 {% extends 'base.html' %} {% block page_name %}成绩{% endblock %} {% block body_part5 %}
<a href="{{ url_for('timetable') }}" class="nav-link active">
    {% endblock %}
    {% block body_part1 %}
    <span class="glyphicon glyphicon-calendar"></span>&ensp;要认真听课哦 ⊙0⊙
    {% endblock %}
    {% block body_part2 %}
    <form method="POST">
        学年：
        <select name=year class="form-control selectpicker" style="width: 13%; height: 35px; font-size: 16px; margin-top:-32px; margin-left:50px;">
            {% if year == '2016-2017' %}
            <option selected="selected" value="2016-2017">2016-2017</option>
            {% else %}
            <option value="2016-2017">2016-2017</option>
            {% endif %} {% if year == '2017-2018' %}
            <option selected="selected" value="2017-2018">2017-2018</option>
            {% else %}
            <option value="2017-2018">2017-2018</option>
            {% endif %}</select>
        </span>
        <span>
            <p style="margin-top:-28px; margin-left:253px;">学期:</p>
            <select name=term class="form-control selectpicker" style="width: 10%; height: 35px; font-size: 16px; margin-top:-50px; margin-left:302px;">
                {% if term == '1' %}
                <option selected="selected" value="1">1</option>
                {% else %}
                <option value="1">1</option>
                {% endif %} {% if term == '2' %}
                <option selected="selected" value="2">2</option>
                {% else %}
                <option value="2">2</option>
                {% endif %}
            </select>
            <span>
                <button type="submit" class="btn btn-success" style="margin-top:-60px; margin-left:465px;width: 8%;height: 45px;">
                    <span class="glyphicon glyphicon-search"></span>&ensp;查询
                </button>
            </span>
    </form>
    <table class="table table-bordered table-hover table-condensed">
        <tr class="info">
            <td align=center colspan="16">{{year}}学年第{{term}}学期学生个人课表</td>
        </tr>
        <tr class="info">
            <td align=center colspan="16">
    '''
    
    with open('/home/fty/new-system/templates/time_table.html', 'w') as f:
        f.write(html)
        tables = soup.find_all('table')
        td = tables[0].find_all('td')
        span = td[1].find_all('span')
        for sp in span:
            f.write(str(sp))
            f.write('&ensp;')
            f.write('\n')
        f.write('</td></tr>')
        tr = tables[1].find_all('tr')
        f.write('')
        for tr in tr:
            f.write(str(tr))
            f.write('\n')
        f.write('</table>\n')
        f.write('{% endblock %}')
