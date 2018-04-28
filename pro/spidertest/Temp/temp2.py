# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib2
import json

url = 'http://www.seputu.com/'
header = {
    "Referer": "http://www.seputu.com/",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}
def getcontent():

    # r = requests.get(url=url, headers=header)
    # print(r.text)
    # soup = BeautifulSoup(r.text, 'html.parser')


    req = urllib2.Request(url=url, headers=header)
    cont = urllib2.urlopen(req)
    # print(cont.read())

    # with open('1.txt', 'wb')as f:
    #     f.write(cont.read())
    soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')
    # print(soup)


    content = []
    for mulu in soup.find_all(class_="mulu"):
        # print(mulu)
        h2 = mulu.find("h2")
        if h2 != None:
            h2_title = h2.string
            for a in mulu.find_all("a"):
                href = a.find("href")
                box_title = a.string
                # print(href,box_title)
                list = []
                list.append({"href":href, "box_title":box_title})
            content.append({"title":h2_title, "content":list})
    with open('test.json', 'wb') as f:
        json.dump(content, fp=f, indent=4)


getcontent()