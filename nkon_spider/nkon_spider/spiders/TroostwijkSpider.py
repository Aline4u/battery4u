import scrapy

class TroostwijkSpider(scrapy.Spider):
    name = 'troostwijk'
    allowed_domains = ['troostwijkauctions.com']
    start_urls = ['https://www.troostwijkauctions.com/auctions']

    def parse(self, response):
        auction_links = response.css('a.aucLink')

        for auction_link in auction_links:
            auction_url = auction_link.attrib['href']

            yield scrapy.Request(auction_url, self.parse_auction)

    def parse_auction(self, response):
        auction_data = {}

        auction_data['title'] = response.css('h1.title').text
        auction_data['description'] = response.css('div.description').text
        auction_data['date'] = response.css('span.date').text
        auction_data['location'] = response.css('span.location').text

        yield auction_data