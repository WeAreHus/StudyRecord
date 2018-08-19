#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
from example.items import ExampleItem,Nexturl,third,fourth
#from illness.items import SickItem
headers = {
    'Referer': 'http://jwgl1.hbnu.edu.cn/(S(dbawgs45zpzce455l3uuyhia))/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }
class EduSpider(scrapy.Spider):
    name = 'urls'
    allowed_domains = ['hbnu.edu.cn']
    start_urls = ['http://www.hbnu.edu.cn/']

    def parse(self, response):
         
         sel = Selector(response)
         sites = sel.xpath('/html/body/div[4]/div/div[2]/div[1]/ul/li')
         #url = 'http://www.hbnu.edu.cn/'
         item = ExampleItem()
         url=[]
         item['title'] = '一级链接' 
         for site in sites:
             item['url'] = site.xpath('a/@href').extract()
             url.append(item)
             yield(item)
         #print(url[2]['url'])
         yield scrapy.Request(url[2]['url'][0], callback=self.next) 

    def next(self, response):
        head='http://www.news.hbnu.edu.cn/'
        item = Nexturl()
        url1 = []
        item['title2'] = '二级链接' 
        sel = Selector(response)
        #sites = sel.xpath('/html/body/div[1]/div[3]/div[1]/p[4]/span/text()').extract()
    # item['book'] = sites
        sites1 = sel.xpath('/html/body/div[1]/div[2]/ul/li[8]')
            #print(url.xpath('a/@href'))
        item['url1'] = sites1.xpath('a/@href').extract()
        #url1.append(item)
            #print(url1[2]['url1'][0])
        yield(item)
           # print(url1[2]['url1'][0])
        #print(item['url1'][0])
        url = head + item['url1'][0]
        yield scrapy.Request(url, callback=self.next2)
    

    def next2(self, response):
        head='http://www.news.hbnu.edu.cn/'
        sel = Selector(response)
        sites = sel.xpath('/html/body/div/div[3]/div[2]/div[2]/ul/li[1]')
        item = third()
        #url2 = []
        #for url in sites:
        item['url2'] = sites.xpath('a/@href').extract()
        yield(item)
        url = head + item['url2'][0]
        yield scrapy.Request(url,callback=self.next3)
    
    def next3(self,response):
        head='http://www.news.hbnu.edu.cn/'
        sel = Selector(response)
        sites = sel.xpath('/html/body/div[1]/div[3]/div[2]/div[2]/ul/li[3]')
        item = fourth()
        hurl = sites.xpath('a/@href').extract()
        #item['url3'] = sites.xpath('a/@href').extract()
        item['url3'] = head + hurl[0]
        yield(item)
      


 

