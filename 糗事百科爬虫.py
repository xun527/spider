# coding=utf-8
import requests
from lxml import etree
from queue import Queue
import threading

class QiuBai:
    def __init__(self):
        self.temp_url = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
        self.url_queue = Queue()  #放url的队列
        self.html_str_queue = Queue()  #放响应的队列
        self.content_list_queue = Queue() #放提取的数据的队列

    def get_url_list(self):  # 获取url列表
        for i in range(1,14):
            self.url_queue.put(self.temp_url.format(i))

    def parse_url(self):  # 发送请求，获取html字符串
        while True:
            url = self.url_queue.get()
            print(url)
            r = requests.get(url, headers=self.headers)
            self.html_str_queue.put(r.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        while True:
            html_str = self.html_str_queue.get()
            html = etree.HTML(html_str)
            div_list = html.xpath("//div[@id='content-left']/div")
            content_list = []
            for div in div_list:
                item = {}
                item["author_name"] = div.xpath(".//h2/text()")[0] if len(div.xpath(".//h2/text()")) > 0 else None
                item["content"] = div.xpath(".//div[@class='content']/span/text()")
                item["img_list"] = div.xpath(".//div[@class='thumb']/a/img/@src")
                content_list.append(item)
            self.content_list_queue.put(content_list)
            self.html_str_queue.task_done()

    def save_content_list(self):  # save
        while True:
            content_list = self.content_list_queue.get()
            for content in content_list:
                # print(content)
                pass
            self.content_list_queue.task_done()

    def run(self):  # 实现主要逻辑
        thread_list = []
        # 1.url_list
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)
        # 2.发送请求，获取数据
        for i in range(3):
            t_parse = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse)
        # 3.提取数据
        for i in range(2):
            t_content_list = threading.Thread(target=self.get_content_list)
            thread_list.append(t_content_list)
        # 4.保存
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)

        for t in thread_list:
            t.setDaemon(True) #设置为守护线程，守护线程：这个线程不重要，主线程结束，子线程结束
            t.start()

        for q in [self.url_queue,self.content_list_queue,self.html_str_queue]:
            q.join()  #让主线程等待着，知道队列计数为0的时候，join失效

        print("主线程结束")



if __name__ == '__main__':
    qiubai = QiuBai()
    qiubai.run()
