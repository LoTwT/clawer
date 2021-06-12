# 爬取斗图吧表情包推荐
# https://www.doutub.com/
import requests
from lxml import etree
import os

url = "https://www.doutub.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


def get_emoji_info_list():
    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)

    recommend_emoji_list = html.xpath(
        '//div[@id="__layout"]//div[@class="recommend-expression"]/div/div[@class="cell"]')

    emoji_info_list = []
    for emoji in recommend_emoji_list:
        emoji_name = emoji.xpath('./a/img/@alt')[0]
        emoji_url = emoji.xpath('./a/img/@src')[0]
        emoji_suffix = emoji_url.split(".")[-1]
        emoji_info_list.append((emoji_name, emoji_url, emoji_suffix))

    return emoji_info_list


def download_emoji(emoji_info_list):
    save_folder = "doutuba"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for emoji_info in emoji_info_list:
        print(f"{emoji_info[0]} => 开始下载")
        with open(f"{save_folder}/{emoji_info[0]}.{emoji_info[2]}", "wb") as f:
            f.write(requests.get(url=emoji_info[1], headers=headers).content)
        print(f"{emoji_info[0]} => 结束下载")
        print("========================================")
    print("全部下载完成")


if __name__ == "__main__":
    emoji_info_list = get_emoji_info_list()
    download_emoji(emoji_info_list)
