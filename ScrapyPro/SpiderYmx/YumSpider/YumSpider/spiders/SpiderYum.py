# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request,FormRequest
from YumSpider.items import YumspiderItem


class Spider02(scrapy.Spider):
    name = "Yumspider"
    allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.cn/?nocache=1524447213472',
    ]



    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.login, dont_filter=True)


    def login(self,response):
        data = {
            "__mk_zh_CN": "亚马逊网站",
            "url": "search - alias = aps",
            "field - keywords": "ipad"
        }
        login_request = FormRequest.from_response(
            response,
            # meta={"cookiejar": response.meta["cookiejar"]},  # 使用上面带来的cookie
            formdata=data,
            callback=self.parse,
            dont_filter=True
        )
        yield login_request
    def parse(self, response):
        pass
        """
        item = YumspiderItem()
        bodys = response.xpath('//*[@id="atfResults"]')
        for body in bodys:
            # print(body)
            #result_1
            item['img_url'] = body.xpath('.//*[@id="result_1"]/div/div[2]/div/div[1]/div/div/a/img/@src').extract()
            item['title'] = body.xpath('.//*[@id="result_1"]/div/div[2]/div/div[2]/div[1]/div[1]/a/h2/text()').extract()
            # item['price'] = body.xpath('.//*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[1]/text()').extract()
            price01 = body.xpath(
                '//*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/sup[1]/text()')
            price02 = body.xpath(
                '//*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/span/text()')
            price03 = body.xpath(
                '//*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[2]/span/sup[2]/text()')
            item['price'] = int(str(price01) + str(price02) + '.' + str(price03))



            yield item

        """