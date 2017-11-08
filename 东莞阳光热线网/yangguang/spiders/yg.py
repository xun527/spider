# -*- coding: utf-8 -*-
import scrapy
from yangguang.items import YangguangItem

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    def parse(self, response):
        tr_list = response.xpath("//div[@class='greyframe']/table[2]/tr/td/table/tr")
        for tr in tr_list:
            item = YangguangItem()  #实例化一个Itme
            item["num"] = tr.xpath("./td[1]/text()").extract_first()
            item["title"] = tr.xpath("./td[2]/a[2]/@title").extract_first()
            item["href"] = tr.xpath("./td[2]/a[2]/@href").extract_first()
            item["stats"] = tr.xpath("./td[3]/span/text()").extract_first()
            item["author_name"] = tr.xpath("./td[4]/text()").extract_first()
            yield scrapy.Request(  #发送关于详情页的请求
                item["href"],
                callback=self.parse_detail,
                meta={"item":item}  #meta携带参数，meta是个字典
            )
        #列表页的下一页的请求
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(  #发送请求
                next_url,  #url
                callback=self.parse  #解析函数指向自己
            )

    def parse_detail(self,response):
        item = response.meta["item"]  #使用resposne.meta接受前部分的item数据
        item["content_text"] = response.xpath("//div[@class='c1 text14_2']//text()").extract()
        item["content_img"] = response.xpath("//div[@class='c1 text14_2']//img/@src").extract()
        # print(item)
        yield item
