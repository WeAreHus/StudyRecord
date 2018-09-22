# -*-coding:utf-8-*-
import requests
import time
from bs4 import BeautifulSoup
from crypto_rsa.RSAJS import RSAKey
from crypto_rsa.base64 import Base64 as pB64
from crypto_rsa.safeInput import safeInput


class Core(object):
    def __init__(self, yhm="", passwd=""):
        self.yhm = yhm
        self.passwd = passwd
        self.loginStatus = False
        self.s = requests.session()

    def setLoginInfo(self, yhm, passwd):
         self.account = yhm
         self.password = passwd

    def __getEnPassword(self, string, exponent, modulus):
        b64 = pB64()
        exponent = b64.b64_to_hex(exponent)
        modulus = b64.b64_to_hex(modulus)

        rsa = RSAKey()
        rsa.setPublic(modulus, exponent)
        crypto_t = rsa.encrypt(string)
        return b64.hex_to_b64(crypto_t)

    def main(self):
        if self.yhm is "" or self.passwd is "":
            raise NameError("yhm or passwd is empty")
	s = requests.Session()
        ntime = int(time.time())
	#print(ntime)
        indexUrl = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t={}".format(ntime)
        #print(indexUrl)
        publicKeyUrl = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_getPublicKey.html?time={}&_={}".format(ntime,ntime-10)
        #print(publicKeyUrl)
        modExp = self.s.get(publicKeyUrl).json()
	base_url = "http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html?time={}".format(ntime)
        #print(base_url)

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
        
        
        index = s.get(indexUrl,headers = headers)
        html = index.content.decode('utf-8')
        soup = BeautifulSoup(html,"html.parser")
        value1 = soup.find('input',id='csrftoken')['value']
        csrftoken = value1
	get_mm = self.__getEnPassword(self.passwd, modExp["exponent"], modExp["modulus"])

        data = [
        ('csrftoken',csrftoken),
        ('yhm',self.yhm),
        ('mm', get_mm),
        ('mm', get_mm)
        ]
	#print(csrftoken)
        #print(self.yhm)
	#print(get_mm)

        response = self.s.post('http://jwxt.hbnu.edu.cn/jwglxt/xtgl/login_slogin.html',headers=headers,data=data)
        html1 = response.content.decode('utf-8')
        print(html1)


if __name__=="__main__":
    yhm = raw_input("输入帐号：")
    pa = safeInput()
    passwd = pa.getpass("请输入密码：")
    #print(passwd)
    client = Core(yhm, passwd)
    client.main()

