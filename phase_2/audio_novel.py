# 有声小说爬取
# 发现具体播放页有请求返回了所有章节的 名称 + url, 所以只要得到这个请求地址即可
# http://m.ysxs8.com/
import requests
from lxml import etree
import os

base_url = "http://m.ysxs8.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


# 获取第一集详情页的链接
def get_detail_playlist_url(overview_url):
    response = requests.get(url=overview_url, headers=headers)
    response.encoding = "gb2312"
    html = etree.HTML(response.text)

    # 有声小说名称
    novel_title = html.xpath(
        '//div[@class="booksite"]/div[@class="bookinfo"]/h2/text()')[0]
    # 爬取第一集详情链接
    detail_playlist_url = base_url + \
        html.xpath('//div[@id="playlist"]/ul/li/a/@href')[0]

    return novel_title, detail_playlist_url


# 获取得到所有音频链接数据的 url
def get_src_url(detail_playlist_url):
    detail_response = requests.get(url=detail_playlist_url, headers=headers)
    detail_html = etree.HTML(detail_response.text)

    src_url = base_url + \
        detail_html.xpath('//div[@class="booksite"]/script[1]/@src')[0]

    return src_url


# 将请求到的音频数据连接返回的字符串进行处理，返回 list
def get_chapter_list(src_url):
    response = requests.get(url=src_url, headers=headers)
    response.encoding = "gb2312"

    chapter_list = response.text.replace("'", "").split("=")[
        1][:-8].split(",")
    chapter_list.pop(0)
    chapter_list[0] = chapter_list[0][1:]
    chapter_list[len(chapter_list) -
                 1] = chapter_list[len(chapter_list) - 1][:-3]

    return chapter_list


def check_folder(save_folder):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)


# 下载
def download_audio(chapter_list, novel_title):
    '''
    chapter_list: "chapter_name$chapter_url$flv"
    '''
    for chapter in chapter_list:
        chapter_info = chapter.split("$")
        chapter_name = chapter_info[0].encode().decode("unicode-escape")
        chapter_url = chapter_info[1]
        chapter_suffix = chapter_url.split(".")[-1]
        print(f"{chapter_name} 开始下载")
        with open(f"{novel_title}/{chapter_name}.{chapter_suffix}", "wb") as f:
            f.write(requests.get(url=chapter_url).content)
        print(f"{chapter_name} 结束下载")
        print("====================")
    print("全部下载完成")


if __name__ == "__main__":
    novel_url = str(input("请输入要爬取的小说地址(有声小说吧): "))
    novel_title, detail_playlist_url = get_detail_playlist_url(novel_url)
    src_url = get_src_url(detail_playlist_url)
    chapter_list = get_chapter_list(src_url)
    check_folder(novel_title)
    download_audio(chapter_list, novel_title)
