# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from scrapy import cmdline

cmdline.execute('scrapy crawl News'.split())