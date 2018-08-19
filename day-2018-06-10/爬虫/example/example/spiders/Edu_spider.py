#-*-coding:utf-8-*-
import scrapy
from scrapy.selector import Selector
from example.items import ExampleItem,Nexturl
#from illness.items import SickItem

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
        item['title2'] = '二级链接' 
        sel = Selector(response)
        sites = sel.xpath('/html/body/div[1]/div[3]/div[1]/p[4]/span/text()').extract()
        item['book'] = sites
        sites1 = sel.xpath('/html/body/div[1]/div[3]/div[1]/ul[2]/li')
        for url in sites1:
            #print(url.xpath('a/@href'))
            item['url1'] = url.xpath('a/@href').extract()
            yield(item)

 

'''
class DmozSpider(scrapy.spiders.Spider):
    name = "dmoz0" //爬虫名称，在每次调用爬虫时需要
    allowed_domains = ["www.tianqihoubao.com"] //注意这里非常重要，它定义整个搜索的范围，既往下的任何搜索都在这个域名的范围内，注：不是链接！
    start_urls = [
        "https://www.tianqihoubao.com/aqi/"
    ]            //这一部分设定起始url
 
    def parse(self, response):   //scrapy框架默认传入parse
        sel = Selector(response)
        sites = sel.xpath('//dl')
        url = "https://www.tianqihoubao.com"
        items = []
        for site in sites:
            provence = site.xpath('dt/b/text()').extract()
            print(provence)
            citys = site.xpath('dd/a')
            for city in citys:
                name = city.xpath('text()').extract()
                cityurl = city.xpath('@href').extract()
                cl = url + cityurl[0]
                item = CityItem()
                item['name'] = name
                item['url'] =url + cityurl[0]
                items.append(item)
                yield scrapy.Request(cl, callback=self.parse_item)     //yield生成请求，将新的url加入到爬取队列中，cl为url，callback为新的爬取调用的parse名称，这个项目新定义的为parse_item。
                print("000")

    def parse_item(self, response): 
         sell = Selector(response)
         sites = sell.xpath('//h2')
         print("999")
         '''