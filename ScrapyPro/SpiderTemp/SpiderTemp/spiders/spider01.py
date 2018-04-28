# -*- coding:utf-8 -*-

import scrapy
from SpiderTemp import items
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Spider01(scrapy.Spider):
    name = "spiderip"
    allowed_domains = ["66ip.cn"]
    start_urls = [
        "http://www.66ip.cn/",
    ]

    def parse(self, response):
        item = items.SpidertempItem()
        tbodys = response.xpath('//*[@id="main"]/div/div[1]/table')
        print(response.url)
        for ip in tbodys:
            for i in range(2,13):
                item['ip'] = ip.xpath('.//tr[%s]/td[1]/text()'%i).extract()
                item['port'] = ip.xpath('.//tr[%s]/td[2]/text()'%i).extract()
                item['location'] = ip.xpath('.//tr[%s]/td[3]/text()'%i).extract()
                item['type'] = ip.xpath('.//tr[%s]/td[4]/text()'%i).extract()
                item['date'] = ip.xpath('.//tr[%s]/td[5]/text()'%i).extract()
                yield item
                # print(item)

        """
        # url跟进开始
        # 获取下一页的url信息     //*[@id="PageList"]/a[16]
        url = response.xpath('//*[@id="PageList"]/a[13]/@href').extract()
        if url:
            # 将信息组合成下一页的url
            page = 'http://www.66ip.cn' + url[0]
            # 返回url
            yield scrapy.Request(page, callback=self.parse)
        # url跟进结束
        """
        for j in range(2,10):
            url = '%s.html'%j
            page = 'http://www.66ip.cn/' + url
            yield scrapy.Request(page,callback=self.parse)
