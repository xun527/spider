# coding=utf-8
import requests
from lxml import etree

class TiebaSpider:
    def __init__(self,tieba_name):
        self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw="+tieba_name+"&lp=7202"
        self.headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        self.part_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/"

    def parse_url(self,url): #2.发送请求，获取响应
        print(url)
        r = requests.get(url,headers=self.headers)
        return r.content

    def get_content_list(self,html_str):#3。1.获取列表页的标题和url地址
        # print(html_str)
        html = etree.HTML(html_str)
        div_list = html.xpath("//div[contains(@class,'i')]")
        content_list = []
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()"))>0 else None
            item["href"] = self.part_url+div.xpath("./a/@href")[0] if len(div.xpath("./a/@href"))>0 else None
            item["img_list"] = self.get_img_list(item["href"],[],item["title"])
            content_list.append(item)

        #获取第二页的url地址
        next_url_temp = html.xpath("//a[text()='下一页']/@href")
        if len(next_url_temp)>0:
            next_url = self.part_url + next_url_temp[0]
        else:
            next_url = None
        return content_list,next_url

    def get_img_list(self,detail_url,total_img_list,title): #detail_url详情页的url，帖子的url地址
        print('正在请求详情页:',title)
        detail_html_str = self.parse_url(detail_url)
        detail_html = etree.HTML(detail_html_str)
        img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
        total_img_list.extend(img_list)  #把当前页面的图片地址放入total_img_list
        next_url_temp = detail_html.xpath("//a[text()='下一页']/@href")
        #判断是否有下一页
        if len(next_url_temp)>0:
            next_url = self.part_url+next_url_temp[0]
            return self.get_img_list(next_url,total_img_list,title)
        else:
            return total_img_list

    def save_content_list(self,content_list): #保存
        for content in content_list:
            print(content)

    def run(self):#实现主要逻辑
        next_url = self.start_url
        while next_url is not None:
            #1.start_url
            #2.发送请求，获取响应
            html_str = self.parse_url(next_url)
            #3.提取数据
            #3。1.获取列表页的标题和url地址
            #3。2获取详情页的图片
            content_list,next_url = self.get_content_list(html_str)
            #保存
            self.save_content_list(content_list)
if __name__ == '__main__':
    tieba_spider = TiebaSpider("李毅")
    tieba_spider.run()

