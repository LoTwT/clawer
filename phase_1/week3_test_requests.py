import requests
from lxml import etree
import re
import time
import urllib.parse


class JDCrawler:
    # 静态加载部分 请求 url
    odd_base_url = "https://search.jd.com/Search"
    # 动态加载部分 请求 url
    even_base_url = "https://search.jd.com/s_new.php"
    # 静态加载 url 请求头
    odd_headers = {
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    def __init__(self):
        print("这里是爬取京东商品小助手~~~")
        # 获取用户输入
        good_category, target_page = self.get_user_input()
        # 要搜索的商品名
        self.good_category = good_category
        # 目标页数
        self.target_page = target_page
        # 动态加载部分 请求头
        self.even_headers = self.odd_headers.copy()
        self.even_headers[
            "referer"] = f"https://search.jd.com/Search?keyword={urllib.parse.quote(self.good_category)}&enc=utf-8&pvid=160dc623081347c6a8259bc3331be37c"

    # 获取用户输入
    def get_user_input(self):
        good_category = str(input("请输入你要搜索的商品名称: "))
        target_page = int(input("请输入你要爬取的页数: "))
        return good_category, target_page

    # 生成请求静态加载 url 的参数列表
    def generate_odd_url_params_list(self):
        odd_url_params_list = []
        for page_count in range(1, self.target_page + 1):
            static_params = (
                ("keyword", self.good_category),
                ("wq", self.good_category),
                ("page", (2 * page_count - 1))
            )
            odd_url_params_list.append(static_params)
        return odd_url_params_list

    # 生成请求动态加载 url 的参数和对应请求头
    def generate_even_url_params(self, odd_response):
        time.sleep(3)
        html = etree.HTML(odd_response.text)
        logParm = "".join(html.xpath('//head/script[4]//text()')).lstrip().split(
            "searchUnit.loadingStart=new Date().getTime();")[0]
        show_items = re.findall(r"wids:'(.*?)',uuid", logParm)[0]
        log_id = re.findall(r"log_id:'(.*?)',", logParm)[0]
        page = int(re.findall(r"page:'(.*?)',", logParm)[0]) + 1
        s = (page - 1) * 29

        even_url_params = (
            ("keyword", self.good_category),
            ("qrst", 1),
            ("suggest", r"1.his.0.0"),
            ("wq", self.good_category),
            ("stock", 1),
            ("page", page),
            ("s", s),
            ("scrolling", "y"),
            ("log_id", log_id),
            ("tpl", "1_M"),
            ("isList", 0),
            ("show_items", show_items),
        )

        return even_url_params

# 爬取商品信息
    def crawl_goods_info(self, response, isOdd):
        goods_li_list = []
        goods_info = []
        html = etree.HTML(response.text)
        if isOdd:
            goods_li_list = html.xpath('//*[@id="J_goodsList"]/ul/li')
        else:
            goods_li_list = html.xpath('//li')

        if len(goods_li_list) > 0:
            # 单页商品信息的数组
            for good in goods_li_list:
                # 商品名称
                # 此处解析得到的文本数组夹杂数组和无关信息, 简单处理
                good_name = "".join(good.xpath(
                    './div/div[@class="p-name p-name-type-2"]/a/em//text()')).replace("京东超市", "").replace("拍拍", "").lstrip()
                # 商品价格
                good_price = good.xpath(
                    './div/div[@class="p-price"]/strong/i//text()')[0]
                # 商家信息
                good_shop = good.xpath(
                    './div/div[@class="p-shop"]/span/a//text()')[0]
                goods_info.append({
                    "name": good_name,
                    "price": good_price,
                    "shop": good_shop
                })

        return goods_info

    # 保存单页数据至 txt 文件中
    def save_data(self, goods_info):
        with open(f"{self.good_category}.txt", "a", encoding="utf-8") as f:
            for good in goods_info:
                good_data = f"名称: {good['name']}, 价格: {good['price']}, 店铺: {good['shop']}\n"
                f.write(good_data)
            f.write(
                "=====================================================================================================================\n")

    # 爬取单页
    def craw_single_page(self, odd_url_params):
        # 请求静态加载部分
        odd_response = requests.get(
            url=self.odd_base_url, headers=self.odd_headers, params=odd_url_params)
        # 静态加载部分商品信息
        odd_goods_info = self.crawl_goods_info(odd_response, isOdd=True)
        # 该页动态加载部分请求参数
        even_url_params = self.generate_even_url_params(
            odd_response)
        # 请求动态加载部分
        even_response = requests.get(
            url=self.even_base_url, headers=self.even_headers, params=even_url_params)
        # 动态加载部分商品信息
        even_goods_info = self.crawl_goods_info(even_response, isOdd=False)
        # 汇总两部分商品信息
        goods_info = odd_goods_info + even_goods_info
        # 存储
        self.save_data(goods_info)

    # 主函数
    def run(self):
        odd_url_params_list = self.generate_odd_url_params_list()
        for index, odd_url_params in enumerate(odd_url_params_list):
            print(f"{self.good_category} 第 {index + 1} 页开始爬取~~~")
            self.craw_single_page(odd_url_params)
            print(f"{self.good_category} 第 {index + 1} 页爬取完成~~~")
        print("爬取完成。小爬虫下班啦~~~")


if __name__ == "__main__":
    jdcrawler = JDCrawler()
    jdcrawler.run()
