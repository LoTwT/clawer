# 小说下载器
# 爬取小说名, 章节名, 单章内容

import requests
from lxml import etree
import os

url = "https://www.tsxs.org/121/121401/"
base_url = "https://www.tsxs.org"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
    "referer": "https://www.doutub.com/"
}


def get_novel_title(url):
    response = requests.get(url, headers=headers)
    response.encoding = "gbk"
    html = etree.HTML(response.text)

    novel_title = html.xpath('//*[@id="maininfo"]/div[1]/h1/text()')[0]
    return novel_title


def mk_novel_folder(novel_title):
    if not os.path.exists(novel_title):
        os.mkdir(novel_title)

    os.chdir(novel_title)


def get_novel_catelogue(url):
    response = requests.get(url, headers=headers)
    response.encoding = "gbk"
    html = etree.HTML(response.text)

    chapter_title = html.xpath('//*[@id="chapterlist"]/li/a/text()')
    chapter_url = html.xpath('//*[@id="chapterlist"]/li/a/@href')
    return list(zip(chapter_title, chapter_url))


def get_single_chapter(url):
    response = requests.get(url, headers=headers)
    response.encoding = "gbk"
    html = etree.HTML(response.text)

    chapter_title = html.xpath('//*[@id="mains"]/div[1]/h1/text()')
    chapter_content = html.xpath('//*[@id="book_text"]//text()')

    chapter_content = ("\n".join([i.strip() for i in chapter_content]))
    return chapter_title, chapter_content
