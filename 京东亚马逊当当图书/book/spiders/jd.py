# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import json

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://book.jd.com/booksort.html']

    def parse(self, response):
        #大分类
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item["b_cate"] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            #小分类
            for em in em_list:
                item["s_cate"] = em.xpath("./a/text()").extract_first()
                item["s_href"]= em.xpath("./a/@href").extract_first()
                if item["s_href"] is not None:
                    item["s_href"] = "https:"+item["s_href"]
                    yield  scrapy.Request(
                        item["s_href"],
                        callback=self.parse_book_list,
                        meta = {"item":deepcopy(item)}
                    )
    #图书的列表页
    def parse_book_list(self,response):
        item = deepcopy(response.meta["item"])
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item["book_href"] = li.xpath(".//div[@class='p-img']/a/@href").extract_first()
            item["book_href"] = "http:" + item["book_href"] if item["book_href"] is not None else None
            item["book_img"] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item["book_img"] is None:
                item["book_img"] = li.xpath(".//div[@class='p-img']//img/@data-lazy-img").extract_first()
            item["book_img"] = "http:" + item["book_img"] if item["book_img"] is not None else None
            item["book_name"] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first()
            item["book_author"] = li.xpath(".//span[@class='p-bi-name']/span/a/text()").extract()
            item["book_press"] = li.xpath(".//span[@class='p-bi-store']/a/text()").extract_first()
            item["book_publish_date"] = li.xpath(".//span[@class='p-bi-date']/text()").extract_first()
            item["book_sku"] = li.xpath("./div/@data-sku").extract_first()
            if item["book_sku"] is not None:
                item["book_price_url"] = "https://p.3.cn/prices/mgets?skuIds=J_{}".format(item["book_sku"])
                yield scrapy.Request(  #发送关于价格的请求
                    item["book_price_url"],
                    callback=self.parse_book_price,
                    meta={"item":deepcopy(item)}
                )
        #下一页
        next_url_temp = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url_temp is not None:
            next_url  = "https://list.jd.com"+next_url_temp
            yield  scrapy.Request(
                next_url,
                callback=self.parse_book_list,#列表页的数据解析调用自己
                meta={"item":response.meta["item"]}
            )
    #获取价格
    def parse_book_price(self,response):
        item = response.meta["item"]
        dict_resposne = json.loads(response.body.decode())
        item["book_price"] = dict_resposne[0].get("op",None) if len(dict_resposne)>0 else None
        # print(item)
        yield item


