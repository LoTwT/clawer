# 异步爬虫
# 协程
# 改写 demo8_1


import time
import requests
from lxml import etree
import pprint
import asyncio
import aiohttp

index_url = 'https://sc.chinaz.com/jianli/free.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42',
}

# 因为本次项目需要先请求目录页，再请求详情页，最后再请求文件下载链接，可能还要实现翻页
# 所以封装一个函数，方便重复使用


def request(url):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        else:
            print('Non 200 status code')
            return ''
    except Exception as err:
        print('crawler error：' + err)


# 爬取目录页中详情页的url。
def get_detail_link(url):
    response = request(url)
    tree = etree.HTML(response.text)
    detail_link = tree.xpath('//*[@id="container"]/div/p/a/@href')
    detall_link_list = ['https:' + i for i in detail_link]  # url拼接
    return detall_link_list


async def download_document(url):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url) as r1:
            text = await r1.read()
            tree = etree.HTML(text.decode('utf-8'))
            document_name = tree.xpath('//h1/text()')[0]
            document_link = tree.xpath(
                '//*[@id="down"]/div[2]/ul/li[1]/a/@href')[0]
            document_type = document_link[-3:]
            async with session.get(document_link) as r2:
                print(f"开始下载{document_name}。")
                content = await r2.read()
                with open(f'{document_name}.{document_type}', 'wb')as f:
                    f.write(content)
                print(f"{document_name}下载结束！")


async def main():
    links = get_detail_link(index_url)
    tasks = []
    for link in links:
        t = asyncio.create_task(download_document(link))
        tasks.append(t)
    for t in tasks:
        await t

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f'共用时：{end_time - start_time}')
