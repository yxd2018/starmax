# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
from urllib import quote
from Spdertaobao.items import SpdertaobaoItem
import sys
import random

from Spdertaobao import settings
reload(sys)
sys.setdefaultencoding('utf-8')


class taobaoSpider(scrapy.spiders.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    base_url = ['https://s.taobao.com/search?q=']
    header = random.choice(settings.MY_USER_AGENT)
    ip = random.choice(settings.IPPOOL)


    def start_requests(self):
        for keyword in self.settings.get('KEYWORDS'):
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = self.base_url[0] + quote(keyword)
                yield Request(url=url, callback=self.parse,meta={'proxy':self.ip, 'User-Agent':self.header, 'page':page} ,dont_filter=True)

    def parse(self, response):
        # with open('2.txt', 'wb') as f:
        #     f.write(response.body)
        print('1')
        item = SpdertaobaoItem()

        for i in range(1,3):
            # products = response.xpath('//div[@class="grid g-clearfix"]/div[i]' % i).extract()
            products = response.xpath('//div[@id="mainsrp-itemlist"]//div[@class="items"][%s]//div[contains(@class, "item")]'%i)
            # print(len(products))
            # print(products)
            for product in products:
                pic_url = ''.join(product.xpath('//div[contains(@class, "pic")]//img[contains(@class,img)]/@src').extract()[0]).strip()
                price = ''.join(product.xpath('.//div[contains(@class, "price")]//text()').extract()).strip()
                deal = ''.join(product.xpath('.//div[contains(@class,"deal-cnt")]//text()').extract()).strip()
                shop = ''.join(product.xpath('.//div[contains(@class,"shop")]//text()').extract()).strip()
                title = ''.join(product.xpath('.//div[contains(@class,"title")]//text()').extract()).strip()

                # print(pic_url,price,deal,shop,title)
                item['pic_url'] = pic_url
                item['price'] = price
                item['deal'] = deal
                item['shop'] = shop
                item['title'] = title
                yield item



