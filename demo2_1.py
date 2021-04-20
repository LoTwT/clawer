# 爬取豆瓣 top250 翻页
# 分析 url, 修改每次爬取的 url 进行爬取单页, 最后进行汇总

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

    movie_info = list(zip(rank, title, score))
    return movie_info


movies = []
for i in range(0, 10):
    print(f"======> page{i} start")
    single_page_url = f"{url}?start={i*25}&filter="
    movies.append(craw_one_page(single_page_url))
    print(f"======> page{i} end")
pprint.pprint(movies)
