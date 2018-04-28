# -*- coding:utf-8 -*-

import scrapy
from Spider0418 import items
from scrapy import Request
import sys
from scrapy.conf import settings


reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderQiushi(scrapy.Spider):
    name = "News"

    allowed_domains = ['news.dailyqd.com']
    start_urls = [
        'http://news.dailyqd.com/node_3118.htm',
        # 'http://news.dailyqd.com/node_3118_3.htm',
    ]

    cookie = settings['COOKIE']  # 带着Cookie向网页发请求

    # def start_requests(self):
    #     yield Request(url=self.start_urls[0],  cookies=self.cookie)  # 这里带着cookie发出请求


    def parse(self, response):
        Cookie = response.request.headers.getlist('Cookie')
        # print 'Cookie', Cookie
        """
        pageNodes = response.xpath('//*[@id="displaypagenum"]/center/a')
        print('****************************')
        npage1 = response.xpath('//*[@id="displaypagenum"]/center/a[%s]/@href'%len(pageNodes)).extract()
        pco = response.xpath('//*[@id="displaypagenum"]/center/a[%s]/text()'%len(pageNodes)).extract()
        print(pco)
        npage2 = [str(i) for i in npage1]
        npage = ''.join(npage2)
        next_url = "http://news.dailyqd.com/" + npage
        print(next_url)
        """
        pageNodes = response.xpath('//*[@id="displaypagenum"]/center/a/@href').extract()
        # print(pageNodes)
        pagenode = pageNodes[-1]
        next_url = "http://news.dailyqd.com/" + pagenode


        for j in range(1,5):
            lists1 = response.xpath('//div[@class="maincon_left_top"]/div[%s]'%j)

            for list1 in lists1:
                for i in range(1,6):
                    item = items.Spider0418Item()
                    img_url = list1.xpath('.//ul/li[%s]/div[1]/a/@href'%i).extract()
                    item['title'] = list1.xpath('.//ul/li[%s]/div[1]/a/text()'%i).extract()
                    item['date'] = list1.xpath('.//ul/li[%s]/span/text()'%i).extract()
                    url1 = img_url
                    url2 = [str(i) for i in url1]
                    # print(url2)
                    url3 = ''.join(url2)
                    # print(url3)
                    # print(type(url3))
                    iurl = 'http://news.dailyqd.com/'+ url3
                    item['url'] = iurl
                    print(iurl)
                    # yield item
                    yield Request(url=item['url'], meta={'key': item},cookies=self.cookie, callback=self.parse2)

        # if npage1 == [u'\u4e0b\u4e00\u9875']:
        yield Request(url=next_url, cookies=self.cookie, callback=self.parse)

    def parse2(self,response):
        """
            这个response已含有上述meta字典，此句将这个字典赋值给item，
            完成信息传递。这个item已经和parse中的item一样了
        """
        item = response.meta['key']
        contentlist = []
        imgurl = []
        i = 1

        bodys = response.xpath('//div[@class="left_text_box"]/p')
        for body in bodys:
            if bodys.xpath('//div[@class="left_text_box"]/p[%s]/text()' % i).extract():
                list = body.xpath('//div[@class="left_text_box"]/p[%s]/text()' % i).extract()
                i += 1
                contentlist.extend(list)
            elif body.xpath('//div[@class="left_text_box"]/p[%s]/strong/text()' % i).extract():
                list = body.xpath('//div[@class="left_text_box"]/p[%s]/strong/text()' % i).extract()
                i += 1
                contentlist.extend(list)
            else:
                list = body.xpath('//div[@class="left_text_box"]/p[%s]/img/@src'% i).extract()
                i += 1
                contentlist.extend(list)
                imgurl.extend(list)
        item['content'] = contentlist
        item['image_urls'] = imgurl
        yield item



"""
[u'\u4e0b\u4e00\u9875']
[u'\u4e0b\u4e00\u9875']


[u'19']
http://news.dailyqd.com/node_3118_19.htm
http://news.dailyqd.com/2017-11/21/content_411149.htm
http://news.dailyqd.com/2017-11/21/content_411151.htm
http://news.dailyqd.com/2017-11/21/content_411150.htm
http://news.dailyqd.com/2017-11/21/content_411148.htm
http://news.dailyqd.com/2017-11/21/content_411147.htm
http://news.dailyqd.com/2017-11/21/content_411146.htm
http://news.dailyqd.com/2017-11/21/content_411144.htm
http://news.dailyqd.com/2017-11/21/content_411101.htm
http://news.dailyqd.com/2017-11/21/content_411099.htm
http://news.dailyqd.com/2017-11/21/content_411095.htm
http://news.dailyqd.com/2017-11/21/content_411090.htm
http://news.dailyqd.com/2017-11/21/content_411091.htm
http://news.dailyqd.com/2017-11/21/content_411019.htm
http://news.dailyqd.com/2017-11/21/content_411028.htm
http://news.dailyqd.com/2017-11/21/content_411022.htm
http://news.dailyqd.com/2017-11/21/content_411024.htm
http://news.dailyqd.com/2017-11/20/content_410924.htm
http://news.dailyqd.com/2017-11/20/content_410881.htm
http://news.dailyqd.com/2017-11/20/content_410815.htm
http://news.dailyqd.com/2017-11/20/content_410804.htm


[u'\u4e0b\u4e00\u9875']
http://news.dailyqd.com/node_3118_20.htm
http://news.dailyqd.com/2017-11/23/content_411374.htm
http://news.dailyqd.com/2017-11/23/content_411352.htm
http://news.dailyqd.com/2017-11/23/content_411348.htm
http://news.dailyqd.com/2017-11/23/content_411347.htm
http://news.dailyqd.com/2017-11/22/content_411303.htm
http://news.dailyqd.com/2017-11/22/content_411244.htm
http://news.dailyqd.com/2017-11/22/content_411240.htm
http://news.dailyqd.com/2017-11/22/content_411235.htm
http://news.dailyqd.com/2017-11/22/content_411200.htm
http://news.dailyqd.com/2017-11/22/content_411202.htm
http://news.dailyqd.com/2017-11/22/content_411196.htm
http://news.dailyqd.com/2017-11/21/content_411169.htm
http://news.dailyqd.com/2017-11/21/content_411167.htm
http://news.dailyqd.com/2017-11/21/content_411165.htm
http://news.dailyqd.com/2017-11/21/content_411166.htm
http://news.dailyqd.com/2017-11/21/content_411162.htm
http://news.dailyqd.com/2017-11/21/content_411157.htm
http://news.dailyqd.com/2017-11/21/content_411156.htm
http://news.dailyqd.com/2017-11/21/content_411153.htm
http://news.dailyqd.com/2017-11/21/content_411152.htm

"""