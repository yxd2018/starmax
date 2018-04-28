# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import requests

url = "https://www.qiushibaike.com/text/"
header = {
    "Referer": "https://www.qiushibaike.com/text/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

"""
request = urllib2.Request(url=url, headers=header)
response = urllib2.urlopen(request)

soup = BeautifulSoup(response, 'lxml')
# print(soup)
divs = soup.find_all('div')
for div in divs:
    span = div.get('span')
    print(span)
"""

r = requests.get(url=url, headers=header)
print(r.text)