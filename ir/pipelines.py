# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from store.storeHandler import storeItem, storeIMDB, storeIFENG

class mysqlPipeline(storeItem):
    def process_item(self, item, spider):
        if spider.name is 'movie':  
            self.store(item,spider)
        return item


class mysqlIMDBPipeline(storeIMDB):
    """docstring for mysqlIMDBPipeline"""
    def process_item(self, item, spider):
        if spider.name in ['coming_movie', 'top_movie']:
            self.store(item, spider)
        return item
        

class mysqlIfengPipeline(storeIFENG):
    """docstring for mysqlIMDBPipeline"""
    def process_item(self, item, spider):
        if spider.name in ['ifeng', 'Bing_news']:
            self.store(item, spider)
        return item