#coding:utf-8
import urllib2
import urllib
from bs4 import BeautifulSoup

# url = "https://www.qiushibaike.com/"
# url = 'https://www.baidu.com'
url = 'https://www.qiushibaike.com/pic/page/'
header = {
    # "referer":"https://www.qiushibaike.com/",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

req = urllib2.Request(url, headers=header)
content = urllib2.urlopen(req)
# with open("1.txt", 'wb') as f:
#     f.write(content.read())
# print content.read()

bsobj = BeautifulSoup(content, 'lxml')
a_lsit = bsobj.find_all("img")
"""
print('*****开始图片网址*****')
text = ''
for a in a_lsit:
    src = a.get('src')
    img_src = 'http:' + src
    text = text + img_src + '\n'
with open('img.txt', 'wb') as f:
    f.write(text)
"""
x = 1
root = '/home/developer/Documents/img/'
for a in a_lsit:
    src = a.get('src')
    imgName = src.rsplit('/',1)[1]
    img_src = 'http:' + src

    print(img_src)
    try:

        urllib.urlretrieve(img_src,root+'%s.jpg' % x)
        x += 1
    except Exception, e:
        print e
    else:
        print imgName+"下载完毕"