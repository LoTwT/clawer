import scrapy
import re
import time


class ErshoucheSpider(scrapy.Spider):
    name = 'ershouche'
    allowed_domains = ['www.che168.com']
    start_urls = ['https://www.che168.com/china/leikesasi/#pvareaid=105866']
    base_url = "https://www.che168.com"

    def parse(self, response):
        car_list = response.xpath(
            '//ul[@class="viewlist_ul"]/li[@name="lazyloadcpc"]')

        for car in car_list:
            # 型号
            car_name = car.xpath(
                './/h4[@class="card-name"]//text()').extract_first()
            # 价格
            car_price = car.xpath(
                './/span[@class="pirce"]/em//text()').extract_first()
            # 描述
            car_description = car.xpath(
                './/p[@class="cards-unit"]//text()').extract_first()

            # 使用正则从描述中提取里程、日期、城市  2.52万公里／2019-02／海口／商家
            car_mile = "".join(re.findall('.*万公里', car_description))
            car_date = "".join(re.findall('\d{4}-\d{2}', car_description))
            car_city = "".join(re.findall('.*万公里／.*／(.*)／', car_description))

            car_info = {
                "型号": car_name,
                "价格": car_price,
                "里程": car_mile + "万公里",
                "日期": car_date,
                "城市": car_city
            }

            detail_url = self.base_url + car.xpath('./a/@href').extract_first()

            # print(car_info)
            yield scrapy.Request(url=detail_url, callback=self.parse_detail_page, meta=car_info)

        print("====================下一页====================")
        # 获取下一页的 url
        next_page_url = self.base_url + \
            response.xpath(
                '//*[@id="listpagination"]/a[@class="page-item-next"]/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail_page(self, response):
        print('================详情页====================')
        seller_info = re.findall(
            '<span class="manger-name">(.*?)</span>', response.text)[0]
        seller_location = re.findall(
            '<div class="protarit-adress">(.*?)</div>', response.text)[0]
        car_info = response.meta
        print(
            f"车辆信息: {car_info}，商家/个人信息：{seller_info}，商家/个人详细地址：{seller_location}")
