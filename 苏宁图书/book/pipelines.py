# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class BookPipeline(object):
    def open_spider(self,spider):
        client = MongoClient("127.0.0.1",27017)
        self.collection = client["book"]["suning"]
    def process_item(self, item, spider):
        self.collection.insert(item)
        return item
