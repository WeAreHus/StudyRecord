#-*-coding:utf-8-*-
from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests

from bs4 import BeautifulSoup

# 初始化机器人，扫码登陆
bot = Bot()
#bot = Bot(console_qr=2,cache_path="botoo.pkl")   　　　　#这里的二维码是用像素的形式打印出来！
headers = {
    'user-agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

def get_news1():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    contents = r.json()['content']
    translation= r.json()['translation']
    return contents,translation

def send_news():
    try:
        my_friend = bot.friends().search(u'哈鹏')[0]
        my_friend.send(get_news1()[0])
        my_friend.send(get_news1()[1][5:])
        my_friend.send(u"给你的心灵鸡汤！")
        t = Timer(86400, send_news)
        t.start()
    except:
        my_friend = bot.friends().search('向晋虎')[0] 
        my_friend.send(u"今天消息发送失败了")
            


            

if __name__ == "__main__":
    send_news()

