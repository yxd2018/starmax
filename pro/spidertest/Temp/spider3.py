#coding:utf-8

# 爬取糗百图片

import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import datetime

url = 'https://www.qiushibaike.com/pic/page/'
header = {
    "referer":"https://www.qiushibaike.com/",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

#创建存储目录地址

def mak_dir():
    global root
    isExists = os.path.exists('/home/developer/Documents/img/')
    if isExists:
        root = '/home/developer/Documents/img/'
    else:
        os.mkdir('/home/developer/Documents/img/')
    return root


def get_urls():
    x = 1
    count = 0
    t1 = datetime.datetime.now()
    for i in range(1,2):
        print "开始下载第%s页"%i
        geturl = url + str(i)
        # print(geturl)
        request = urllib2.Request(geturl, headers=header)
        content = urllib2.urlopen(request)

        # print(content.read())
        # name = str(i) + '.txt'
        # with open(name,'wb') as f:
        #     f.write(content)

        bsobj = BeautifulSoup(content, 'lxml')
        a_list = bsobj.find_all('img')
        # print(a_list)
        for a in a_list:
            src = a.get('src')
            imgName = src.rsplit('/', 1)[1]
            img_src = "http:"+src

            try:

                urllib.urlretrieve(img_src, root + '%s.jpg' % x, reporthook=get_data)
                count += 1
                x += 1
            except Exception, e:
                print e
            else:

                print imgName + "下载成功！"
    print '共下载图片%s张'%count
    t2 = datetime.datetime.now() - t1
    print "总用时为：%s"%t2


def get_data(a, b, c):
    num = float(a + 1) * b / c
    if num >1:
        num = 1
    num *= 100
    print('**********')
    print('%.2f%%'%num)
    print('**********')

if __name__ == '__main__':

    mak_dir()
    get_urls()