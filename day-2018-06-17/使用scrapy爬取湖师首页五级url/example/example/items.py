# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


class ExampleItem(scrapy.Item):
    url = Field()
    title = Field()

class Nexturl(scrapy.Item):
    url1 = Field()
    book = Field()
    title2 = Field()

class third(scrapy.Item):
    url2 = Field()
    title3 = Field()

class fourth(scrapy.Item):
    url3 = Field()