# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import  RedisSpider
from copy import deepcopy

class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://book.dangdang.com/']
    redis_key = "dangdang"

    def parse(self, response):
        div_list = response.xpath("//div[@class='con flq_body']/div")
        # print(len(div_list),"("*100)
        for div in div_list:#大分类
            item = {}
            item["b_cate"] = div.xpath("./dl/dt//text()").extract()
            #中间分类
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            # print(len(dl_list),")"*100)
            for dl in dl_list:
                item["m_cate"] = dl.xpath("./dt/a/text()").extract_first()
                #获取小分类
                a_list = dl.xpath("./dd/a")
                # print("-"*100,len(a_list))
                for a in a_list:
                    item["s_cate"] = a.xpath("./@title").extract_first()
                    item["s_href"] = a.xpath("./@href").extract_first()
                    if item["s_href"] is not None:
                        yield scrapy.Request(  #发送图书列表页的请求
                            item["s_href"],
                            callback=self.parse_book_list,
                            meta = {"item":deepcopy(item)}
                        )

    def parse_book_list(self,response):
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_title"] = li.xpath("./a/@title").extract_first()
            item["book_href"] = li.xpath("./a/@href").extract_first()
            item["book_detail"] = li.xpath("./p[@class='detail']/text()").extract_first()
            item["book_price"] = li.xpath(".//span[@class='search_now_price']/text()").extract_first()
            item["book_author"] = li.xpath("./p[@class='search_book_author']/span[1]/a/@title").extract_first()
            item["book_publish_date"] = li.xpath("./p[@class='search_book_author']/span[2]/text()").extract_first()
            item["book_press"] = li.xpath("./p[@class='search_book_author']/span[3]/a/@title").extract_first()
            print(item)


