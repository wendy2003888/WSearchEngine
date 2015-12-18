#-*- coding:utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from ir.spiders.spider import newsSpider,newsSpiderBing, IMDBSpider

process = CrawlerProcess()
process.crawl(newsSpider)
process.crawl(newsSpiderBing)
process.start() # the script will block here until all crawling jobs are finished