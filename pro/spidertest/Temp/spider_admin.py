# -*- coding:utf-8 -*-

import requests
import urllib2
import urllib
from bs4 import BeautifulSoup
import http.cookiejar

url = 'https://zhidao.baidu.com/'



data = {
    "username":18562557397,
    "password":"dd930822"
}

post_data = urllib.urlencode(data).encode("utf-8")
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36",
    "referer": "https://zhidao.baidu.com/",

}
cookie = http.cookiejar.CookieJar() #构造cookie
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
req = urllib2.Request(url, headers=header, data=post_data)

#发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
resp = opener.open(req)

#构造访问请求
# req = urllib.request.Request(url, headers = header)
#
# resp = opener.open(req)

# print(resp.read())
print(resp)