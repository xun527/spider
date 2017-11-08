# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CsdnSpdierSpider(CrawlSpider):
    name = 'csdn_spdier'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['http://blog.csdn.net/hbblzjy']

    rules = (
        #提取专家的博客地址
        Rule(LinkExtractor(allow=r'blog.csdn.net/\w+$'), follow=True),
        #提取博客详情页的地址
        Rule(LinkExtractor(allow=r'/\w+/article/details/\d+$'),callback="parse_item"),
        #提取专家翻页地址
        Rule(LinkExtractor(allow=r'channelid=\d+&page=\d+$'), follow=True),
        #提取博客列表页翻页
        Rule(LinkExtractor(allow=r'/\w+/article/list/\d+$'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item["title"] = response.xpath("//h1/text()").extract_first()
        item['update_time'] = response.xpath("//span[@class='time']/text()").extract_first()
        item["tag"] = response.xpath("//ul[@class='article_tags clearfix csdn-tracking-statistics']//text()").extract()
        # item["content"] = response.xpath("//div[@id='article_content']")
        # print(item)
        yield item
