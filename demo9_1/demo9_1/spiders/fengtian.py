import scrapy


class FengtianSpider(scrapy.Spider):
    name = 'fengtian'
    allowed_domains = ['www.che168.com']
    start_urls = ['http://www.che168.com/']

    def parse(self, response):
        print(response.text)
