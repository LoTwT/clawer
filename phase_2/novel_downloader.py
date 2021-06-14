# 小说下载器
# 吞噬小说网 https://www.tsxs.org/
import requests
from lxml import etree
import os

base_url = "https://www.tsxs.org"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


# 基本请求，返回 html
def base_request(url):
    response = requests.get(url=url, headers=headers)
    response.encoding = "gbk"
    return etree.HTML(response.text)


# 获得小说信息 (标题，章节列表)
def get_novel_info(novel_html):
    # 小说标题
    novel_title = novel_html.xpath(
        '//div[@id="maininfo"]/div[@class="info"]/h1/text()')[0]
    # 小说章节列表
    novel_chapter_url_list = novel_html.xpath(
        '//div[@class="article"]/div[1]/ul[@id="chapterlist"]/li/a/@href')
    return novel_title, novel_chapter_url_list


# 获得章节信息 (章节名称，章节内容)
def get_chapter_info(novel_chapter_url):
    novel_chapter_html = base_request(novel_chapter_url)
    # 章节名称
    chapter_title = novel_chapter_html.xpath(
        '//div[@id="mains"]/div[1]/h1/text()')[0].replace("正文 ", "")
    # 章节内容
    chapter_content = novel_chapter_html.xpath(
        '//div[@id="mains"]/div[1]/div[@id="book_text"]/text()')
    # 处理空格，并用换行符连接
    chapter_content = "\n".join([i.strip() for i in chapter_content])
    return chapter_title, chapter_content


# 判断要写入的文件夹是否存在
def check_folder(save_folder):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)


def download_novel(novel_url):
    noven_html = base_request(novel_url)
    novel_title, novel_chapter_url_list = get_novel_info(noven_html)

    check_folder(novel_title)

    with open(f"{novel_title}/{novel_title}.txt", "a", encoding="utf-8") as f:
        print(f"{novel_title} 开始下载")
        print("===================")
        # 写入标题
        f.write(f"{novel_title}\n")

        for novel_chapter_url in novel_chapter_url_list:
            # 将章节 url 补全
            novel_chapter_url = base_url + novel_chapter_url
            chapter_title, chapter_content = get_chapter_info(
                novel_chapter_url)
            print(f"{chapter_title} 开始下载")
            # 写入章节名称
            f.write(f"{chapter_title}\n")
            # 写入章节内容
            f.write(f"{chapter_content}\n")
            print(f"{chapter_title} 下载完成")
            print("===================")

        print(f"{novel_title} 下载完成")


if __name__ == "__main__":
    target_novel_url = str(input("请输入要下载的小说 url (仅限吞噬小说网): "))
    download_novel(target_novel_url)
