# -*-coding:utf-8-*-
import requests
import time
from bs4 import BeautifulSoup
from crypto_rsa.RSAJS import RSAKey
from crypto_rsa.base64 import Base64 as pB64
from crypto_rsa.safeInput import safeInput
import sys 
import json
reload(sys) 
sys.setdefaultencoding( "utf-8")



s = requests.Session()
ntime = int(time.time() * 1000)
indexUrl = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t={}".format(ntime)

headers = {
    'Origin': 'http://jwxt.hbnu.edu.cn',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': indexUrl,
    'Connection': 'keep-alive',
    'DNT': '1'
    }

def __getEnPassword(string, exponent, modulus):
    b64 = pB64()
    exponent = b64.b64_to_hex(exponent)
    modulus = b64.b64_to_hex(modulus)
	
    rsa = RSAKey()
    rsa.setPublic(modulus, exponent)
    crypto_t = rsa.encrypt(string)
    return b64.hex_to_b64(crypto_t)

def main(yhm,passwd):

    
    
    
    base_url = 'http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?time={0}'.format(ntime)

    index = s.get(base_url,headers = headers)
    index.encoding = 'utf-8'
    doc = index.text	
    soup = BeautifulSoup(doc,"html.parser")
    csrftoken = str(soup.find('input',id='csrftoken')['value'])


    publicKeyUrl = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time={}&_={}".format(ntime,ntime-10)
    modExp = s.get(publicKeyUrl).json()

    get_mm = __getEnPassword(passwd, modExp["exponent"], modExp["modulus"])
    data1 = [
    ('csrftoken',csrftoken),
    ('yhm',yhm),
    ('mm', get_mm),
    ('mm', get_mm)
    ]


    response = s.post(base_url,data=data1,headers =headers)
    html1 = response.content.decode('utf-8')
    #print(html1)
     
    print("欢迎进入教务成绩系统!")
    select = raw_input("请选择功能选项:(1.查成绩,2.查课表)")
    if select=="1":
        getgrades(yhm)
    elif select=="2":
        table()
    else:
        print("选择错误!")

def getgrades(yhm):
    #print(cook)
    #s = requests.session()
    #ctime = int(time.time() * 1000)
    xnm = str(raw_input("请输入学年:"))
    xqm = str(raw_input("请输入学期:"))
    if xqm == "2":
        xqm = "3"
    elif xqm == "1":
        xqm = "12"
    else:
        pass
    
    grades_url = "http://jwxt.hbnu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"
    data2 = {
	    'xnm': xnm,
        'xqm': xqm,
        '_search':'false',
        'nd': ntime,
        'queryModel.showCount':'15',
        'queryModel.currentPage':'1',
        'queryModel.sortName':'', 
        'queryModel.sortOrder':'asc',
        'time':'0'
    }
    grades = s.post(grades_url,data = data2,headers = headers)
    grades.encoding='utf8'
    html = str(grades.text)
    print(html)
    #html_data = str(grades.content.decode('utf-8'))
    #print(html_data)
    html = json.loads(html,encoding='utf8')
    #print(type(html))
    grade = html['items']
    print(grade)
    i = 1
    for  key in html['items']:
        print i,key['kcmc'],key['bfzcj'],key['xf'],key['jd']
        i = i + 1

def table():
    xnm = str(raw_input("请输入学年:"))
    xqm = str(raw_input("请输入学期:"))
    if xqm == "1":
        xqm = "3"
    elif xqm == "2":
        xqm = "12"
    else:
        pass
    table_url = "http://jwxt.hbnu.edu.cn/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"
    data3 = {
        'xnm': xnm,
        'xqm': xqm
    }
    tables = s.post(table_url,data = data3,headers = headers) 
    html2 = tables.content.decode('utf-8')
    with open('/home/cris/New-education-system/client/table.json','wb') as f:
        f.write(html2)
    #print(html2)
    html2 = json.loads(html2,encoding='utf8')
    i = 1
    for  key in html2['kbList']:
        print i,key['kcmc'],key['xqjmc'],key['jc'],key['zcd'],key['cdmc'],key['xm'],key['xqmc']
        i = i + 1
    
    
if __name__=="__main__":
    yhm = raw_input("请输入学号：")
    passwd = safeInput().getpass("请输入密码：")
    main(yhm,passwd)

