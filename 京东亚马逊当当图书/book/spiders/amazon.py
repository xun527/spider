# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider


class AmazonSpider(RedisCrawlSpider):
    name = 'amazon'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/%E5%9B%BE%E4%B9%A6/b/ref=sd_allcat_books_l1?ie=UTF8&node=658390051']
    redis_key = "amazon"
    rules = (
        # 能够匹配大分类的url地址和小分类的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='categoryRefinementsSection']/ul/li",)), follow=True),
        # 匹配图书的详情页的url地址
        Rule(LinkExtractor(restrict_xpaths=("//div[@id='mainResults']/ul/li//h2/..",)), callback="parse_book_detail")
    )

    def parse_book_detail(self, response):
        item = {}
        item["book_title"] = response.xpath("//span[contains(@id,'roductTitle')]/text()").extract_first()
        item["book_publish_date"] = response.xpath("//h1[@id='title']/span[last()]/text()").extract_first()
        item["book_author"] = response.xpath("//span[@class='author notFaded']/a/text()").extract()
        item["book_price"] = response.xpath("//span[text()='售价:']/following-sibling::*[1]/text()").extract_first()
        if item["book_price"] is None:
            item["book_price"] = response.xpath("//tr[@class='kindle-price']/td[2]/text()").extract_first()
        # item["book_img"] = response.xpath("//div[contains(@id,'img-canvas')]/img/@src").extract_first()
        item["book_press"] = response.xpath("//b[text()='出版社:']/../text()").extract_first()
        item["book_info"] = response.xpath("//ul[@class='zg_hrsr']/li[1]/span[2]/a/text()").extract()
        print(item)