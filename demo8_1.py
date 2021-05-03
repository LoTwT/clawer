# 异步爬虫
# https://sc.chinaz.com/jianli/free.html
# 同步实现


import requests
from lxml import etree
import time
import os
import pprint

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}

base_url = "https://sc.chinaz.com/jianli/free.html"

saveFolder = "ResumeTemplate"


def mk_folder(saveFolder):
    if not os.path.exists(saveFolder):
        os.mkdir(saveFolder)


def base_request(url):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = "utf-8"
        if response.status_code == 200:
            return response
        else:
            return None
    except:
        return None


def craw_detail_urls(base_url):
    main_response = base_request(base_url)
    if status_check(main_response):
        main_html = etree.HTML(main_response.text)
        detail_urls = main_html.xpath('//div[@id="main"]/div/div/a/@href')
        return ["https:" + detail_url for detail_url in detail_urls]
    else:
        raise Exception("craw_detail_urls error")


def craw_resume(detail_url):
    detail_response = base_request(detail_url)
    if status_check(detail_response):
        detail_html = etree.HTML(detail_response.text)

        resume_title = detail_html.xpath(
            '//div[@class="ppt_tit clearfix"]/h1/text()')[0]
        download_url = detail_html.xpath(
            '//div[@class="clearfix mt20 downlist"]/ul/li[1]/a/@href')[0]
        download_resume(resume_title, download_url)
    else:
        raise Exception("craw_resume error")


def download_resume(resume_title, download_url):
    resume_respnose = base_request(download_url)
    if status_check(resume_respnose):
        resume_data = resume_respnose.content
        resume_type = download_url[download_url.rfind("."):]

        pprint.pprint(f"{resume_title} 开始下载")
        with open(f"./{saveFolder}/{resume_title}.{resume_type}", "wb") as f:
            f.write(resume_data)
        pprint.pprint(f"{resume_title} 下载完成")
    else:
        raise Exception("download_resume error")


def status_check(response):
    if response != None and response.status_code == 200:
        return True
    return False


def main_loop():
    try:
        start_time = time.time()
        mk_folder(saveFolder)
        detail_urls = craw_detail_urls(base_url)
        for detail_url in detail_urls:
            craw_resume(detail_url)
        end_time = time.time()
        pprint.pprint(f"共用时: {end_time - start_time}")
    except Exception as err:
        pprint.pprint(err)


if __name__ == "__main__":
    main_loop()
