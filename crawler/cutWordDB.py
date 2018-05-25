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
import jieba.posseg as pseg
import pandas as pd
from pandas import DataFrame as df


def creadstoplist(stopwordspath):
    stwlist = [line.strip()
               for line in open(stopwordspath, 'r', encoding='utf-8').readlines()]
    return stwlist

jieba.load_userdict("userdict.txt") 
stwlist = creadstoplist('stopwords.txt')

def dealWithCutWord(data,filterOrNot,flag):
    words=pseg.cut(data.strip())

    
    strArticle=""
    for w in words:
     #去停用词
     if w.word not in stwlist:
      if len(w.word) > 1:
        if filterOrNot:
         flagStrArray=flag.split(',')
         if w.flag in flagStrArray:
            strArticle+=w.word+","+w.flag+";"
        else:
         strArticle+=w.word+","+w.flag+";"
    return str(strArticle)

def updateArticleKeyWords():
    jieba.load_userdict("userdict.txt") 

    index=1
    allData=Article.objects.all()
    cutwordsres=[]
    for da in allData:
        articles=da.articleInfo
        if articles.strip()!='':
            cutword=dealWithCutWord(articles,True,"pos")
            cutwordsres.append(cutword)
            
            percent=index/allData.count()*100
            printResult="%.2f" % percent +'%'
            print(printResult)
            #print(cutword)
        index+=1
        
    df2Csv=pd.DataFrame({'result':cutwordsres})
    df2Csv.to_csv("cutword-result.csv", index=False, encoding='utf-8')  
         


updateArticleKeyWords()