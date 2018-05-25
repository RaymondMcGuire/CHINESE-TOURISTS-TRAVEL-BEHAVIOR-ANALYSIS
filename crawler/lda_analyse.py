#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 00:29:05 2017

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
    doc_set = [da.articleInfo for da in allData if da.articleInfo.strip()!='']
    #doc_set = [da.articleInfo for da in allData if da.articleInfo.strip()!='' and da.authorPos=='北京']
    return doc_set

# compile sample documents into a list
doc_set = getArticleFromDataBase()

# list for tokenized documents in loop



#是否控制读取数量
maxProcessNum=300
topicNum=28
wordNum=15
needConstraint=False
plt.figure(1)

perplexityValue=list()
numValue=list()

index=0
texts = []
for i in doc_set:
    
    index+=1
    
    #print(curdoc)
    
    #处理分词，True使用过滤分词/False不使用过滤
    curdoc=dealWithCutWord(i,True,"pos,n")
    curtexts=[]
    curtexts.append(curdoc)
    #curDictionary = corpora.Dictionary(curtexts)
    #curCorpus = [curDictionary.doc2bow(text) for text in curtexts]
    #curLdamodel = gensim.models.ldamodel.LdaModel(curCorpus,num_topics=topicNum,id2word=curDictionary,passes=20)   
    #number.append(index)
    #articleTopic.append(curLdamodel.print_topics(num_topics=topicNum, num_words=wordNum))


    texts.append(curdoc)    
    print('read article from database:'+str(index)+'/'+str(len(doc_set)))
    
    if index>=maxProcessNum and needConstraint:
        break

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]




ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=topicNum,id2word=dictionary,passes=20)  
ldamodel.save('lda.model')
#lda = models.ldamodel.LdaModel.load('lda.model')
print(ldamodel.print_topics(num_topics=topicNum,num_words=wordNum))


donatePercent=list()
for _ in range(0,topicNum):
    curVal=0.0
    donatePercent.append(curVal)

print(len(corpus))


for art in range(0,len(corpus)):
    if len(ldamodel[corpus[art]])>0:
        for val in range(0,len(ldamodel[corpus[art]])):
            if len(ldamodel[corpus[art]][val])>1:
                curIndex=ldamodel[corpus[art]][val][0]
                curVal=ldamodel[corpus[art]][val][1]
                donatePercent[curIndex]+=curVal

resultDonatePercent=[round(xx/maxProcessNum,2)  for xx in donatePercent]

print(resultDonatePercent)



"""
for num in range(1,topicNum+1):

    
    print('process article! current topic: '+str(num))

    
    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus,num_topics=num,id2word=dictionary,passes=20)  
    perwordbound = ldamodel.log_perplexity(corpus)
    perplex=np.exp2(-perwordbound)
    perplexityValue.append(perplex)
    numValue.append(num)


    #print(perplex)

#print(perplexityValue)


#draw graph
plt.figure(1)
plt.plot(numValue,perplexityValue,marker='o')
plt.title('PPL(n=10598)')
plt.xlabel('topic num')
plt.ylabel('PPL')
plt.show()

#print value
for i in range(0,len(numValue)):
    print("topic num:"+str(numValue[i])+",perplexity value:"+str(perplexityValue[i]))

"""


"""
index=0
for _ in doc_set:
    
    index+=1
    
    for i in range(0,topicNum):
        topicList[i].append('')
    
    if index>=maxProcessNum and needConstraint:
        break

    
df2Csv=pd.DataFrame({'number':number,
                     'articleLDA':articleTopic,
                     'topic1':topicList[0],
                     'topic2':topicList[1],
                     'topic3':topicList[2],
                     'topic4':topicList[3],
                     'topic5':topicList[4],
                     'topic6':topicList[5],
                     'topic7':topicList[6],
                     'topic8':topicList[7],
                     'topic9':topicList[8],
                     'topic10':topicList[9],
                     'topic11':topicList[10],
                     'topic12':topicList[11],
                     'topic13':topicList[12],
                     'topic14':topicList[13],
                     'topic15':topicList[14]
                     },columns=['number','articleLDA','topic1','topic2','topic3','topic4','topic5','topic6','topic7','topic8','topic9','topic10','topic11','topic12','topic13','topic14','topic15'])
#df2CsvFixed=pd.DataFrame(df2Csv,index=['number','articleLDA','topic1','topic2','topic3','topic4','topic5','topic6','topic7','topic8','topic9','topic10','topic11','topic12','topic13','topic14','topic15'])
df2Csv.to_csv("result.csv", index=False, encoding='utf-8')  
""" 

