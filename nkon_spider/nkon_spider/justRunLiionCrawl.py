from scrapy.crawler import CrawlerProcess
from nkon_spider.nkon_spider.spiders.nkon_battery_spider import NkonLionSpider



process = CrawlerProcess()
process.crawl(NkonLionSpider)
process.start()