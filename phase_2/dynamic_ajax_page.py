# 动态页面爬取 - 分析法
# 1. 页面动态加载，response.text 只有最简单的结构
# 2. 分析 ajax 请求 (注意携带必要的 request headers)
# 3. 分析参数，模拟数据请求
# https://www.epubit.com/books
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Origin-Domain": "www.epubit.com",
    "Referer": "https://www.epubit.com/books",
    "X-Requested-With": "XMLHttpRequest"
}


def get_booklist_data():
    # 返回 booklist 的url
    booklist_url = "https://www.epubit.com/pubcloud/content/front/portal/getUbookList"
    # 拼接请求所需参数
    # params 对应 get 请求 / data 对应 post 请求
    params = (
        ("page", 1),
        ("row", 20),
        ("startPrice", ""),
        ("endPrice", ""),
        ("tagId", "")
    )

    response = requests.get(url=booklist_url, headers=headers, params=params)
    booklist_data = response.json()["data"]["records"]
    return booklist_data


def generate_book_info(booklist_data):
    for book_info in booklist_data:
        print("书名: {}, 作者: {}, 价格: {}".format(
            book_info["name"], book_info["authors"], book_info["price"]))


if __name__ == "__main__":
    booklist_data = get_booklist_data()
    generate_book_info(booklist_data)
