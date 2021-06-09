# 爬取豆瓣电影排行 top250 单页
# https://movie.douban.com/top250
import requests
from lxml import etree
import pprint

url = "https://movie.douban.com/top250"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}

response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)

# 直接得到所有电影的同一项信息
film_rank = html.xpath(
    '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="pic"]/em/text()')
film_name = html.xpath(
    '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="info"]/div[@class="hd"]/a/span[1]/text()')
film_score = html.xpath(
    '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
pprint.pprint(list(zip(film_rank, film_name, film_score)))

print("======================================================================================")
# 先得到电影列表, 再得到每部电影的信息
movie_list = html.xpath('//div[@id="content"]/div/div[@class="article"]/ol/li')
for movie in movie_list:
    movie_rank = movie.xpath('./div/div[@class="pic"]/em/text()')
    movie_name = movie.xpath(
        './div/div[@class="info"]/div[@class="hd"]/a/span[1]/text()')
    movie_score = movie.xpath(
        './div/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
    pprint.pprint(list(zip(movie_rank, movie_name, movie_score)))
