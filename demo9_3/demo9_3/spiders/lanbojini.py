import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class LanbojiniSpider(CrawlSpider):
    name = 'lanbojini'
    # allowed_domains = ['www.che168.com']
    start_urls = ['https://www.che168.com/china/lanbojini/?pvareaid=101025']

    rules = (
        Rule(LinkExtractor(allow=r'/china/lanbojini/a0_0msdgscncgpi1ltocsp\d+exx0/\?pvareaid=102179#currengpostion'),
             callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print("===========================================")
        print(response.text)
        print("===========================================")
