# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Demo94Item(scrapy.Item):
    model = scrapy.Field()
    price = scrapy.Field()
    dist = scrapy.Field()
    city = scrapy.Field()
    date = scrapy.Field()
