# Import scrapy module
import scrapy
from scrapy import Selector


# Define a spider class that inherits from scrapy.Spider
class NkonSpider(scrapy.Spider):
    # Give a name to the spider
    name = "nkon_spider"

    # Define the start_urls attribute with the web address
    start_urls = ["https://eu.nkon.nl/rechargeable/li-ion/samsung-inr-18650-30q-3000mah-15a-2017.html"]

    # Define the parse method that will be called for each response
    def parse(self, response):

        sel = Selector(response)

        # Create an empty list to store the text elements

        text_list = []
        xPath_list = []
        # Loop through all the xpaths in the response
        # Loop through all the elements in the HTML document
        for element in Selector(response=response).xpath("//text()"):
            # Get the XPath of the element
            xpath = element.get()

            # Get the text of the element
            text = element.text

            # If the text is not empty, add the XPath to the list
            if text:
                xPath_list.append(xpath)

        for xpath in response.xpath("//*"):
            # Extract the text from the xpath using .get() method
            text = xpath.get()

            # Check if the text is not empty or None
            if text and text.strip():
                # Append the text to the list
                text_list.append(text)
            if text == 'Voltage':
                xPath_list.append(xpath)

        # Print the list of text elements
        print(text_list)