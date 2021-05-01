# 代理 IP 使用
# 代理 IP 池 -- 代理云
# 爬取药智数据 -- https://db.yaozh.com

import random
import requests


class Craw:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }

    proxy_pool_url = "http://kk709937065.v4.dailiyun.com/query.txt?key=NP067E83B2&word=&count=1&rand=false&ltime=0&norepeat=false&detail=false"

    def __init__(self, url_count):
        self.url_count = url_count

    @property
    def proxy(self):
        proxy_ip = requests.get(self.proxy_pool_url).text.strip()
        return {"https": f"https://{proxy_ip}"}

    def target_link_urls(self):
        urls = []
        for url in range(1, self.url_count + 1):
            urls.append(f"https://db.yaozh.com/hmap/{url}.html")
        # 将 urls 打乱顺序
        random.shuffle(urls)
        return urls

    def craw_data(self, url):
        response = requests.get(
            url=url, headers=self.headers, allow_redirects=False, proxies=self.proxy)
        print(f"url   : {url}")
        print(f"status: {response.status_code}")
        print("=======================================")

    def run(self):
        urls = self.target_link_urls()
        for url in urls:
            self.craw_data(url)


if __name__ == "__main__":
    count = int(input("请输入你要爬取的 url 数量: "))
    craw_instance = Craw(count)
    craw_instance.run()
