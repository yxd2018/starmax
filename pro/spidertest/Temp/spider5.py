# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import urllib
import requests
import re
import os
import datetime

# url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E6%B0%B4%E6%9D%AF&oq=%E6%B0%B4%E6%9D%AF&rsp=-1/"
url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%9D%AF%E5%AD%90&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=%E6%9D%AF%E5%AD%90&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=60&rn=30&gsm=3c&1523840779274="
header = {
    "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1523840751600_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E6%9D%AF%E5%AD%90",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

#创建目录
def mkdir():
    global imgpath
    isExists = os.path.exists('img')
    print(isExists)
    if not isExists:
        os.mkdir('img')
    imgpath = os.path.abspath('img')
    print(imgpath)
    return imgpath

#下载图片
def get_img(keyword,page):
    t1 = datetime.datetime.now()
    for i in range(1,page+1):
        data = {
            "word": keyword,
            "queryWord": keyword,
            "pn":30*i
        }

        req = requests.get(url=url, headers=header, params=data)
        content = req.content
        # print(content)
        urls = r'.*?"thumbURL":"(.*?)"'
        geturl = re.findall(urls,content)
        # print(geturl)
        print(len(geturl))
        i = 1
        for src in geturl:
            # print(src)
            try:
                urllib.urlretrieve(src, imgpath+'/'+"%s.jpg" % i)
                i += 1
            except Exception, e:
                print(str(e) + "下载失败")
    t2 = datetime.datetime.now()-t1
    print("下载完成！共用时%s")%t2


mkdir()
get_img("电脑",1)
