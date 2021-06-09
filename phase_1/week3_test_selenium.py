from selenium import webdriver
from lxml import etree
import time

# 创建 JDCrawler


class JDCrawler:
    base_url = "https://www.jd.com"

    def __init__(self, global_interval=1):
        print("这里是爬取京东商品小助手~~~")
        # 获取用户输入
        good_category, target_page = self.get_user_input()
        # 要搜索的商品名
        self.good_category = good_category
        # 目标页数
        self.target_page = target_page
        # 实例化
        self.chrome = webdriver.Chrome()
        # 全局延时, 根据网络状态自行调整
        self.global_interval = global_interval

    # 获取用户输入
    def get_user_input(self):
        good_category = str(input("请输入你要搜索的商品名称: "))
        target_page = int(input("请输入你要爬取的页数: "))
        return good_category, target_page

    # 首页搜索框输入
    def searchbar_input(self, good_category):
        self.chrome.find_element_by_xpath(
            '//*[@id="search"]/div/div[@class="form"]/input').send_keys(good_category)
        time.sleep(self.global_interval)

    # 首页搜索跳转
    def searchbar_click(self):
        self.chrome.find_element_by_xpath(
            '//*[@id="search"]/div/div[@class="form"]/button').click()
        time.sleep(self.global_interval)

    # 商品列表页 滚动页面至底部 => 等待页面动态加载数据完成
    def scroll_to_bottom(self):
        self.chrome.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(self.global_interval * 2)

    # 商品列表页 下一页
    def go_next_page(self):
        self.chrome.find_element_by_xpath(
            '//*[@id="J_bottomPage"]/span[@class="p-num"]/a[@class="pn-next"]').click()
        time.sleep(self.global_interval)

    def start(self, url):
        self.chrome.get(url)
        print("建立连接、发送请求成功~~~小爬虫开始上班啦~~~")

    # 获得响应
    def get_response(self):
        return self.chrome.page_source

    # 爬取商品列表页 单页 所需数据
    def crawl_single_page(self, response):
        html = etree.HTML(response)
        # 商品列表
        goods_list = html.xpath('//*[@id="J_goodsList"]/ul/li')
        # 单页商品信息的数组
        goods_info = []
        for good in goods_list:
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

    # 关闭链接、关闭浏览器
    def close(self):
        self.chrome.close()
        print("关闭链接~~~小爬虫下班啦~~~")

    # 运行爬虫
    def run(self):
        # 建立连接、发送请求
        self.start(self.base_url)
        # 搜索框输入
        self.searchbar_input(self.good_category)
        # 搜索跳转
        self.searchbar_click()

        for page_count in range(1, self.target_page + 1):
            print(f"第{page_count}页开始下载")
            # 滚动页面
            self.scroll_to_bottom()
            # 获得响应
            page_response = self.get_response()
            # 爬取单页数据
            goods_info = self.crawl_single_page(page_response)
            # 进行存储
            self.save_data(goods_info)
            # 当前页为要爬取的最后一页时, 不进行下一页跳转
            if page_count != self.target_page:
                self.go_next_page()
            print(f"第{page_count}页下载完成")

        # 关闭链接
        self.close()


if __name__ == "__main__":
    jdcrawler = JDCrawler()
    jdcrawler.run()
