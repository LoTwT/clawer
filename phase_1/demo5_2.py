from selenium import webdriver
import requests
from lxml import etree
import time

chrome = webdriver.Chrome()
chrome.get("https://www.epubit.com/books")


# 爬取单页上的信息
def craw_one_page_books(page_source):
    html = etree.HTML(page_source)
    book_list = html.xpath('//*[@id="bookItem"]/a')

    print("========== one page start ==========")
    for book in book_list:
        book_name = book.xpath(
            './div[@class="list-title moreline2"]/text()')[0]
        book_price = book.xpath(
            './div[@class="list-price clear"]/div[@class="price fl"]/text()')[0]
        print(f"书名: {book_name}, 价格: {book_price}")
    print("=========== one page end ===========")


# 模拟点击下一页
def to_next_page():
    next_page = chrome.find_element_by_xpath(
        '//div[@class="list-pagination"]/div[1]/button[2]')
    next_page.click()


def craw_books():
    for _ in range(3):
        craw_one_page_books(chrome.page_source)
        to_next_page()
        time.sleep(2)


if __name__ == "__main__":
    craw_books()
    chrome.quit()
