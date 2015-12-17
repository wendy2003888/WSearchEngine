# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class irItem(scrapy.Item):
    # define the fields for your item here:
    chname = scrapy.Field()     #译名
    orgname = scrapy.Field()     #片名
    year = scrapy.Field()       #年代
    country = scrapy.Field()    #国家
    imdbScor = scrapy.Field()   #imdb评分
    imdbUrl = scrapy.Field()    #imdb链接
    doubanScor = scrapy.Field() #豆瓣评分
    doubanUrl = scrapy.Field()  #豆瓣链接
    size = scrapy.Field()       #大小
    url = scrapy.Field()        #下载链接

class imdbItem(scrapy.Item):
    # define the fields for your item here:
    orgname = scrapy.Field()     #片名
    year = scrapy.Field()       #年代
    country = scrapy.Field()    #国家
    imdbScor = scrapy.Field()   #imdb评分
    description = scrapy.Field()
    storyline = scrapy.Field()       #简介
    url = scrapy.Field()        #链接


class ifengItem(scrapy.Item):
    # define the fields for your item here:
    title = scrapy.Field()     #标题
    date = scrapy.Field()       #时间
    content = scrapy.Field()    #内容
    url = scrapy.Field()        #链接
    orgUrl = scrapy.Field()     #来源