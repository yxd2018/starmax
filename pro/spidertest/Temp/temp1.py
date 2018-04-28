# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


url = 'https://www.qiushibaike.com/pic/page/'
header = {
    "referer":"https://www.qiushibaike.com/",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

request = urllib2.Request(url=url, headers=header)
response = urllib2.urlopen(request)


soup = BeautifulSoup(response, 'lxml')
# print(soup)
img_s = soup.select("img[src]")
print(img_s)
img_f = soup.find_all('img')
print(img_f)

for imgs in img_s:
    src = 'http:' + imgs.get('src')
    name = src.rsplit('?',1)[0]
    imgname = name.rsplit('/',1)[1]
    print(imgname)
    print(src)