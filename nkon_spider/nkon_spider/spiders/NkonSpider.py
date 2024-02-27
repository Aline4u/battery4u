# Import the scrapy library
import scrapy

# Define the spider class
class NkonSpider(scrapy.Spider):
    # Set the name of the spider
    name = "nkon"

    # Load the settings from nkon.settings
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'FEED_FORMAT': 'json',
        # Change the FEED_URI to output.json
        'FEED_URI': 'output.json'
    }

    # Define the start URLs
    start_urls = [
        "https://www.nkon.nl/"
    ]

    # Define the parse method
    def parse(self, response):
        # Extract the title and price of each product
        products = response.xpath("//div[@class='product-item-info']")
        for product in products:
            yield {
                'title': product.xpath(".//a/text()").get(),
                'price': product.xpath(".//span[@class='price']/text()").get()
            }

        # Follow the next page link
        next_page = response.xpath("//a[@class='action next']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)