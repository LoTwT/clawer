from selenium import webdriver
from lxml import etree
import time


class JDCrawler:
    base_url = "https://www.jd.com/"

    def __init__(self, good_category, target_page, global_interval=1):
        # 实例化
        self.chrome = webdriver.Chrome()
        # 要搜索的商品名
        self.good_category = good_category
        # 目标页数
        self.target_page = target_page
        # 全局延时, 根据网络状态自行调整
        self.global_interval = global_interval
        # 页数检查
        self.check_page_count(target_page)

    # 建立连接
    def start(self, url):
        self.chrome.get(url)
        print("小爬虫开始工作啦~~~")

    # 关闭浏览器
    def close(self):
        self.chrome.close()
        print("小爬虫下班啦~~~")

    # 页数检查
    # 京东默认只显示 100 页
    def check_page_count(self, target_page):
        # 当输入的页数不是数值
        if type(target_page) is not int:
            self.target_page = 1
            print("输入页数不为数值, 默认更改为第 1 页")
        else:
            if target_page < 1:
                self.target_page = 1
                print("输入页数小于 0, 默认更改为第 1 页")
            elif target_page > 100:
                self.target_page = 100
                print("输入页数大于 100, 默认更改为第 100 页")

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

    # 爬取商品列表页 单页 所需数据
    def crawl_single_page(self):
        html = etree.HTML(self.chrome.page_source)
        goods_list = html.xpath('//*[@id="J_goodsList"]/ul/li')
        goods_info = []
        for good in goods_list:
            good_name = "".join(good.xpath(
                './div/div[@class="p-name p-name-type-2"]/a/em//text()')).replace("京东超市", "").replace("拍拍", "").lstrip()
            good_price = good.xpath(
                './div/div[@class="p-price"]/strong/i//text()')[0]
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

    # 主函数
    def run(self):
        self.start(self.base_url)
        self.searchbar_input(self.good_category)
        self.searchbar_click()

        for page_count in range(1, self.target_page + 1):
            print(f"第{page_count}页开始下载")
            self.scroll_to_bottom()
            self.save_data(self.crawl_single_page())
            if page_count != self.target_page:
                self.go_next_page()
            print(f"第{page_count}页下载完成")

        self.close()


if __name__ == "__main__":
    print("这里是爬取京东商品小助手~~~")
    good_category = str(input("请输入你要搜索的商品名称: "))
    target_page = int(input("请输入你要爬取的页数: "))
    jdCrawler = JDCrawler(good_category=good_category, target_page=target_page)
    jdCrawler.run()
