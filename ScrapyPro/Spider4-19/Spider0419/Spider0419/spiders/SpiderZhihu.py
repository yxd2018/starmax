# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request
from selenium import webdriver



class Spider0419(scrapy.Spider):

    name = "Zhihu"
    allowed_domains = [
        'www.baidu.com'
    ]
    url = [
        'https://www.amazon.cn/?tag=baidu250-23&hvadid={creative}&ref=pz_ic_22fvxh4dwf_e',
    ]
    def start_requests(self):
        yield Request(url=self.url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        pass