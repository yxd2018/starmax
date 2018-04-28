# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpidertempItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #ip
    ip = scrapy.Field()
    #端口
    port = scrapy.Field()
    #代理位置
    location = scrapy.Field()
    #代理类型
    type = scrapy.Field()
    #验证时间
    date = scrapy.Field()