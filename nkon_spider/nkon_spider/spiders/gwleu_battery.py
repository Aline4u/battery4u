import scrapy
from scrapy.linkextractors import LinkExtractor
import re
from numpy.core.defchararray import isnumeric

class GwleuBatterySpider(scrapy.Spider):
    name = "gwleu_battery"
    allowed_domains = ["shop.gwl.eu"]
    # start_urls = ["https://shop.gwl.eu/"] rsponse 403 refused
    start_urls = ["https://shop.gwl.eu/LiFePO4-Single-Cells/"]

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    def parse(self, response):
        for url in LinkExtractor(unique='true', restrict_css='.item').extract_links(response):
            self.cur_url = url
            yield scrapy.Request(url.url, callback=self.parseDetail)
        productUrl = response.request.url

        yield {
            # "Debug": voltageList,
            "Product url": current_url,
        }