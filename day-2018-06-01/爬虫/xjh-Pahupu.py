import requests
from lxml import etree
from bs4 import BeautifulSoup
#from pymongo import MongoClient

headers = {
    
    "Referer": "https://www.baidu.com/link?url=ZvxrKZu1fQYDIeO6HirlmNQg7uwcVmT4vKoLI6bZOnC&wd=&eqid=d01453b200009677000000025b1767e2",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}


r = requests.get('https://nba.hupu.com', headers=headers)
    
soup = BeautifulSoup(r.content, 'html.parser')
#print(soup)
list = soup.find_all('div', class_='nba-latestNews')
#print (list)
dict = []
t1 = list[0].find_all('a')
for t2 in t1:
    t3 = t2.get('href')
    print(t3)
    dict.append(t3)
    
for url in dict:
    r = requests.get(url, headers=headers)
    r.encoding=r.apparent_encoding
   # print r.text
    n1 = etree.HTML(r.text)
    n2 = n1.xpath('/html/body/div[4]/div[1]/div[2]/div/div[2]/p[1]/text()')
    print(n2)

    '''
    soup = BeautifulSoup(r.content, 'html.parser')
    test = soup.find_all('div', class_='artical-content')
    print(test)
    b1 = test[0].find_all('div', class_='artical-main-content')
    
    b2 = b1[0].find_all('p').text
    print (b2)

    

list = soup.find_all('div', class_='nba-latestNews')

for news in list:
    title = news.find('ul', class_ ='item-list news-item').text
    print(title)

/html/body/div[4]/div[1]/div[2]/div/div[2]/p[1]
/html/body/div[4]/div[1]/div[2]/div/div[2]/p[1]
'''