# 爬取斗图吧最新表情包推荐 多张、下载

import requests
from lxml import etree
import os

# 检查文件夹是否存在，不存在就创建

url = "https://www.doutub.com/"
folder = "./download"
if not os.path.exists(folder):
    os.mkdir("download")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "referer": "https://www.doutub.com/"
}

response = requests.get(url, headers=headers)
html = etree.HTML(response.text)

img_divs = html.xpath('//div[@class="recommend-expression"]/div/div')


def download_one_img(img_name, img_url, img_suffix):
    '''
    :img_url 表情包的url,
    :img_name 表情包的名字,
    :img_suffix 表情包文件的后缀
    '''

    img_response = requests.get(img_url, headers=headers)
    img_data = img_response.content

    with open(f"./download/{img_name}.{img_suffix}", "wb") as f:
        f.write(img_data)


for index, div in enumerate(img_divs):
    img_name = div.xpath('./a/span/text()')[0]
    img_url = div.xpath('./a/img/@src')[0]
    img_suffix = img_url[img_url.rfind("."):]
    download_one_img(img_name, img_url, img_suffix)
    print(f"第{index + 1}张下载完毕")
