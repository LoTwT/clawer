# 爬取豆瓣电影排行 top250 翻页
# 拼接 url / 从下一页按钮获取
import requests
from lxml import etree
import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


# 基础请求，获取 html
def base_request(url):
    response = requests.get(url=url, headers=headers)
    return etree.HTML(response.text)


# 得到电影信息
def get_movies_info(html):
    # 排名
    film_rank = html.xpath(
        '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="pic"]/em/text()')
    # 名称
    film_name = html.xpath(
        '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="info"]/div[@class="hd"]/a/span[1]/text()')
    # 评分
    film_score = html.xpath(
        '//div[@id="content"]/div/div[@class="article"]/ol/li/div/div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
    return list(zip(film_rank, film_name, film_score))


# 获取一页中的电影信息
def crawl_page_movies(page_url):
    # 请求页面 html
    html = base_request(page_url)
    # 得到电影信息 list
    return get_movies_info(html)


# 拼接 url
def generate_urls(page_count):
    page_urls = []
    for i in range(1, page_count + 1):
        page_urls.append(
            f"https://movie.douban.com/top250?start={(i - 1) * 25}&filter=")
    return page_urls


# 根据传入的页数，拼接要爬取的 url
def crawl_movies_by_urls(page_urls):
    for index, page_url in enumerate(page_urls):
        print(f"=====第 {index + 1} 页开始爬取=====")
        pprint.pprint(crawl_page_movies(page_url))
        print(f"=====第 {index + 1} 页结束爬取=====")


# 爬取电影信息 + 下一页请求的 params
def crawl_page_movies_by_nextpage(url):
    html = base_request(url)
    movies_info = get_movies_info(html)
    next_page = html.xpath(
        '//div[@id="content"]/div/div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href')[0]
    return movies_info, next_page


# 根据下一页按钮进行翻页
def crawl_movies_by_nextpage(page_count):
    base_url = "https://movie.douban.com/top250"
    page_url = base_url
    for i in range(1, page_count + 1):
        movies_info, next_page = crawl_page_movies_by_nextpage(page_url)
        print(f"=====第 {i} 页开始爬取=====")
        pprint.pprint(movies_info)
        print(f"=====第 {i} 页结束爬取=====")
        page_url = base_url + next_page


if __name__ == "__main__":
    # 拼接 url
    # crawl_movies_by_urls(generate_urls(5))

    # 下一页
    crawl_movies_by_nextpage(5)
