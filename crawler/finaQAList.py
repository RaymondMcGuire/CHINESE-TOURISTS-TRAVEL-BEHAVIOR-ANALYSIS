# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 16:09:13 2018

@author: SongZilong
"""

from selenium import webdriver
import random
import os
#os.environ["PATH"] += os.pathsep + os.getcwd()
os.environ['DJANGO_SETTINGS_MODULE'] = 'crawler.settings'

import django
django.setup()
from crawlerDataBase.models import QuestAnswerList
import socket
import time


timeout = 400
socket.setdefaulttimeout(timeout)

def create_question_id(q_id):        
    entry = QuestAnswerList.objects.filter(qid=q_id).exists()
    if not entry:
        quest,created = QuestAnswerList.objects.get_or_create(qid=q_id)
        if created:
              print("new question! id:"+str(q_id))
              quest.save()
    else:
        print("have recorded! id:"+str(q_id))

data_type = [3,0,2]
def main():
  
  #select data type
  for dtye in data_type:
      url = "http://www.mafengwo.cn/wenda/area-10183.html?sFrom=mdd"
      driver = webdriver.Chrome()
      driver.get(url)
      labelhref = driver.find_element_by_xpath("//ul[@class='cate-tab']/li[@data-type='"+str(dtye)+"']/a")
      labelhref.click()
      rnd_time =random.uniform(1.0,2.0)
      time.sleep(rnd_time)
      print("current collect label is:"+str(labelhref.text))
      # identify whether there have more questions or not
      loadhrefText = driver.find_element_by_xpath("//div[@class='answer-more _j_add_more_button']/a").text
     
      while loadhrefText == "加载更多":
          loadhref = driver.find_element_by_xpath("//div[@class='answer-more _j_add_more_button']/a")
          loadhref.click()
          rnd_time =random.uniform(2.0,3.0)
          time.sleep(rnd_time)
          loadhrefText = driver.find_element_by_xpath("//div[@class='answer-more _j_add_more_button']/a").text
      
      qlist = driver.find_elements_by_xpath("//li[@class='item clearfix _j_question_item']")
      for q in qlist:
          create_question_id(q.get_attribute("data-qid"))
          #print(q.get_attribute("data-qid"))
      
      driver.quit()
      

if __name__ == "__main__":
	main()