# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request



class Login(scrapy.spiders.Spider):
    name = "login"
    allowed_domains = [
        "https://www.amazon.cn/"
    ]
    urls = [
        "https://www.amazon.cn/?tag=baidu250-23&hvadid={creative}&ref=pz_ic_22fvxh4dwf_e",
        'https://www.amazon.cn/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=cnflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2F%3Fnocache%3D1524450292375%26ref_%3Dnav_ya_signin&switch_account='
    ]

    def start_requests(self):

        yield Request(url=self.urls[0], callback=self.parse, dont_filter=True)
    def parse(self,response):

        with open('2.html', 'wb') as f:
            f.write(response.body)
