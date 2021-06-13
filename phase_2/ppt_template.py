# 爬取 PPT 模板
# http://www.pptbz.com/pptmoban/jingmeippt/
import requests
from lxml import etree
import os

url = "http://www.pptbz.com/pptmoban/jingmeippt/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
}


# 请求获得 html
def get_html_tree(target_url):
    response = requests.get(url=target_url, headers=headers)
    response.encoding = "gbk"
    return etree.HTML(response.text)


# 生成 ppt 详情页的 url
def generate_detail_urls():
    detail_html = get_html_tree(url)
    base_url = "http://www.pptbz.com/"
    ppt_detail_suffix_list = detail_html.xpath(
        '//div[@class="wrapper"]/ul/li/a[1]/@href')
    ppt_detail_urls_list = []
    # 拼接 url
    for suffix in ppt_detail_suffix_list:
        ppt_detail_urls_list.append(base_url + suffix)

    return ppt_detail_urls_list


# 生成单张 ppt 的 名称、下载链接、文件后缀
def generate_ppt_info(ppt_detail_urls_list):
    ppt_info_list = []
    for ppt_detail_url in ppt_detail_urls_list:
        page_html = get_html_tree(ppt_detail_url)
        # 名称
        ppt_name = page_html.xpath('//div[@class="infoss"]/h1/text()')[0]
        # 下载链接
        ppt_download_url = page_html.xpath(
            '//div[@class="infoss"]/div[@class="button"]/a/@href')[0]
        # 后缀
        ppt_suffix = ppt_download_url.split(".")[-1]
        ppt_info_list.append((ppt_name, ppt_download_url, ppt_suffix))
    return ppt_info_list


# 下载 ppt
def download_ppts(ppt_info_list):
    '''
    ppt_info_list: 单张 ppt 信息 的 list, [(ppt_name, ppt_download_url, ppt_suffix)]
    '''
    # 生成文件夹
    save_folder = "ppt"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    # 下载
    for ppt_info in ppt_info_list:
        print(f"{ppt_info[0]}.{ppt_info[2]} 开始下载")
        # 获取文件的二进制数据
        ppt_content = requests.get(url=ppt_info[1], headers=headers).content
        with open(f"{save_folder}/{ppt_info[0]}.{ppt_info[2]}", "wb") as f:
            # 写入
            f.write(ppt_content)
        print(f"{ppt_info[0]}.{ppt_info[2]} 完成下载")
        print("==================================================")
    print("所有 ppt 下载完成")


if __name__ == "__main__":
    # 生成 ppt 详情页的 url
    ppt_detail_urls_list = generate_detail_urls()
    # 生成单张 ppt 的 名称、下载链接、文件后缀
    ppt_info_list = generate_ppt_info(ppt_detail_urls_list)
    # 下载
    download_ppts(ppt_info_list)
