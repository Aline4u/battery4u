#!/usr/bin/python3

# Scrapy API imports
import scrapy
from scrapy.crawler import CrawlerProcess

# your spider
from FollowAllSpider import FollowAllSpider

# list to collect all items
items = []

# pipeline to fill the items list
class ItemCollectorPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        items.append(item)

# create a crawler process with the specified settings
process = CrawlerProcess({
    'USER_AGENT': 'scrapy',
    'LOG_LEVEL': 'INFO',
    'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
})

# start the spider
process.crawl(FollowAllSpider)
process.start()

# print the items
for item in items:
    print("url: " + item['url'])