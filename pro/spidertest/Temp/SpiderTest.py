#coding:utf-8
import requests
import urllib
import os
import re
import socket
import threading
import datetime
import time

referer = url = "http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1523547209584_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%A3%8E%E6%99%AF"

headers = {

    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Referer": referer
}

"""
创建存放图片文件夹
"""
def creat_dir():
    isExists = os.path.exists("image")
    print isExists
    if not isExists:
        os.makedirs("image")
    imagePath =  os.path.abspath("image")
    return imagePath

"""
下载图片
start:imgas的起始index
end:images的末尾index
imgs：存放图片的数组
"""

def pic_download(start,end,imgs):
    for imgUrl in imgs[start:end]:
        imgName = imgUrl.rsplit("/", 1)[1]
        imgPath = os.sep.join([imagePath,imgName])
        #print "startdownloading :"+imgName
        try:
            urllib.urlretrieve(imgUrl, imgPath)
        except Exception, e:
            print e
        else:
            print imgName+"下载完毕"

"""
循环下载图片
keyWord:搜索关键字
start:起始图片位置
page：下载多少页图片，一页30张
"""            
def get_pic(keyWord,start,page,timeout,threadNum):
    socket.setdefaulttimeout(timeout) #设置下载每张图的超时间隔
    imgs=[]
    for p in range(page):
        pn = start + p*30
        params = {"word": keyWord,"pn": pn}
        req = requests.get(url=url, headers=headers, params=params)
        content = req.content
        imgs.extend(re.findall(r'objURL":"(.*?jpg)', content))
    nPic = len(imgs)/threadNum
    lastPic = start + len(imgs)
    print nPic
    thread_list = []
    for i in range(threadNum):
        end = start + nPic
        if end > lastPic:
            end = lastPic
        print "start:"+str(start)
        print "end:"+str(end)
        t = threading.Thread(target=pic_download, args=(start,end,imgs))
        t.setDaemon(True)
        thread_list.append(t)
        start = end
        
    print "thread:"+ str(len(thread_list))
    start_time  = datetime.datetime.now()
    for n,t in enumerate(thread_list):
        t.start()

    for t in thread_list:
        t.join()

    end_time = datetime.datetime.now()
    duration = end_time-start_time
    print "下载共用时间: %s"%duration 
imagePath = creat_dir()
print imagePath
get_pic("凹凸美女",0,30,10,300)
