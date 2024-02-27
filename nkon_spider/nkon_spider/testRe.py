import re
import string
from array import array
import numpy as np
# from pandas.core.computation.ops import isnumeric

from numpy.core.defchararray import isnumeric

keepNumPat = re.compile('[^0-9]')
stringIn = '3.2vaaaa'
bla = np.array(['3.2'])
# print('is number 3.2 '+ str(isnumeric(bla)))

# if re.match('3.2V', stringIn):
#             stringIn = '_Li-ion'

 # '/[^0-9.]*/g'

pat = re.compile('[^0-9.]')
# stringIn.replace('[\D]/g','')

# print(re.sub(pat,'',stringIn))

def removeThis(pattern, stringIn: string):
    if(isinstance(stringIn,str)):
        print('is string true')
        return re.sub(pattern,'',stringIn)
    return stringIn

def getSmallestPrice(lowPriceList):
    lPrice = float(110)
    for price in lowPriceList:
        if not isinstance(price,float):
            p = removeThis(keepNumPat,price)
        if float(p) < float(lPrice):
            lPrice = p
    return lPrice


testLowPricelist = ['€95.95', '€97.95', '€96.95']

# print(getSmallestPrice(testLowPricelist))


def getNumber(valueList):
    for n in valueList:
        print(n)
        b = removeThis(keepNumPat, n)
        print(b)
        if ( isnumeric(b)):
            return n
    return None

print(getNumber(np.array(['43.2'])))

