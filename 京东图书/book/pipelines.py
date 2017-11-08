# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BookPipeline(object):
    def process_item(self, item, spider):
        item["book_name"] = item["book_name"].strip() if item["book_name"] is not None else None
        item["book_publish_date"] = item["book_publish_date"].strip() if item["book_publish_date"] is not None else None
        print(item)
        # return item
