# -*- coding:utf-8 -*-
from scrapy import cmdline
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


cmdline.execute('scrapy crawl taobao'.split())