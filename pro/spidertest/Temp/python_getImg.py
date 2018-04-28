#coding:gbk 

import time
import urllib
import urllib2

from lxml import etree

#etree 可以对html格式的字符串构建html结构

#1查看我们要爬取的网站，分析爬虫的地址和头部

url = "https://www.duitang.com/search/?kw=%E6%96%97%E5%9B%BE&type=feed"
header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }#标识我们请求时候的身份。
    
#2、发起请求
request = urllib2.Request(url,data = None,headers = header)

#3、我们将请求响应的内容返回成为一个文件对象
opener = urllib2.urlopen(request)

#4、查看返回的内容  
content = opener.read()
#print(content)
#5、筛选我们需要的数据
    #re
    #xpath
    #beautifulsoup

    #1、构建html结构

html = etree.HTML(content)

    #进行匹配我们需要的数据
        #该网页所有图片的地址 img标签的src属性
            #// 代表递归匹配，匹配该结构当中所有的指定标签
            #[@class=""] 标签的class属性
img_list = html.xpath("//img")

#爬虫礼仪
    #指在数据采集过程当中，对请求的网站保持一种和平，非攻击的行为
for img in img_list:
    print(img.attrib["src"])
#构建下载图片的地址和名称
    img_url = img.attrib["src"]
    name = img_url.rsplit("/",1)[1]
    print(img_url)
    print(name)
    urllib.urlretrieve(url,name)
    time.sleep(3)




















