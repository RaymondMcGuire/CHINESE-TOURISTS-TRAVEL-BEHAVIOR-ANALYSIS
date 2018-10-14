# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 13:27:46 2018

@author: raymondmg
"""
import requests
from lxml import etree


headers="Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"

#web url(edit)
url="http://www.mafengwo.cn/wenda/detail-8736355.html"
xpath = '//div[@class="q-title"]/h1/text()'
xpath1 = '//a[@class="a-tag"]/text()'

r=requests.get(url,headers)
xml_content=etree.HTML(r.text)

for q in xml_content.xpath(xpath):
    print(q)

for q in xml_content.xpath(xpath1):
    print(q)