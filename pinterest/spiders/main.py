from scrapy import cmdline

# cmdline.execute("scrapy crawl pinterest_spider -s JOBDIR=crawls/pinterest_spider-1".split())
cmdline.execute("scrapy crawl pinterest_spider".split())

