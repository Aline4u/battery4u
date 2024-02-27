import re


validChemistries = ['LIFEPO4','Li-ion','LTO']


# a = re.match(validChemistries, 'LIFEPO4',re.IGNORECASE)

def isValidItem(item, validItemList):
    for i in validItemList:
        ans = re.match(i, item,re.IGNORECASE)
        if(ans):
            return True
    return None



print(isValidItem('LIFEPO4',validChemistries))