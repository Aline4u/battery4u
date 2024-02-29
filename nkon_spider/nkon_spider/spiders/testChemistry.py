import re

chemistryList = [" 18650", " LIFEPO4"]

for c in chemistryList:
    if re.match(r'\d+', c.strip() ):
        continue
    else:
        print(c.strip())
print('finished')