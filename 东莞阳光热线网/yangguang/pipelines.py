# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class YangguangPipeline(object):
    def process_item(self, item, spider):
        item["content_text"] = [i.replace("\xa0","").replace("\t","") for i in item["content_text"]]
        item["content_text"] = [i for i in item["content_text"] if len(i)>0]
        print(item)
        with open("yangguang.txt","a",encoding="utf-8") as f:
            f.write(json.dumps(dict(item),ensure_ascii=False))
        # return item
