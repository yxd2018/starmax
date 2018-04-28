import sys
from scrapy import cmdline

reload(sys)
sys.setdefaultencoding('utf-8')


cmdline.execute('scrapy crawl login'.split())