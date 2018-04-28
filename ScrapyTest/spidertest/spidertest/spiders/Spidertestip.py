# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from spidertest import settings
import random

class iptest(scrapy.spiders.Spider):
    name = "test"
    allowed_domains = ["ip.filefab.com"]
    start_urls = ["http://ip.filefab.com/index.php"]
    ip = random.choice(settings.IPPOOL)

    def start_request(self):
        yield Request(url=self.start_urls[0],meta={'proxy':self.ip},callback=self.parse)
        #//div[contains(@class, "pic")]//img[contains(@class,img)]/@src

    def parse(self,response):
        # p = response.xpath('//div[contanins(@class="notediv)]"//span//text()').extract()
        print(1)