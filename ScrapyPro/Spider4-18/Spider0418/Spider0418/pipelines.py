# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from scrapy.exceptions import DropItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#数据保存
class Spider0418Pipeline(object):
    def __init__(self):
        # "".decode()
        self.file = open('data1.json', 'wb')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    #该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass
    #该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.title = item['title'][0]
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        for ok, value in results:
            image_path = value["path"]  # 获取文件路径
            if not image_path:
                raise DropItem('Item contains no images')

            item["image_paths"] = image_path
        return item

    def file_path(self, request, response=None, info=None):
        # open("image_urls.txt", "a").write(request.url + "\n")
        image_guid = request.url.split('/')[-1]

        return 'full/%s' % (image_guid)

