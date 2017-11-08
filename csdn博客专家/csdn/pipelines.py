# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

class CsdnPipeline(object):
    def process_item(self, item, spider):
        item["tag"] = [re.sub(r"\s+|/","",i,re.S) for i in item["tag"]]
        item["tag"] =[i for i in item["tag"] if len(i)>0 and i!='标签：']
        print(item)
        # return item
