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
import csv

def export_txtfile(name,context):
    name = './key_word_article/article/'+str(name)+'.txt'
    with open(name, 'w', encoding='utf-8') as f:
        f.write(context)
    f.close()

def export_keywordfile(header,body):
    name = './key_word_article/chk_keyword.csv'
    with open(name, 'w', encoding='utf-8', newline='') as f:
          writer = csv.writer(f)  
          writer.writerow(header)
          writer.writerows(body)
          f.close()

def chkKeyWordFromDataBase(key_word_list):
    allData=Article.objects.all()
    header = ['ID','articleName','authorPos','authorSex','startTime','people','duringDay','cost','href']
    header.extend(key_word_list)
    body = []
    
    idx = 0
    for da in allData:
        
        if da.articleInfo.strip()!='':
            article = str(da.articleInfo)
            keywordContainOrNot = []
            flag = False
            for kw in key_word_list:
                if kw in article:
                    flag = True
                    keywordContainOrNot.append(1)
                else:
                    keywordContainOrNot.append(0)
            if flag:
                cur_context = []
                idx +=1
                cur_context.append(idx)
                cur_context.append(da.articleName)
                cur_context.append(da.authorPos)
                cur_context.append(da.authorSex)
                cur_context.append(da.startTime)
                cur_context.append(da.people)
                cur_context.append(da.duringDay)
                cur_context.append(da.cost)
                
                href = da.href
                if da.href is None:
                    href = "None"
                
                cur_context.append(href)
                cur_context.extend(keywordContainOrNot)
                body.append(cur_context)
                export_txtfile(idx,da.articleInfo)
    
    export_keywordfile(header,body)

            
key_word_list = ["琵琶湖","输水"]
chkKeyWordFromDataBase(key_word_list)





  



