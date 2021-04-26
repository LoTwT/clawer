# 动态页面爬取 - 分析法

import requests
from lxml import etree
import pprint


def craw_onepage_booklist(page_num):
    url = "https://www.epubit.com/pubcloud/content/front/portal/getUbookList"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Origin-Domain": "www.epubit.com",
        "X-Requested-With": "XMLHttpRequest"
    }

    params = (
        ("page", int(page_num)),
        ("row", "20"),
        ("startPrice", ""),
        ("endPrice", ""),
        ("tagId", "")
    )

    response = requests.get(url, headers=headers, params=params)
    return response.json()


def extract_data(booklist_json):
    booklist = booklist_json["data"]["records"]

    for book in booklist:
        print(
            f'书名: {book["name"]}, 作者: {book["authors"]}, 价格: {book["price"]}')


def run_craw(page_num):
    booklist_json = craw_onepage_booklist(page_num)
    extract_data(booklist_json)


if __name__ == "__main__":
    page_num = int(input("请输入要爬取的页数: "))
    run_craw(page_num)
