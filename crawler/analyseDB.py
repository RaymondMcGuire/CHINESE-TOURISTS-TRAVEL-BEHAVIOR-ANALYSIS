#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 13:56:35 2017

@author: raymondmg
"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
import django
django.setup()
from crawlerDataBase.models import Article
import requests
import re
import random
from lxml import etree
import time
import jieba
from jieba import analyse




def dealWithKeyWord(data):
    keyWordsInfo=jieba.analyse.extract_tags(data, topK=15, withWeight=True, allowPOS=('a'))
    
    word=list()
    weight=list()
    for rowV in range(len(keyWordsInfo)):
       word.append(keyWordsInfo[rowV][0])
       weight.append(keyWordsInfo[rowV][1])
    return str(word)

def updateArticleKeyWords():
    
    index=1
    allData=Article.objects.all()

    for da in allData:
        articles=da.articleInfo
        if articles.strip()!='':
            keyword=dealWithKeyWord(articles)
            curData=Article.objects.get(id=da.id)
            curData.keyWords=keyword
            curData.save()
            
            percent=index/allData.count()*100
            printResult="%.2f" % percent +'%'
            print(printResult)
            print(keyword)
        index+=1
         


updateArticleKeyWords()