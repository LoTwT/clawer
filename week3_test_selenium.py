from selenium import webdriver
from lxml import etree
import time


class JDCrawler:
    base_url = "https://www.jd.com/"

    def __init__(self):
        self.chrome = webdriver.Chrome()

    # 建立连接
    def request(self, url):
        self.chrome.get(url)

    # 关闭浏览器
    def close(self):
        self.chrome.close()

    # 首页搜索框输入
    def searchbar_input(self, good_category, interval=1):
        self.chrome.find_element_by_xpath(
            '//*[@id="search"]/div/div[@class="form"]/input').send_keys(good_category)
        time.sleep(interval)

    # 首页搜索跳转
    def searchbar_click(self, interval=1):
        self.chrome.find_element_by_xpath(
            '//*[@id="search"]/div/div[@class="form"]/button').click()
        time.sleep(interval)

    # 商品列表页 滚动页面至底部 => 等待页面动态加载数据完成
    def scroll_to_bottom(self, interval=2):
        self.chrome.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(interval)

    # 商品列表页 下一页
    def go_next_page(self, interval=1):
        self.chrome.find_element_by_xpath(
            '//*[@id="J_bottomPage"]/span[@class="p-num"]/a[@class="pn-next"]').click()
        time.sleep(interval)

    # 爬取商品列表页 单页 所需数据
    def crawl_single_page(self):
        html = etree.HTML(self.chrome.page_source)
        goods_list = html.xpath('//*[@id="J_goodsList"]/ul/li')
        goods_info = []
        for good in goods_list:
            good_name = "".join(good.xpath(
                './div/div[@class="p-name p-name-type-2"]/a/em//text()'))
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
        with open("data.txt", "a", encoding="utf-8") as f:
            for good in goods_info:
                good_data = f"名称: {good['name']}, 价格: {good['price']}, 店铺: {good['shop']}\n"
                f.write(good_data)

    def run_sync(self):
        self.request(self.base_url)
        self.searchbar_input("鸡胸肉")
        self.searchbar_click()
        self.scroll_to_bottom()
        self.save_data(self.crawl_single_page())
        self.close()


if __name__ == "__main__":
    jdCrawler = JDCrawler()
    jdCrawler.run_sync()
