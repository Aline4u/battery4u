import scrapy


class EbayBatterySpider(scrapy.Spider):
    name = "ebay_battery"
    allowed_domains = ["ebay.co.uk"]
    start_urls = ["https://www.ebay.co.uk/sch/i.html?_nkw=lifepo4+battery"]
    # https: // www.ebay.co.uk / sch / i.html?_from = R40 & _trksid = p4432023.m570.l1313 & _nkw = lithium + battery & _sacat = 0

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        'ROBOTSTXT_OBEY': False
    }
    def parse(self, response):
        for item in response.css("li.s-item"):
            # yield {
                # "title": item.xpath("//div/div[2]/a/div/text").get(),
                # "price": item.css("span.s-item__price::text").get(),
                # "condition": item.css("span.s-item__condition::text").get(),
            #     "url": item.css("a.s-item__link::attr(href)").get(),
            # }
            yield scrapy.Request(item.css("a.s-item__link::attr(href)").get(), callback=self.parseDetail)

        next_page = response.css("a.s-pagination__next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parseDetail(self, response):
        pass
