#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'
import django
django.setup()
from crawlerDataBase.models import Article
import requests
import re
import random
from lxml import etree
import subprocess
import datetime
import time
import jieba
from jieba import analyse




check_ip ={"www.baidu.com":0}
send_error_limit = [30,60]
def checkNetConnected(get_ip):
    print("check ip start,ip: "+get_ip)
    try :
     p = subprocess.Popen(["ping "+get_ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
     check_result=p.stdout.readline()
     curtime = datetime.datetime.now() 

     if len(check_result) == 0:
      check_result=0
      print("[%s] timeout %s" % (curtime,get_ip))
     else:
      check_result=1
      print ("[%s] %s arrived" % (curtime,get_ip))
    except :
      check_result = 0
    
    return check_result


def dealWithKeyWord(data):
    keyWordsInfo=jieba.analyse.extract_tags(data, topK=15, withWeight=True, allowPOS=('n','ns'))
    
    word=list()
    weight=list()
    for rowV in range(len(keyWordsInfo)):
       word.append(keyWordsInfo[rowV][0])
       weight.append(keyWordsInfo[rowV][1])
    return str(word)
    #df2Csv=pd.DataFrame({'KeyWords':word,'weight':weight})
    #df2Csv.to_csv("/Users/raymondmg/クローラ/jiebaDemo/articleInfo/アーカイブ/keyWordsFile/result"+str(i)+".csv", index=False, encoding='utf-8') 


def create_article(title,sex,pos,timeInfo,dayInfo,peopleInfo,costInfo,strArticle,keyWordsStr,curHref):        
    entry = Article.objects.filter(articleName=title,authorPos=pos,authorSex=sex,startTime=timeInfo,people=peopleInfo,duringDay=dayInfo,cost=costInfo,articleInfo=strArticle,keyWords=keyWordsStr).exists()
    if entry:
        edit=Article.objects.get(articleName=title,authorPos=pos,authorSex=sex,startTime=timeInfo,people=peopleInfo,duringDay=dayInfo,cost=costInfo,articleInfo=strArticle,keyWords=keyWordsStr)
        if edit.href is None:
         edit.href=curHref
         edit.save()
         print("edit href!")
    else:
        article,created = Article.objects.get_or_create(articleName=title,authorPos=pos,authorSex=sex,startTime=timeInfo,people=peopleInfo,duringDay=dayInfo,cost=costInfo,articleInfo=strArticle,keyWords=keyWordsStr,href=curHref)
        if created:
              print("new article!")
              article.save()

def getDataFromMFW(pageNumStart,pageNumEnd,style,USER_AGENTS):
    
    #default
    startPage=1
    endPage=3
    step=1
    
    if style == '最热':#最热-》最新
        startPage=1
        endPage=3
        step=1
    elif style == '最新':#最新-》最热
        startPage=2
        endPage=0
        step=-1
        
    for curStyle in range(startPage,endPage,step):
        for curPage in range(pageNumStart[curStyle-1],pageNumEnd[curStyle-1]):
             headers=random.choice(USER_AGENTS)
             curPageNumUrl="http://www.mafengwo.cn/yj/10183/"+str(curStyle)+"-0-"+str(curPage)+".html"
             r=requests.get(curPageNumUrl,headers)
             sel=etree.HTML(r.text)
             for quote in sel.xpath('//h2[@class="post-title yahei "]/a|//h2[@class="post-title yahei hasxjicon"]/a'):
                
                href=quote.xpath('@href')
                title_bool=quote.xpath('text()!="APP"')
                title=quote.xpath('text()')
               
                if title_bool:
                  time.sleep(random.uniform(0.5,1.5))
                  if 'http' in ''.join(href):
                      continue;
           
                  print(href)
                  curHref='http://www.mafengwo.cn'+''.join(href)
                  currentR=requests.get(curHref,headers)
                  currentR.encoding = 'utf-8'
                  currentSel=etree.HTML(currentR.text)
            
                  #AuthorInfo
                  
                  #user id cal
                  scriptEnvi=currentSel.xpath('//head/script/text()')
                  pattern = re.compile(r'"author_uid":[^,]+') 
                  result_mid = pattern.findall(str(scriptEnvi))
                  pattern_nub=re.compile(r'\d+')
                  result=pattern_nub.findall(''.join(result_mid))
               
                  userUrl='http://www.mafengwo.cn/u/'+''.join(result)+'.html'
                  time.sleep(random.uniform(0.5,1.5))
                  a_R=requests.get(userUrl,headers)
                  a_R.encoding = 'utf-8'
                  a_Sel=etree.HTML(a_R.text)
                  
                  sexInfo=a_Sel.xpath('//div[@class="MAvaName"]/i/@class')
            
                  sex="None"
                  if str(sexInfo) == "['MGenderFemale']":
                      sex="Male"
                  elif str(sexInfo) == "['MGenderMale']":
                      sex="FeMale"
                  
                  pos="None"
                  posInfo=a_Sel.xpath('//span[@class="MAvaPlace flt1"]/@title')
                  
                  if len(posInfo) != 0:
                   pos=str(posInfo)
               
                  #Articleinfo
                  timeInfo=currentSel.xpath('//li[@class="time"]/text()')
                  if len(timeInfo)==2 and timeInfo[1] is not None: 
                   timeInfo=timeInfo[1]
                  else:
                   timeInfo="None"
                   
                  dayInfo=currentSel.xpath('//li[@class="day"]/text()')
                  if len(dayInfo)==2 and dayInfo[1] is not None: 
                   dayInfo=dayInfo[1]
                  else:
                   dayInfo="None"
                   
                  peopleInfo=currentSel.xpath('//li[@class="people"]/text()')
                  if len(peopleInfo)==2 and peopleInfo[1] is not None: 
                   peopleInfo=peopleInfo[1]
                  else:
                   peopleInfo="None"
                   
                  costInfo=currentSel.xpath('//li[@class="cost"]/text()')
                  if len(costInfo)==2 and costInfo[1] is not None: 
                   costInfo=costInfo[1]
                  else:
                   costInfo="None"
                  
                  #articleInfo
                  strArticle=""
                  for q in currentSel.xpath('//div[@class="va_con _j_master_content"]//text()'):        
                      curStr=q.strip() 
                      strArticle+=curStr
                
                  articleStr=strArticle.replace("\r\n","")
                  keyWordsStr=dealWithKeyWord(articleStr)
                  create_article(title,sex,pos,timeInfo,dayInfo,peopleInfo,costInfo,articleStr,keyWordsStr,curHref)
             time.sleep(random.uniform(0.5,1.5))
             print("page"+str(curStyle)+"-"+str(curPage)+" completed!")

def main():

    #customize dic
    jieba.load_userdict("userdict.txt") 
    pageNumStart=list()
    
    pageNumStart.append(1)  #最热游记起始页数
    pageNumStart.append(1)  #最新游记起始页数
    pageNumEnd=list()
    
    pageNumEnd.append(201)  #最热游记结束页数+1
    pageNumEnd.append(68)   #最新游记结束页数+！
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    ]
    
    getDataFromMFW(pageNumStart,pageNumEnd,'最新',USER_AGENTS)
    
    """
    try:
        getDataFromMFW(pageNumStart,pageNumEnd,USER_AGENTS)
    except :
        print('net connected failed! or error happened')
        
        flag=True
        while flag :
         for i in check_ip:
            check_status = checkNetConnected("%s"%i)
            if check_status == 1:
                check_ip["%s"%i] = 0
                print('connect successed')
                flag=False
                main()
            else :
                check_ip["%s"%i] +=1
            if check_ip["%s"%i] in send_error_limit :
                flag=True
                print('fail and error')
         time.sleep(3)
    """




if __name__ == "__main__":
    countNum=0

    while 1:
        countNum+=1
        main()
        """
        for i in check_ip:
            check_status = checkNetConnected("%s"%i)
            if check_status == 1:
                check_ip["%s"%i] = 0
                print('connect successed')
                flag=False
                main()
            else :
                check_ip["%s"%i] +=1
            if check_ip["%s"%i] in send_error_limit :
                flag=True
                print('fail and error')
        """
        print("Done!"+str(countNum))
