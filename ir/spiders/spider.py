#-*- coding:utf-8 -*-

import re, time
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import json

from ir.items import irItem, imdbItem, ifengItem

def get_time():
  return  time.strftime('%Y-%m-%d %H:%M')

class movieSpider(scrapy.spiders.Spider):
    name = "movie"
    allowed_domains = ["piaohua.com"]
    start_urls = [
        "http://www.piaohua.com/"
    ]

    fields = {u'译名' : 'chname',
    u'片名' : 'orgname',
    u'年代' : 'year',
    u'国家' : 'country',
    u'评分' : 'imdbScor',
    u'链接' : 'imdbUrl',
    u'豆瓣评分' : 'doubanScor',
    u'豆瓣链接' : 'doubanUrl',
    u'大小' : 'size'}
    

    def parse(self, response):

        for info in response.xpath("//div[@id='iml']/ul/li"):
            item_url = info.xpath('.//a[1]/@href').extract()
            item = irItem()
            item['url'] = self.start_urls[0] + item_url[0]
            yield scrapy.Request(item['url'], self.parse_item, meta = {'item' : item})
 
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        info =  sel.xpath("//div[@id='showinfo']")

        for data in info.xpath(".//div/text()"):
            string = "".join(data.extract().split())
            for key, value in self.fields.items():
                if key in  string:
                    pattern = re.compile('.*?' + key)
                    result = re.sub(pattern, '', string)
                    item[value] = result
                    break
            # print string
        return item


class IMDBTOPSpider(scrapy.spiders.Spider):
    name = "top_movie"
    allowed_domains = ["imdb.com"]
    start_urls = [
        "http://www.imdb.com/chart/top?ref_=ft_250"
    ]

    homepage = 'http://www.imdb.com'
    

    def parse(self, response):
        for info in response.xpath("//td[@class='titleColumn']/a"):
            # print info.extract()
            item = imdbItem()
            item_url = info.xpath('.//@href').extract()
            item['orgname'] = info.xpath('.//text()').extract()[0]
            item['url'] = self.homepage + item_url[0]
            yield scrapy.Request(item['url'], self.parse_item, meta = {'item' : item})   
 
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        rating = sel.xpath("//span[@itemprop='ratingValue']/text()").extract()
        dspt = sel.xpath("//p[@itemprop='description']/text()").extract()
        storyline = sel.xpath("//div[@id='titleStoryLine']/div[@itemprop='description']/p/text()").extract()
        country = sel.xpath("//div[@id='titleDetails']/div/h4[text()='Country:']/following-sibling::*/text()").extract()
        if rating:
            item['imdbScor'] = rating[0]
        if dspt:
            item['description'] = dspt[0]
        item['storyline'] = storyline[0].lstrip().rstrip()
        item['country'] = country[0]
        return item

class IMDBSpider(scrapy.spiders.Spider):
    name = "coming_movie"
    allowed_domains = ["imdb.com"]
    start_urls = [
        "http://www.imdb.com/movies-coming-soon/2015-12/",
        "http://www.imdb.com/movies-coming-soon/2016-01/",
        "http://www.imdb.com/movies-coming-soon/2016-02/",
        "http://www.imdb.com/movies-coming-soon/2016-03/",
        "http://www.imdb.com/movies-coming-soon/2016-04/",
        "http://www.imdb.com/movies-coming-soon/2016-05/",
        "http://www.imdb.com/movies-coming-soon/2016-06/",
        "http://www.imdb.com/movies-coming-soon/2016-07/"
    ]

    homepage = 'http://www.imdb.com'


    

    def parse(self, response):
        for info in response.xpath("//div[@class='list detail']/div/table/tbody/tr/td[@class='overview-top']/h4/a"):
            item = imdbItem()
            item_url = info.xpath('.//@href').extract()
            item['orgname'] = info.xpath('.//text()').extract()[0]
            item['url'] = self.homepage + item_url[0]
            yield scrapy.Request(item['url'], self.parse_item, meta = {'item' : item})   
 
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        top =  sel.xpath("//td[@id='overview-top']")
        rating = top.xpath("./div[@id='star-box giga-star']/div[@class='star-box-details']/strong/span[@itemprop='ratingValue']/text()").extract()
        # rating = top.xpath("./div[@id='star-box giga-star']/div[@class='star-box-details']").extract()
        dspt = top.xpath("./p[@itemprop='description']/text()").extract()
        storyline = sel.xpath("//div[@id='titleStoryLine']/div[@itemprop='description']/p/text()").extract()
        country = sel.xpath("//div[@id='titleDetails']/div/h4[text()='Country:']/following-sibling::*/text()").extract()
        if rating:
            item['imdbScor'] = rating[0]
        if dspt:
            item['description'] = dspt[0]
        item['storyline'] = storyline[0].rstrip()
        item['country'] = country[0]
        return item

class newsSpider(scrapy.spiders.Spider):
    name = "ifeng"
    allowed_domains = ["news.ifeng.com"]
    start_urls = [
        "http://news.ifeng.com/mainland/",
        "http://news.ifeng.com/world/index.shtml",
        "http://news.ifeng.com/taiwan/index.shtml",
        "http://news.ifeng.com/hongkong/index.shtml",
        "http://news.ifeng.com/society/index.shtml"
    ]

    # "http://www.bttiantang.com/",
    #     "http://bt.neu6.edu.cn/forum-13-1.html",   "bttiantang.com", "neu6.edu.cn"
    

    def parse(self, response):
        for info in response.xpath("//div[@class='juti_list']/h3/a"):
            # print info.extract()
            item = ifengItem()
            item_url = info.xpath('.//@href').extract()
            item['title'] = info.xpath('.//text()').extract()[0]
            item['url'] = item_url[0]
            print item['url']
            yield scrapy.Request(item['url'], self.parse_item, meta = {'item' : item})   
 
    def parse_item(self, response):
        item = response.meta['item']
        sel = Selector(response)
        top =  sel.xpath("//p[@class='p_time']")
        date = top.xpath("./span[@itemprop='datePublished']/text()").extract()
        o = top.xpath("./span[@itemprop='publisher']/span/a/@href").extract()
        detail = sel.xpath("//div[@id='main_content']/p/text()").extract()
        item['date'] = date[0]
        if o:
            item['orgUrl'] = o[0]
        item['content'] = detail
        return item


class newsSpiderBing(scrapy.spiders.Spider):
    name = "Bing_news"
    allowed_domains = ["global.bing.com"]
    start_urls = [
        "http://www.bing.com/news?q=world+news&FORM=NSBABR"
    ]
    

    def parse(self, response):
        for info in response.xpath("//div[@class='newstitle']/a"):
            # print info.extract()
            item = ifengItem()
            item_url = info.xpath('.//@href').extract()
            item['title'] = info.xpath('.//text()').extract()[0]
            item['url'] = item_url[0]
            detail =  response.xpath("//span[@class='sn_snip']/text()").extract()[0]
            date = response.xpath("//span[@class='sn_tm tm_fre']/text()").extract()[0]
            date = date.split(' ')
            t = list(get_time())
            if date[1] == 'minutes':
                t[14:] = str(int(''.join(t[14:])) - int(date[0]))
            elif date[1] == 'hours':
                t[11:13] = str(int(''.join(t[11:13])) - int(date[0]))
            item['date'] = ''.join(t)
            item['content'] = detail
            yield item
