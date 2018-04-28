# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sys
import urllib
import os
import resouce
import random


reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderTest(object):
    #创建图片存储文件夹
    def mkdir(self):
        global root
        root2 = '/home/developer/workspace/pro/spidertest/0419'
        isExists = os.path.exists('image')
        print(isExists)
        if not isExists:
            root1 = os.mkdir('image')
            root = os.path.join(root2, root1)
        root = os.path.abspath('image')
        return root


    #获取列表页信息  文章标题 详情页地址 时间
    def get_content(self, url):
        r = requests.get(url=url, headers=header)
        r.encoding = r.apparent_encoding
        selector = etree.HTML(r.text)
        for i in range(1,5):
            bodys = selector.xpath('//div[@class="maincon_left_top"]/div[%s]' % i)
            # print(bodys)
            for list1 in bodys:
                for i in range(1, 6):

                    title = list1.xpath('.//ul/li[%s]/div[1]/a/text()' % i)
                    f.write(title[0] + ' ')
                    date = list1.xpath('.//ul/li[%s]/span/text()' % i)
                    f.write(date[0] + ' ')
                    # f.write('\n')
                    url_con1 = list1.xpath('.//ul/li[%s]/div[1]/a/@href' % i)
                    url_con = 'http://news.dailyqd.com/'+url_con1[0]
                    f.write(url_con + ' ')
                    # f.write('\n')
                    self.get_content2(f, url_con, title,date)


    #获取详情页文章内容 图片链接
    def get_content2(self, f, url_con, title, date):
        contentlist = []
        imgurl = []
        i = 1
        req = requests.get(url=url_con, headers=header)
        req.encoding = req.apparent_encoding
        selector = etree.HTML(req.text)
        contents = selector.xpath('//div[@class="left_text_box"]/p')
        for content in contents:
            if content.xpath('//div[@class="left_text_box"]/p[%s]/text()' % i):
                list = content.xpath('//div[@class="left_text_box"]/p[%s]/text()' % i)
                i += 1
                contentlist.extend(list)

            elif content.xpath('//div[@class="left_text_box"]/p[%s]/strong/text()' % i):
                list = content.xpath('//div[@class="left_text_box"]/p[%s]/strong/text()' % i)
                i += 1
                contentlist.extend(list)

            else:
                list = content.xpath('//div[@class="left_text_box"]/p[%s]/img/@src' % i)
                i += 1
                # contentlist.extend(list)
                imgurl.extend(list)
                for imgs in imgurl:
                    # print imgs
                    name = imgs.rsplit('/',1)[-1]
                    print(name)
                    # print(type(imgs))
                    try:

                        absname = os.path.join(root,name)
                        urllib.urlretrieve(imgs, absname)
                        print(absname+'下载成功')
                    except Exception,e:
                        print(str(e)+"图片下载失败")

        for conts in contentlist:
            f.write(conts +' ')
        for img in imgurl:
            f.write(img+' ')
        f.write('\n')
        # print(url_con, title, date, contentlist, imgurl)

        print 'resp', req.cookies._cookies

    def getnetpage(self,next_url):
        pass
if __name__=='__main__':
    spider = SpiderTest()
    spider.mkdir()
    url0 = 'http://news.dailyqd.com/node_3118.htm'
    user_agent = random.choice(resouce.MY_USER_AGENT)
    refere = "http://news.dailyqd.com/node_3118.htm"
    ipprox = random.choice(resouce.IPPOOL)
    cookie = resouce.COOKIE
    header = {
        "User-Agent": user_agent,
        "Referer": refere
    }
    f = open('data.txt', 'wb')

    r = requests.get(url=url0, headers=header,proxies=ipprox,verify=False,cookies=cookie)
    r.encoding = r.apparent_encoding
    selector = etree.HTML(r.text)

    #//*[@id="displaypagenum"]/center/a[5]
    num = selector.xpath('//*[@id="displaypagenum"]/center/a/text()')[-2]
    print(num)
    for j in range(1, int(num)+1):
        if j == 1:
            url = url0
            print(url)
            spider.get_content(url)
        else:
            url = url0.rsplit('.',1)[0] + '_%s.htm' % j
            print(url)
            spider.get_content(url)