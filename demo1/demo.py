import requests
from lxml import etree

url = "https://movie.douban.com/top250"

# 抓取豆瓣必须添加User-Agent的Header，有的网站不需要
# 要知道自己的浏览器的header，可以访问这个地址：http://httpbin.org/get
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}

response = requests.get(url, headers=headers)

html = etree.HTML(response.text)
rank = html.xpath('//div[@class="item"]/div[1]/em/text()')
title = html.xpath('//div[@class="item"]/div[2]/div[1]/a/span[1]/text()')
score = html.xpath('//div[@class="item"]/div[2]/div[2]/div/span[2]/text()')

movie_info = list(zip(rank, title, score))
print(movie_info)
