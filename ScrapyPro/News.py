# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

url = 'http://news.dailyqd.com/node_3118.htm',
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36",
    "Referer": "http://news.dailyqd.com/node_3118.htm"
}

r = requests.get(url=url, headers=header)
soup = BeautifulSoup(r,'html.parser')

for news in soup.select('li'):
    li_n = len(soup.select('li'))
    for i in range(li_n+1):
        title=news.select('a')['%s'%i].text
        url=news.select('a')['%s'%i]['href']
        print(title,url)