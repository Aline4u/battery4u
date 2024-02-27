# import string
# from math import ceil
# from typing import Any
from bs4 import BeautifulSoup as BS
import scrapy
from scrapy.linkextractors import LinkExtractor
import re
# from numpy.core.defchararray import isnumeric
# from scrapy.utils import response
import scrapy.item
keepNumOrDotPat = re.compile('[^0-9.]')
keepNumPat = re.compile('[^0-9]')
debug = ''
debugOn = True
reqVoltage = float(51.2)
# Name	Usable 	URL price	Voltage	ah	kwh	required4V		cycles	kWH for voltage	req V Kwh	4v pylontec factor	VoltagePrice	requiredfor2.5KW	TotalCost	Actualparallel		Cost2.4Kwh		Cost 5.38KwH	Cost2.4Kw boxes 	171.428571428571
# ,+++++,https://eu.nkon.nl/recharge  able/lifepo4/26650/jgne-26650-3200mah-3.29-6a-lifepo4.html,,€1.99,3.2,3.2,=F27*G27/1000,=CEILING(requiredVoltage/F27),,,=I27*H27,=I27*H27,=M27/2.4,=I27*E27,=requiredKW/(requiredVoltage*G27/1000),=P27*O27,"=IF(P27 < 1,1,P27)",=R27*O27,"=S27/IF(N27<1,1,N27)",=T27/2.4,=U27*5.38,,

def getKwHcost(priceIn, capacity, voltage: float, NumCells4ReqVoltage: float):
    if capacity == "no capacity2": return 'not calculated'
    capacity_Ah: float = capacity/1000
    price = float(priceIn)
    voltagePrice = NumCells4ReqVoltage * price
    actKwh = NumCells4ReqVoltage * float(voltage) * float(capacity_Ah / 1000)
    act1Kwh = 1 / actKwh
    cost4ReqKw = act1Kwh * voltagePrice
    return float(cost4ReqKw)



def xpath_soup(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name
            if siblings == [child] else
            '%s[%d]' % (child.name, 1 + siblings.index(child))
        )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


class NkonLionSpider(scrapy.Spider):
    name = "nkon_dataXpaths"
    allowed_domains = ["eu.nkon.nl"]
    # start_urls = ["https://eu.nkon.nl/rechargeable/lifepo4.html"]
    start_urls = ["https://eu.nkon.nl/rechargeable/li-ion.html", "https://eu.nkon.nl/rechargeable/lifepo4.html"]
    cur_url = None
    count = 0

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        }
    }

    def parse(self, response, **kwargs):
        for url in LinkExtractor(unique='true', restrict_css='.item').extract_links(response):
            self.cur_url = url
            yield scrapy.Request(url.url, callback=self.parseDetail)
        # create_csv()

    def parseDetail(self, response):
        self.count += 1
        html = response.xpath('/*').get()
        # soup = BS(html, 'html.parser')
        soup = BS(html, features="lxml")

        # ================== Voltage ======================================================

        elem = soup.find(name="th", string=re.compile('Voltage'))
        if (elem):
            voltLabelXpath = xpath_soup(elem)
            voltageXpath = voltLabelXpath.replace("th", "td/text()")
            voltage = response.xpath(voltageXpath).get()
            if voltage:
                voltage = voltage.strip()
        else:
            voltage = "notFound"


        # ================== chemistry ======================================================Size

        elem = soup.find(name="th", string=re.compile('Battery chemistry'))

        if (elem):
            chemistryLabelXpath = xpath_soup(elem)
            chemistryXpath = chemistryLabelXpath.replace("th", "td/text()")
            chemistry = response.xpath(chemistryXpath).get()

            if chemistry:
                chemistry = chemistry.strip()
        else:
            chemistry = "notFound"


        # ================== size ======================================================Battery version

        elem = soup.find(name="th", string=re.compile('Size'))

        if (elem):
            sizeLabelXpath = xpath_soup(elem)
            sizeXpath = sizeLabelXpath.replace("th", "td/text()")
            size = response.xpath(sizeXpath).get()

            if size:
                size = size.strip()
        else:
            size = "no Size"

        # ================== batType ======================================================Battery version

        elem = soup.find(name="th", string=re.compile('Battery version'))

        if (elem):
            batTypeLabelXpath = xpath_soup(elem)
            batTypeXpath = batTypeLabelXpath.replace("th", "td/text()")
            batType = response.xpath(batTypeXpath).get()

            if batType:
                batType = batType.strip()
        else:
            batType = "notFound"



        # ================== Brand ======================================================

        elem = soup.find(name="th", string=re.compile('Brand'))

        if elem:
            brandLabelXpath = xpath_soup(elem)
            brandXpath = brandLabelXpath.replace("th", "td/text()")
            brand = response.xpath(brandXpath).get()

            if brand:
                brand = brand.strip()
        else:
            brand = "notFound"

        # ================== Weight g ======================================================

        elem = soup.find(name="th", string=re.compile('Weight - g'))
        weightGm = "No Wght"
        if elem:
            weightGmLabelXpath = xpath_soup(elem)
            weightGmXpath = weightGmLabelXpath.replace("th", "td/text()")
            weightGm = response.xpath(weightGmXpath).get()
            weightGm = weightGm.strip()
        else:
            weightGm = "unkown"

        # ================== Min. capacity - mAh ======================================================

        elem = soup.find(name="th", string=re.compile('Min. capacity - mAh'))
        minCapacity_mAh = "Not found"
        if elem:
            minCapacity_mAhLabelXpath = xpath_soup(elem)
            minCapacity_mAhXpath = minCapacity_mAhLabelXpath.replace("th", "td/span/    text()")
            minCapacity_mAh = response.xpath(minCapacity_mAhXpath).get()

            if minCapacity_mAh:
                minCapacity_mAh = minCapacity_mAh.strip()
            # else:
            #     minCapacity_mAh = "Not found"



        # ================== PRICE ======================================================Weight - g

        # for price in prices:
        #     print(price)
        #     print(price.text.replace('â‚¬', '\u20ac'))
        price = "notFound"
        # elem = soup.find(name="th", string=re.compile('Price'))
        elem = soup.find('span', attrs={"itemprop": "price"})
        if elem:
            priceXpath = xpath_soup(elem)
            # priceXpath = priceLabelXpath.replace("th", "td/text()")
            price = re.match(r'\A.(\d+\.\d+)',elem.text).group(1)
            price = price
        else:
            price = "notFound"

# =================================== Bulk prices ================================

        rePat = re.compile(r'Buy (\d+) times for €(\d+\.\d+) \(€(\d+\.\d+) (.*)')
        bulkPrices = []
        debug = 0
        myElems = soup.find_all("li")
        for elem in myElems:
            ans = re.match(rePat, elem.text.strip())
            if ans:
                debug += 1
                bulkPrices.append(ans.group(1) + ' ' + '@' + ' ' + ans.group(2) + ' ')
                # print(elem.text.strip().replace('â‚¬', '\u20ac'))
        if len(bulkPrices) > 0:
            bulkPrice = '%s' % ' '.join(bulkPrices)
        else:
            bulkPrice = "No Bulk price"

# ================== Capacity ======================================================

        elem = soup.find(name="th", string=re.compile('Capacity - Ah'))

        if elem:
            capacityLabelText = 'Capacity - Ah'
        else:
            elem = soup.find(name="th", string=re.compile('Typ. capacity - mAh'))
            if elem:
                capacityLabelText = 'Typ. capacity - mAh'
            else:
                capacityLabelText = 'no capacity'

        if elem:
            capacityLabelXpath = xpath_soup(elem)
            capacityXpath = capacityLabelXpath.replace("th", "td/span/text()")
            capacity = response.xpath(capacityXpath).get()

            if capacity:
                capacity = capacity.strip()
        else:
            capacity = "no capacity2"

        # print(len(scrapy.Item))
        if bulkPrice != "No Bulk price" and bulkPrice:
            lcPrice = re.search(r'(\d+.\d+)(?!.*\d)', bulkPrice).group()
        else:
            lcPrice = price
        if capacityLabelText == 'Typ. capacity - mAh':
            capacityAh = float(capacity.strip().replace(',', ''))/1000
        elif capacity != 'no capacity2':
            capacityAh =float(capacity.strip().replace(',',''))

        yield {
            # "count": self.count,
            "Brand": brand,
            "WeightGm":  weightGm,
            "Price": price,
            "Bulk Prices": bulkPrice,
            'LC KwH' : '%.2f' % getKwHcost(lcPrice, capacityAh, float(voltage.replace('V','')),NumCells4ReqVoltage=16),
            "debug": debug,
            "Voltage": voltage,
            "CapacityLabelText": capacityLabelText,
            "Capacity": capacity,
            "MinCapacity_mAh":  minCapacity_mAh,
            "chemistry": chemistry,
            "Size" : size,
            "Battery Type": batType,

        }
        # raise CloseSpider('readyToStop_exceeded')
