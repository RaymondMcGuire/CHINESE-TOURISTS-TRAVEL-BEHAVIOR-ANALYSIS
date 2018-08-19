#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 18:56:28 2017

@author: raymondmg
"""

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
import django
django.setup()
from crawlerDataBase.models import Article
import jieba


def export_txtfile(i,context):
    name = './key_word_article/article_'+str(i)+'.txt'
    with open(name, 'w', encoding='utf-8') as f:
        for c in range(len(context)):
            f.write(context[c] + '\t')
    f.close()

def creadstoplist(stopwordspath):
    stwlist = [line.strip()
               for line in open(stopwordspath, 'r', encoding='utf-8').readlines()]
    return stwlist

stwlist = creadstoplist('stopwords.txt')
jieba.load_userdict("userdict.txt")

def getArticleFromDataBase():
    allData=Article.objects.all()
    doc_set = [da.articleInfo for da in allData if da.articleInfo.strip()!=''] #and da.authorSex=='FeMale'
    #doc_set = [da.articleInfo for da in allData if da.articleInfo.strip()!='' and da.authorPos=='北京']
    return doc_set

# compile sample documents into a list
doc_set = getArticleFromDataBase()

# list for tokenized documents in loop



#是否控制读取数量
maxProcessNum=500
needConstraint=True

index=0
for i in doc_set:
   
    index+=1
    
    if i.contains("琵琶湖"):
        print(str(i))
        export_txtfile(index,i)

    
    print('read article from database:'+str(index)+'/'+str(len(doc_set)))
   
    if index>=maxProcessNum and needConstraint:
        break





  



