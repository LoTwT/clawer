# 抓取该 url 下所有 ppt 模板
# http://www.pptbz.com/pptmoban/jingmeippt/

import requests
from lxml import etree
import os

url = "http://www.pptbz.com/pptmoban/jingmeippt/"
base_url = "http://www.pptbz.com"
save_folder = "pptx"


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "referer": "https://www.doutub.com/"
}


# 获取所有 ppt_url
def craw_ppt_urls(url):
    response = requests.get(url, headers=headers)
    response.encoding = "gbk"
    html = etree.HTML(response.text)

    # ppt_url
    ppt_urls = html.xpath('//div[@class="wrapper"]/ul/li/a[2]/@href')\

    return ppt_urls


# 获取单张 ppt 的名称和下载链接
def craw_pptdown(ppt_url):
    ppt_response = requests.get(ppt_url, headers=headers)
    ppt_response.encoding = "gbk"
    html = etree.HTML(ppt_response.text)

    ppt_name = html.xpath('//div[@class="info"]/div/div/h1/text()')[0]
    pptdown_url = html.xpath(
        '//div[@class="info"]/div/div/div[@class="button"]/a/@href')[0]

    return ppt_name, pptdown_url


# 下载单张 ppt 模板
def download_ppt(ppt_name, pptdown_url):
    pptdown_data = requests.get(pptdown_url, headers=headers).content
    pptdown_suffix = pptdown_url[pptdown_url.rfind("."):]

    with open(f"./{ppt_name}.{pptdown_suffix}", "wb") as f:
        f.write(pptdown_data)


# 下载所有 ppt 模版
def download_ppts(ppt_urls):
    for index, ppt_url in enumerate(ppt_urls):
        ppt_name, pptdown_url = craw_pptdown(base_url + ppt_url)
        download_ppt(ppt_name, pptdown_url)
        print(f"第{index + 1}份: {ppt_name} 下载完成")


# 确定下载路径
def mk_folder(save_folder):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    os.chdir(save_folder)


# 爬取 ppt 模板主程序
def craw_ppts(url):
    mk_folder(save_folder)
    ppt_urls = craw_ppt_urls(url)
    download_ppts(ppt_urls)


if __name__ == "__main__":
    craw_ppts(url)
