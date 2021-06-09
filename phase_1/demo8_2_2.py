# 异步爬虫
# 多线程、进程池
# 改造 demo8_1


import requests
from lxml import etree
import time
import os
import pprint
from threading import Thread
from multiprocessing.dummy import Pool

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

        print(f"{resume_title} 开始下载")
        with open(f"./{saveFolder}/{resume_title}.{resume_type}", "wb") as f:
            f.write(resume_data)
        print(f"{resume_title} 下载完成")
    else:
        raise Exception("download_resume error")


def status_check(response):
    if response != None and response.status_code == 200:
        return True
    return False


# 多线程
def run_threading():
    threads = []
    for detail_url in craw_detail_urls(base_url):
        thread = Thread(target=craw_resume, args=(detail_url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# 线程池
def run_pool():
    with Pool(10) as pool:
        pool.map(craw_resume, craw_detail_urls(base_url))


if __name__ == "__main__":
    try:
        start_time = time.time()
        mk_folder(saveFolder)
        # run_threading()  # 多线程
        run_pool()  # 进程池
        end_time = time.time()
        print(f"共用时: {end_time - start_time}")
    except Exception as err:
        print(err)
