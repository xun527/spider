# -*- coding: utf-8 -*-
import scrapy
from myspider.items import MyspiderItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")[1:-1]
        print(tr_list,"*"*100)
        for tr in tr_list:
            item = {}
            item["position_name"] = tr.xpath("./td[1]/a/text()").extract_first()
            item["position_cate"] = tr.xpath("./td[2]/text()").extract_first()
            yield item
        #获取下一页的数据
        next_url = response.xpath("//a[@id='next']/@href").extract_first()
        next_url = "http://hr.tencent.com/"+next_url if next_url!="javascript:;" else None
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    # def parse1(self,response):
    #     pass