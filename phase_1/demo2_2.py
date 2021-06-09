# 爬取豆瓣 top250 翻页
# 模拟点击下一页, 通过 xpath 得到下一页的地址, 进行单页爬取, 进行汇总

import requests
from lxml import etree
import pprint

url = "https://movie.douban.com/top250"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}


def craw_one_page(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)

    rank = html.xpath('//div[@class="item"]/div[1]/em/text()')
    title = html.xpath('//div[@class="item"]/div[2]/div[1]/a/span[1]/text()')
    score = html.xpath('//div[@class="item"]/div[2]/div[2]/div/span[2]/text()')
    # 判断是否有下一页的地址
    next_page = html.xpath("//span[@class='next']/a/@href")

    movie_info = list(zip(rank, title, score))
    return movie_info, next_page


movies = []
current_url = url
page_count = 1
while(current_url):
    print(f"正在抓取第{page_count}页")
    movie_info, next_page = craw_one_page(current_url)
    movies.append(movie_info)
    if (len(next_page) > 0):
        page_count += 1
        current_url = f"{url}{next_page[0]}"
    else:
        current_url = None

pprint.pprint(movies)
