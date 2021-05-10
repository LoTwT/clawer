# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Demo94Pipeline:
    def process_item(self, item, spider):
        line_data = f"型号：{item['model']}，价格：{item['price']}，里程：{item['dist']}，日期：{item['date']}，城市：{item['city']}\n"
        self.f.write(line_data)
        return item

    def open_spider(self, spider):
        print("爬虫开始")
        self.f = open("laosilaisi.txt", "w", encoding="utf-8")

    def close_spider(self, spider):
        print("爬虫结束")
        self.f.close()
