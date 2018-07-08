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
from gensim import corpora
import gensim
import jieba
import jieba.posseg as pseg
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import matplotlib.pyplot as plt

def splitResultFromLDAModel(data):
    freq  =[]
    words =[]
    if '*' not in data or '+' not in data:
        return freq,words
    firArray=data.split('+')
   
    for d in firArray:
        secArray=d.split('*')
        freq.append(secArray[0])
        words.append(secArray[1])
    return freq,words

def export_txtfile(i,context):
    name = './export_article/article_'+str(i)+'.txt'
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

def dealWithCutWord(data,filterOrNot,flag):
    curtexts = []
    words=pseg.cut(data.strip())  
    for w in words:
     #remove stopwords
     if w.word not in stwlist:
      if len(w.word) > 1:
        if filterOrNot:
         flagStrArray=flag.split(',')
         if w.flag in flagStrArray:
            curtexts.append(w.word)
        else:
          curtexts.append(w.word)
    return curtexts

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
   
    #print(curdoc)
   
    #处理分词，True使用过滤分词/False不使用过滤
    curdoc=dealWithCutWord(i,True,"pos,n")
    export_txtfile(index,curdoc)

    
    print('read article from database:'+str(index)+'/'+str(len(doc_set)))
   
    if index>=maxProcessNum and needConstraint:
        break





  



