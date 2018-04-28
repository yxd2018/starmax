# -*- coding:utf-8 -*-

import urllib2
import urllib
from lxml import etree
import os
import bs4


url = 'https://www.qiushibaike.com/pic/page/'
header = {
    "referer":"https://www.qiushibaike.com/",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}


#创建文件夹
def mak_dir():
    global root
    isExists = os.path.exists('img')
    if not isExists:
        os.mkdir('img')
    else:
        root = os.path.abspath('img')
        return root

def downImg():
    count = 0
    for i in range(1, 11):
        print "开始下载第%s页"%str(i).center(20,'*')
        geturl = url + str(i)
        request = urllib2.Request(geturl,headers=header)
        content = urllib2.urlopen(request)

        obj = bs4.BeautifulSoup(content, 'lxml')
        img_list = obj.find_all('img')
        for img in img_list:
            src = img.get('src','')
            imgname = src.rsplit('/',1)[1]
            src_url = 'http:' + src

            try:
                urllib.urlretrieve(src_url,os.sep.join([root,imgname]))
                count += 1
            except Exception, e:
                print e
            else:
                print imgname+'下载成功'
        print "总共下载%s张图片"%count


if __name__=="__main__":
    mak_dir()
    downImg()