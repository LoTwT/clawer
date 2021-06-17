# 动态页面爬取 - Selenium
# https://www.epubit.com/books
from lxml import etree
from selenium import webdriver
import time


class Crawler:
    url = "https://www.epubit.com/books"

    def __init__(self):
        # 由用户输入要爬取的页数
        self.target_page_count = int(input("请输入要爬取的页数: "))

    # 初始化实例
    def init_chrome(self):
        self.chrome = webdriver.Chrome()

    # 关闭实例
    def close_chrome(self):
        self.chrome.close()

    # 请求
    def base_request(self):
        self.chrome.get(self.url)

    # 获取一页上的 booklist 和 下一页 信息
    def get_page_info(self):
        # 通过 selenium 拿到 DOM tree
        html = etree.HTML(self.chrome.page_source)

        a_list = html.xpath('//div[@id="bookItem"]/a')
        for a in a_list:
            book_name = a.xpath(
                './div[@class="list-title moreline2"]/text()')[0]
            book_price = a.xpath(
                './div[@class="list-price clear"]/div[@class="price fl"]/text()')[0]
            print(f"书名：《{book_name}》, 价格：{book_price}")

    # 跳转下一页
    def go_next_page(self):
        button_next = self.chrome.find_element_by_xpath(
            '//div[@class="el-pagination is-background"]/button[@class="btn-next"]')
        button_next.click()

    # 入口函数
    def run(self):
        # 初始化实例
        self.init_chrome()
        # 建立连接
        self.base_request()
        # 爬取信息
        for count in range(1, self.target_page_count + 1):
            print(f"第 {count} 页 开始爬取")
            self.get_page_info()
            print(f"第 {count} 页 结束爬取")
            print("====================")
            time.sleep(2)
            if count != self.target_page_count + 1:
                self.go_next_page()
        # 关闭实例
        self.close_chrome()
        print("全部爬取完成")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
