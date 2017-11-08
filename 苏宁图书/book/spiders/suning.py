# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy

class SuningSpider(scrapy.Spider):
    name = 'suning'
    allowed_domains = ['suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):  #提取大小分类
        print(response.request.headers["User-Agent"])
        li_list = response.xpath("//ul[@class='ulwrap']/li")
        for li in li_list:
            item = {}
            item["b_cate"]=li.xpath("./div[1]/a/text()").extract_first()
            a_list = li.xpath("./div[2]/a")
            for a in a_list:
                item["s_cate"] = a.xpath("./text()").extract_first()
                item["s_href"] = "http://snbook.suning.com/"+a.xpath("./@href").extract_first()
                yield scrapy.Request( #发送图书列表页的请求
                    item["s_href"],
                    callback=self.parse_book_list,
                    meta={"item":deepcopy(item)} #重新开辟空间存储赋值之后的item，让下一次的循环的赋值不会影响到前一次
                )
                # print(item)

    def parse_book_list(self,response): #图书列表页
        print(response.request.headers["User-Agent"])
        item = deepcopy(response.meta["item"])
        li_list =response.xpath("//div[@class='filtrate-books list-filtrate-books']/ul/li")
        for li in li_list:
            item["book_img"] = li.xpath("./div[@class='book-img']//img/@src").extract_first()
            item["book_title"] = li.xpath(".//div[@class='book-title']/a/@title").extract_first()
            item["book_publish"] = li.xpath(".//div[@class='book-publish']/a/text()").extract_first()
            item["book_desc"] = li.xpath(".//div[@class='book-descrip c6']/text()").extract_first()
            item["book_href"] = li.xpath("./div[@class='book-img']/a/@href").extract_first()
            yield scrapy.Request(  #发送详情页的请求
                item["book_href"],
                callback=self.parse_book_detail,
                meta={"item":deepcopy(item)}
            )
        #方法一，翻页
        # if len(li_list)>0: #存在书在页面上
        #     ret = re.findall("pageNumber=(.*?)&sort=0",response.request.url)
        #     if len(ret)==0:
        #         next_url = item["s_href"] + "?pageNumber=2&sort=0"
        #     else:
        #         next_url = item["s_href"] + "?pageNumber={}&sort=0".format(int(ret[0])+1)
        #     yield scrapy.Request(
        #         next_url,
        #         callback=self.parse_book_list,
        #         meta={"item":response.meta["item"]}
        #     )
        #方法二：
        total_page =re.findall("var pagecount=(.*?);",response.body.decode())[0]
        current_page = re.findall("var currentPage=(.*?);",response.body.decode())[0]
        if current_page<=total_page:
            next_url = item["s_href"] + "?pageNumber={}&sort=0".format(int(current_page)+1)
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list,
                meta={"item":response.meta["item"]}
            )



    def parse_book_detail(self,response): #图书详情页
        print(response.request.headers["User-Agent"])
        item = response.meta["item"]
        ret = re.findall(r"\"bp\":'(.*?)',",response.body.decode(),re.S)

        # print(item)
        # yield item
