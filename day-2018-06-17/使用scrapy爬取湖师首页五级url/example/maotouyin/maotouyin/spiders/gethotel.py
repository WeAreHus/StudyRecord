#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
from maotouyin.items import MaotouyinItem,hotel


class HotelSpider(scrapy.Spider):
    name = 'hurl'
    allowed_domains = ['tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/']

    def firsturl(self, response):
         sel = Selector(response)
         sites = sel.xpath('//*[@id="popularDestinations"]/div[1]/ul[2]/li[1]/ul/li[1]')
         item = MaotouyinItem()
         url = []
         item['Furl'] = sites.xpath('a/@href').extract()
         url.append(item)
         #yield(item)
         yield scrapy.Request(url[0]['Furl'], callback=self.nexturl)

    def nexturl(self, response):
        sel =  Selector(response)
        sites = sel.xpath('//*[@id="HTL_FAVS"]/li[1]/div')
        item = hotel()
        item['Surl'] = sites.xpath('a/@href').extract()
        yield(item)
    '''
    def Thirdurl(self, response):
        sel = Selector(response)
       # sites = sel.xpath('')

'''

'''
//*[@id="HTL_FAVS"]/li[1]/div
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
'''
