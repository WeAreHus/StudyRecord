# -*-coding:utf-8-*-
import requests
import time
from bs4 import BeautifulSoup
from crypto_rsa.RSAJS import RSAKey
from crypto_rsa.base64 import Base64 as pB64
from crypto_rsa.safeInput import safeInput
import sys 
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
 
    html1 = str(response.content.decode('utf-8'))
    #print(html1)
    cook =  response.request.headers['Cookie']
    #print(cook)
    with open('/home/cris/New-education-system/client/inedx.html','wb') as f:
        f.write(html1)
    print("已获取成功!")
    getgrades(yhm)

def getgrades(yhm):
    #s = requests.session()
    #ctime = int(time.time() * 1000)
    """headers1 = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Host': 'jwxt.hbnu.edu.cn',
    'Origin': 'http://jwxt.hbnu.edu.cn',
    'Referer':'http://jwxt.hbnu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su={}'.format(yhm),
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }"""
    grades_url = "http://jwxt.hbnu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"
    data2 = {
	    'xnm': '2017',
        'xqm': '3',
        '_search':'false',
        'nd': ntime,
        'queryModel.showCount':'15',
        'queryModel.currentPage':'1',
        'queryModel.sortName':'', 
        'queryModel.sortOrder':'asc',
        'time':'0'
    }
    grades = s.post(grades_url,data = data2,headers = headers)
    #print(grades)
    html = grades.content.decode('utf-8')
    print(html)

    #with open('/home/cris/New-education-system/client/grades.json','wb') as f1:
    #    f1.write(html)
    #print("成绩保存成功!")


if __name__=="__main__":
    yhm = raw_input("请输入学号号：")
    passwd = safeInput().getpass("请输入密码：")
    main(yhm,passwd)

