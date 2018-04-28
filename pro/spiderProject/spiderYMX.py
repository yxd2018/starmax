# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

url = "https://www.amazon.com/s/ref=nb_sb_noss_2/130-7479687-3822736?url=search-alias%3Daps&field-keywords=cup"
# url = "https://www.amazon.cn/s?rh=n%3A79193071&ie=UTF8"
"""
https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=i%3Aaps%2Ck%3Acup&page=2&keywords=cup&ie=UTF8&qid=1523846875
https://www.amazon.com/s/ref=sr_pg_3?fst=p90x%3A1&rh=i%3Aaps%2Ck%3Acup&page=3&keywords=cup&ie=UTF8&qid=1523846984
"""

header = {
    "Referer": "https://www.amazon.com/s/ref=sr_pg_1?fst=p90x%3A1&rh=i%3Aaps%2Ck%3Acup&keywords=cup&ie=UTF8&qid=1523847172",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36"
}
proxies = {
	"https":"http://34.227.82.35:8080",
    }
r = requests.get(url, headers=header,proxies=proxies,verify=False)
# print(r.content.decode('utf-8'))
content = r.content
print(content)


"""
#爬取图片链接
findimg = r'<div aria-hidden="true" class="a-column a-span12 a-text-center">(.*?)</div>'
imgconts = re.findall(findimg, content)
# print(imgconts)
# print(len(imgconts))
for imgcont in imgconts:
    # print(cont)
    fimg = r'<img src="(.*?)"'
    img = re.findall(fimg,imgcont)
    # print(img)

#爬取标题
soupt = BeautifulSoup(content, 'lxml')
titleconts = soup.findAll('h2')
for titlecont in titleconts:
    # print(titlecont.text)
    pass
    
    
# //*[@id="result_1"]/div/div[2]/div/div[2]/div[1]/div[1]/a/h2/text()
"""

#获取价格

findprice = r'<a class="a-link-normal a-text-normal" href=.*?><span class="a-offscreen">(.*?)</span>'
priconts = re.findall(findprice, content)
# print(priconts)
# print(len(priconts))
with open("1,txt", "wb")as f:
    for pricont in priconts:
        f.write(pricont+'\n')




# //*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[1]

# img = selector.xpath('//*[@id="result_1"]/div/div[2]/div/div[1]/div/div/a/img')

"""
selector = etree.HTML(content)
for i in range(1,17):
    prices = selector.xpath('//*[@id="result_%s"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[1]' %i)
    print(prices)
    # for price in prices:
    #     print(price.text)
"""
"""
//*[@id="result_1"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/a/span[1]
//*[@id="result_2"]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[3]/a/span[1]
//*[@id="result_3"]/div/div/div/div[2]/div[2]/div[1]/div[1]/a/span[1]

"""
"""
selector = etree.HTML(content)
for i in range(1,17):
    title = selector.xpath('//*[@id="result_1"]/div/div[2]/div/div[2]/div[1]/div[1]/a/h2/text()')
    print(title)

"""