# coding=utf-8
from selenium import webdriver
import time

class DouyuSpider:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.start_url = "https://www.douyu.com/directory/all"


    def get_content_list(self):#提取数据
        li_list = self.driver.find_elements_by_xpath("//ul[@id='live-list-contentbox']/li")
        content_list = []
        for li in li_list:
            item = {}
            item["title"] = li.find_element_by_xpath("./a").get_attribute("title")
            item["category"] = li.find_element_by_xpath(".//span[@class='tag ellipsis']").text
            item["watch_num"] = li.find_element_by_xpath(".//span[@class='dy-num fr']").text
            item["anchor"]= li.find_element_by_xpath(".//span[@class='dy-name ellipsis fl']").text
            print(item)
            content_list.append(item)
        #提取房间的下一页
        next_url_temp = self.driver.find_elements_by_class_name("shark-pager-next")
        next_url = next_url_temp[0] if len(next_url_temp)>0 else None
        return content_list,next_url

    def save_content_list(self,content_list):#保存
        pass

    def __del__(self): #析构方法
        self.driver.quit()

    def run(self):#实现主要的逻辑
        #1.实例化一个dirver,start_url
        #2.发送请求
        self.driver.get(self.start_url)
        #3.提取数据
        #3.1房间信息
        content_list,next_url = self.get_content_list()
        #3.2下一页的元素
        #4保存
        self.save_content_list(content_list)
        #5.循环2-5
        while next_url is not None:
            next_url.click()
            time.sleep(2)
            content_list,next_url = self.get_content_list()
            self.save_content_list(content_list)
        # self.driver.quit()


if __name__ == '__main__':
    douyu = DouyuSpider()
    douyu.run()