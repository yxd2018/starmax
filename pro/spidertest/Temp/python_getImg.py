#coding:gbk 

import time
import urllib
import urllib2

from lxml import etree

#etree ���Զ�html��ʽ���ַ�������html�ṹ

#1�鿴����Ҫ��ȡ����վ����������ĵ�ַ��ͷ��

url = "https://www.duitang.com/search/?kw=%E6%96%97%E5%9B%BE&type=feed"
header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
    }#��ʶ��������ʱ�����ݡ�
    
#2����������
request = urllib2.Request(url,data = None,headers = header)

#3�����ǽ�������Ӧ�����ݷ��س�Ϊһ���ļ�����
opener = urllib2.urlopen(request)

#4���鿴���ص�����  
content = opener.read()
#print(content)
#5��ɸѡ������Ҫ������
    #re
    #xpath
    #beautifulsoup

    #1������html�ṹ

html = etree.HTML(content)

    #����ƥ��������Ҫ������
        #����ҳ����ͼƬ�ĵ�ַ img��ǩ��src����
            #// ����ݹ�ƥ�䣬ƥ��ýṹ�������е�ָ����ǩ
            #[@class=""] ��ǩ��class����
img_list = html.xpath("//img")

#��������
    #ָ�����ݲɼ����̵��У����������վ����һ�ֺ�ƽ���ǹ�������Ϊ
for img in img_list:
    print(img.attrib["src"])
#��������ͼƬ�ĵ�ַ������
    img_url = img.attrib["src"]
    name = img_url.rsplit("/",1)[1]
    print(img_url)
    print(name)
    urllib.urlretrieve(url,name)
    time.sleep(3)




















