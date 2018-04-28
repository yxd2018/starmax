# -*- coding:utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


#爬取糗事百科文段

url = "https://www.qiushibaike.com/text/"
header = {
    "Referer": "https://www.qiushibaike.com/text/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}

req = urllib2.Request(url=url, headers=header)
resp = urllib2.urlopen(req)
# with open("1.txt", "wb") as f:
#     f.write(resp.read())
# print(resp.read())
soup = BeautifulSoup(resp,'lxml')
# print(soup)

# contents = soup.find_all("div")
contents = soup.select("div .content")


# print(contents)
# print(len(contents))
for content in contents:
    print(content[0])
    # span = content.get("span")
    # print(span)
