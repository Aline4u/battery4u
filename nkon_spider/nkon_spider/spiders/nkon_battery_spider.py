import string
from math import ceil
# from typing import Any
import scrapy
from scrapy.linkextractors import LinkExtractor
import re
from numpy.core.defchararray import isnumeric


keepNumOrDotPat = re.compile('[^0-9.]')
keepNumPat = re.compile('[^0-9]')
debug = ''
debugOn = True
reqVoltage = float(51.2)


def getenergyPerCell(voltage, capacity_Ah):
    return float(voltage) * capacity_Ah


def getKwHcost(priceIn, capacity, voltage: float, NumCells4ReqVoltage: float):
    capacity_Ah: float = capacity/1000
    price = float(priceIn)
    energyPerCell =  getenergyPerCell(voltage,capacity_Ah) #Energy per cell in watts
    cells1Kw = 1000/energyPerCell
    Cost1Kw = cells1Kw * price
    return Cost1Kw

def getWatts4Conf(cellVoltage, mAh, series, parallel,):
    ah = mAh/1000
    return cellVoltage * ah * parallel * series

def getMinCost(price, voltage):
    numCells4ReqVolt = ceil(reqVoltage / float(voltage))
    return numCells4ReqVolt * float(price)
def getKwh4MinCost(capacity):
    return reqVoltage * (capacity / 1000) / 1000


def doesNotContain(avoidList, ans):
    if ans == avoidList:
        return False
    for item2Exclude in avoidList:
        if re.match(item2Exclude, ans):
            return False

    return True


def getValues(response, listXpaths, val2Exclude=['blablabla']):
    ans = list(())
    for path in listXpaths:
        val = response.xpath(path).get()
        if val and doesNotContain(val2Exclude, val) and val != " ":
            ans.append(val)

    if len(ans) >= 1:
        return ans
    else:
        return None


def getAllValues(response, listXPaths):
    ans = list(())
    for path in listXPaths:
        val = response.xpath(path).get()
        if val:
            ans.append(val.strip())
        else:
            ans.append("notSet")
    return ans

def getVoltageFromList(voltageList):
    if voltageList:
        for v in voltageList:
            if v:
                v = v.strip().replace('V', '')
                if re.match(r"\d\.\d", v):
                    return float(v)
    else:
        return None


def removeThis(pattern, stringIn: string):
    if isinstance(stringIn, str):
        return re.sub(pattern, '', stringIn)
    return stringIn


def getNumCells4ReqVoltage(voltage):
    return float(ceil(reqVoltage / float(voltage)))


def getSmallestPrice(lowPriceList):
    lPrice = float(10000)
    p = ''
    for price in lowPriceList:
        if not isinstance(price, float):
            p = removeThis(keepNumOrDotPat, price)
        if float(p) < float(lPrice):
            lPrice = p
    return lPrice


def getNumber(valueList, pattern=keepNumPat):
    if valueList:
        for n in valueList:
            b = removeThis(pattern, n)
            if isnumeric(b):
                return float(n.replace(',', ''))
    return None


def isValidItem(item, validItemList):
    for i in validItemList:
        ans = re.match(i, item, re.IGNORECASE)
        if ans:
            return True
    return False


def getExpWithlargestInt(valueList):
    num = 0
    if not valueList:
        return "No offers"
    for item in valueList:
        match = re.search(r'\d+', item)
        n = int(match.group())
        if num < n:
            num = n

    return "Buy " + str(num) + " times for "


def createUrl(current_url, text):
    return "<a href=""" + current_url + " \">  " + text + "</a>"


def getIndex(response, labelXPaths, searchKey):
   ind = 0
   for xpath in labelXPaths:
       label = response.xpath(xpath).get()
       if label == searchKey:
           return ind
       else:
           ind += 1
   return None

def getIndex2(labelList, searchKey):
   ind = 0
   for label in labelList:
       if label.strip() == searchKey:
           return ind
       else:
           ind += 1
   return None


def getWattsPerKG(capacity, NumCells4ReqVoltage, weightPerCell):
    if weightPerCell == 0:
        return 'TBA'
    TotalCap = getKwh4MinCost(capacity)
    totalWeightKG = (NumCells4ReqVoltage*(weightPerCell/1000))
    return (TotalCap/totalWeightKG)*1000

# from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging

# *********************************************** Start Class *********************************************************
class NkonLionSpider(scrapy.Spider):
    name = "nkon_battery"
    allowed_domains = ["eu.nkon.nl"]
    # settings = get_project_settings()

    # start_urls = ["https://eu.nkon.nl/rechargeable/lifepo4.html"]
    # start_urls = ["https://eu.nkon.nl/rechargeable/li-ion.html", "https://eu.nkon.nl/rechargeable/lifepo4.html"]
    start_urls = [ "https://eu.nkon.nl/rechargeable/lifepo4.html"]
    cur_url = None

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        },
        'FEED_FORMAT': 'json',
        # Change the FEED_URI to output.json
        # 'FEED_URI': '../LiionOutput.json'
        'FEED_URI': '../outputLIFEPO4.json'
        # 'FEED_URI': '../AllOutput.json'

    }




    if __name__ == "__main__":
        process = CrawlerProcess(custom_settings)
        process.crawl(crawler_or_spidercls="nkon_battery")
        process.start()

        # configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
        # runner = CrawlerRunner()
        # d = runner.crawl(MySpider)
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run()



        # Start the crawler with the spider name


    # Run the crawler


    # def __init__(self, category2=None, *args, **kwargs):
    #     super(NkonLionSpider, self).__init__(*args, **kwargs)
    #     print(category2)
    #     # self.start_urls = ['http://www.example.com/categories/%s' % category]
    def parse(self, response, **kwargs):
        for url in LinkExtractor(unique='true', restrict_css='.item').extract_links(response):
            self.cur_url = url
            yield scrapy.Request(url.url, callback=self.parseDetail)
        # create_csv()

    def parseDetail(self, response):
        #  = self.cur_url
        productUrl = response.request.url
        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&# AmpHours or milli Amp #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&
        ampHrsLabelXpaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/span/../../th/text()",
                             "// * [ @ id = 'product-attribute-specs-table'] / tbody / tr[8] / th / text()",
                             "//*[@id='product-attribute-specs-table']/tbody/tr[6]/th/text()"]
        ampHrsLabelList = getValues(response, ampHrsLabelXpaths)
        isAmpHrs = False
        if ampHrsLabelList is not None:
            for label in ampHrsLabelList:
                if label == 'Capacity - Ah':
                    isAmpHrs = True
                    # isMilliAmp = False
                elif label == 'Min. capacity - mAh':
                    isAmpHrs = False
                # isMilliAmp = True
        # debug = ampHrsLabel

        # capacity = None
        # CapacityLabel = 'Min. capacity - mAh'
        capacityXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/span/text()",
                          "//*[@id='product-attribute-specs-table']/tbody/tr[8]/td/span/text()"]

        capacityList = getValues(response, capacityXPaths)

        capacity = getNumber(capacityList)

        # if (response.xpath("//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/span/text()").get()):
        #     capacity = response.xpath("//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/span/text()").get()
        # if (not capacity):
        #     capacity = response.xpath().get()

        if not capacity:
            capacity = .000000001

        if isAmpHrs:
            capacity = capacity * 1000
            # CapacityLabel = 'Capacity - Ah'

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&# Price #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&&&&&&&&&&&&&&&&&&&&&
        price = response.xpath("//span[@class='price'] [@itemprop='price']/text()").get()
        if price:
            price = price.strip()
        # debug =''

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&# Brand #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&&&&&&&&&&&&&&&&&&&&&
        brand = 'TBA'
        brandXPaths = ['//*[@id="product-attribute-specs-table"]/tbody/tr[3]/td/text()']
        brandList = getValues(response, brandXPaths)
        if brandList is not None:
            brand = brandList[0]
            if brand:
                brand = brand.strip()

    # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&# Model &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&#&&&&&&&&&&&&&&&&&&&
        model = ''
        modelXPaths = ["// * [ @ id='product-attribute-specs-table'] / tbody / tr[4] / td/text()"]
        modelList = getValues(response, modelXPaths,val2Exclude='Time2Stop')
        if modelList is not None:
            if modelList[0]:
                model = modelList[0].strip()
# /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ BatType @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if model.find('18650') >= 0 or productUrl.find('18650') >= 0:
            battype = '18650'
        elif model.find('21700') >= 0 or productUrl.find('21700') >= 0:
            battype = '21700'
        elif model.find('20700') >= 0:
            battype = '20700'
        else: battype = 'TBA'
# /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ AmpHrs @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        AmpHrs = 0
        AmpHrsXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[10]/td/span/text()",
                        "// *[ @ id = 'product-attribute-specs-table'] / tbody / tr[8] / td / span/text()"]
        AmpHrsList = getValues(response, AmpHrsXPaths)
        if AmpHrsList is not None:
            AmpHrs = AmpHrsList[0]
# /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ discharge label @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        dischargeLabelXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[7]/th/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[8]/th/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[10]/th/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[11]/th/text()"]
        searchKey = "Discharge current - A"
        dischargeLabelIndex = getIndex(response,dischargeLabelXPaths,searchKey)

# /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ discharge Amps @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

        dischargeAmpXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/span/text()",
                              "//*[@id='product-attribute-specs-table']/tbody/tr[8]/td/span/text()",
                              "//*[@id='product-attribute-specs-table']/tbody/tr[10]/td/span/text()",
                              "//*[@id='product-attribute-specs-table']/tbody/tr[11]/td/span/text()"]
        dischargeAmpList = getAllValues(response, dischargeAmpXPaths)
        # debug = dischargeAmpList
        if dischargeAmpList and dischargeLabelIndex:
            # dischargeAmp = getNumber(dischargeAmpList,keepNumOrDotPat)
            dischargeAmp = dischargeAmpList[dischargeLabelIndex]
        else:
            dischargeAmp = "Not set"


        lowpriceXPaths = ["//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[4]/span[1]/text()",
                          "/html/body/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div/form/div[3]/div/div[2]/ul/li[2]/span[1]/text()",
                          "//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[3]/span[1]/text()"]

        lowPriceList = getValues(response, lowpriceXPaths)
        # debug = lowPriceList
        if lowPriceList:
            lowPrice = getSmallestPrice(lowPriceList)
        else:
            lowPrice = '£10000'

        lowPriceReqQtyXPaths = ["//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[3]/text()",
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[2]/text()",
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/p/span/font/font/b/text()"
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[2]/text()",
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/ul/li[4]/span[1]/parent ::*/text()"]

        lowPriceQtyReqList = getValues(response,lowPriceReqQtyXPaths)

        # debug = lowPriceQtyReqList

        lowPriceQtyReq = getExpWithlargestInt(lowPriceQtyReqList)

        if lowPriceQtyReq:
            lowPriceQtyReq = lowPriceQtyReq.strip()

        availabilityXPaths =["//*[@id='product_addtocart_form']/div[3]/div/div[2]/p/span/font/text()",
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/p/span/text()",
                             "//*[@id='product_addtocart_form']/div[3]/div/div[2]/p/span/font/font/b/text()"]

        availabilityList  = getValues(response, availabilityXPaths)
        if availabilityList is None:
            availability = "No Cur Availability"
        elif len(availabilityList) == 1:
            availability = availabilityList[0]
        else:
            availability = "not Sure"
        # debug = availabilityList
        weightPerCell = 98760
        weightXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()"]
        weightlist = getValues(response, weightXPaths)
        if weightlist is not None:
            weightPerCell = float(weightlist[0])


        price = removeThis(keepNumOrDotPat, price)
        if lowPrice == '£10000':
            lowPrice = price
        else:
            lowPrice = removeThis(keepNumOrDotPat, lowPrice)


        chemistryLabelXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[4]/td/font/font/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[4]/th/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[5]/td/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[5]/th/text()",
                                "//*[@id='product-attribute-specs-table']/tbody/tr[6]/th/text()"
                                ]

        chemistryLabelList = getAllValues(response, chemistryLabelXPaths)

        # debug = chemistryLabelList

        chemistry = ''
        chemistryXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[4]/td/font/font/text()",
                           "//*[@id='product-attribute-specs-table']/tbody/tr[4]/td/text()",
                           "//*[@id='product-attribute-specs-table']/tbody/tr[5]/td/text()",
                           "//*[@id='product-attribute-specs-table']/tbody/tr[5]/td/text()",
                           "//*[@id='product-attribute-specs-table']/tbody/tr[6]/td/text()"
                           ]

        chemistryList = getAllValues(response, chemistryXPaths)
        searchKey = "Battery chemistry"
        chemistryLabelIndex = getIndex2(chemistryLabelList,searchKey)

        # if chemistryLabelIndex:
        #     debug = chemistryList[chemistryLabelIndex]
        # else:
        #     debug = chemistryLabelList.append(chemistryLabelIndex)#'None chemistryLabelIndex'

        aVoltage = ''
        # debug = chemistryList
        validChemistries = ["LIFEPO4", "Li-ion", "LTO"]
        if chemistryList is not None and chemistryLabelIndex is not None :
            if len(chemistryList) > 0 and chemistryList:
                chemistry = chemistryList[chemistryLabelIndex]
            else:
                for chem in chemistryList:
                    if chem and re.match(r'\d+', chem.strip()):
                        if re.match('3.2V', chem):
                            chemistry = '_Li-ion'
                            aVoltage = 3.20001
                        elif re.match('3.6V', chem):
                            chemistry = '_LIFEPO4'
                            aVoltage = 3.6000002
                        elif isValidItem(chem, validChemistries):
                            chemistry = chem
                            break
                        continue
                    else:
                        chemistry = chem

        # debug = chemistryList

        if chemistry and not chemistry == '':
            chemistry = chemistry.strip()
        else:
            chemistry = '_Unknown'
#=============================================================== Voltage =============================================

        voltageLabelXPaths =["//*[@id='product-attribute-specs-table']/tbody/tr[7]/th/text()",
                             "//*[@id='product-attribute-specs-table']/tbody/tr[6]/th/text()",
                             "//*[@id='product-attribute-specs-table']/tbody/tr[5]/th/text()"
                            ]
        voltageLabelList = getAllValues(response, voltageLabelXPaths)

        searchKey = "Voltage"

        voltageLabelIndex = getIndex2(voltageLabelList, searchKey)

        # debug = voltageLabelList[voltageLabelIndex]
        debug = voltageLabelIndex

        voltage = None
        voltageList = None

        voltageXPaths = ["//*[@id='product-attribute-specs-table']/tbody/tr[7]/td/text()",
                         "//*[@id='product-attribute-specs-table']/tbody/tr[6]/td/text()",
                         "//*[@id='product-attribute-specs-table']/tbody/tr[5]/td/text()"]


        voltageList = getAllValues(response, voltageXPaths)

        if voltageLabelIndex is not None:
            voltage = voltageList[voltageLabelIndex].strip().replace('V','')



        # voltage = float(removeThis('V', voltage).strip())





        if voltage is None:
            if re.match('Li-ion', chemistry):
                voltage = '3.599555'
            elif re.match('LIFEPO4', chemistry):
                voltage = '3.199555'
            else:
                voltage = '3.5995551234'

        NumCells4ReqVoltage = float(getNumCells4ReqVoltage(voltage))

        # desiredChemistry = 'Li-ion'
        # desiredChemistry = 'LIFEPO4'
        desiredChemistry = 'all'

        if (chemistry == desiredChemistry or desiredChemistry == 'all') and availability != 'Out of stock':
            yield {
                # "Debug": voltageList,
                "Product url": productUrl,
                "Brand": brand,
                "Model": model,
                "Type": battype,
                "Price": price,
                "Capacity - mAh": capacity,
                "EnergyPerCell - Watts": '%.2f' % getenergyPerCell(voltage,capacity/1000),
                "Max Discharge A": dischargeAmp,
                "Num Cells4V": NumCells4ReqVoltage,
                "Weight": weightPerCell,
                "Current Ah": AmpHrs,
                "min Cost":  '%.2f' % getMinCost(price, voltage),
                "Kwh for Min cost": '%.2f' % getKwh4MinCost(capacity),
                "Chemistry": chemistry,
                "Voltage": voltage,
                "availability": availability,
                "Cost KwH": '%.2f' % getKwHcost(price, capacity, voltage, NumCells4ReqVoltage),
                "LowPriceQty": lowPriceQtyReq,
                "LowPrice": lowPrice,
                "Density W/KG":'%.2f' % getWattsPerKG(capacity,NumCells4ReqVoltage, weightPerCell) ,
                "LC Min Price": '%.2f' % getMinCost(lowPrice, voltage),
                "LC KwH": '%.2f' % getKwHcost(lowPrice, capacity, voltage, NumCells4ReqVoltage)


            }
        # raise CloseSpider('readyToStop_exceeded')
