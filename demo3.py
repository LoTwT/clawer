# 爬取斗图吧最新表情包推荐 单张、下载

import requests
from lxml import etree

url = "https://www.doutub.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
}


def craw_one_img(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)

    # 图片名称
    img_name = html.xpath(
        '//div[@class="recommend-expression"]/div/div[2]/a/span/text()')[0]
    # 图片 url
    img_url = html.xpath(
        '//div[@class="recommend-expression"]/div/div[2]/a/img/@src')[0]
    # 图片后缀
    img_suffix = img_url[img_url.rfind(".") + 1:]

    return img_name, img_url, img_suffix


def download_one_img(url):
    img_name, img_url, img_suffix = craw_one_img(url)
    img_response = requests.get(img_url, headers=headers)
    img_data = img_response.content

    # 路径请自行修改
    with open(f"./download/{img_name}.{img_suffix}", "wb") as f:
        f.write(img_data)

    print(f"{img_name}.{img_suffix} 下载完成")


download_one_img(url)
