
from scrapy import cmdline

# cmdline.execute("scrapy crawl nkon_battery -o outputLiion.json".split())

cmdline.execute([
    'scrapy', 'crawl', 'nkon_battery',
    '-a', '-o outputLiion.json'])

