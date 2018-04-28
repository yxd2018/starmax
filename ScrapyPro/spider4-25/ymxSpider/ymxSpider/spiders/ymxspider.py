# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request
import json


class spiderymx(scrapy.spiders.Spider):
    name = "ymx_cookie"
    allowed_domains = [
        'www.amazon.cn'
    ]
    start_urls = [
        "https://www.amazon.cn/?tag=baidu250-23&hvadid={creative}&ref=pz_ic_22fvxh4dwf_e",
        "https://www.amazon.cn/gp/product/B0185KHPMM/ref=s9_acss_bw_cg_FTZ_2a1_w?pf_rd_m=A1U5RCOVU0NYF2&pf_rd_s=merchandised-search-top-1&pf_rd_r=3WVBSGYJRSZYNRV91PD9&pf_rd_t=101&pf_rd_p=18ea428b-fcea-4825-a1e0-8104313c9c01&pf_rd_i=1976720071",

    ]
    # url = "https://www.amazon.cn/?tag=baidu250-23&hvadid={creative}&ref=pz_ic_22fvxh4dwf_e"
    def start_requests(self):

        yield Request(url=self.start_urls[1], callback=self.parse, dont_filter=True)

    def parse(self, response):
        with open('1.html', 'wb')as f:
            f.write(response.body)
