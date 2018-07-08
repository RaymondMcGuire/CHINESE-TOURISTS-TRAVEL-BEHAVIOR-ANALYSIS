#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 16:51:14 2018

@author: raymondmg
"""

from selenium import webdriver
import os
import socket
import time


img_path='/Users/raymondmg/Downloads/testimage/'
output_path='/Users/raymondmg/Downloads/res/'
timeout = 400
socket.setdefaulttimeout(timeout)
os.environ["PATH"] += os.pathsep + os.getcwd()
extension_list=["jpg","gif","jpeg","png","bmp","tif","webp"]

def export_txtfile(original,context):
    name = output_path+'label.txt'
    with open(name, 'w', encoding='utf-8') as f:
        for c in range(len(context)):
            f.write(original[c]+ '\t'+context[c] + '\n')
    f.close()

def getfilename(file_dir):
    dirs = os.listdir(file_dir)
    file_name=[]
    for dir in dirs:
        file_name.append(dir)
    return file_name

def main():
  
  file_list=getfilename(img_path)
  result_context = []
  original_name =[]
  for i in range(len(file_list)):
      extension = file_list[i].split('.')[1]
      if extension not in extension_list:
          continue
      url = "https://www.google.co.jp/searchbyimage/upload"
      driver = webdriver.Chrome()
      driver.get(url)
    	
      headers = {}
      headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
      time.sleep(1)
      file_input = driver.find_element_by_id("qbfile")
      file_input.send_keys(img_path+file_list[i])
      
      result_url=driver.current_url
      driver.get(result_url)
      result_label = driver.find_element_by_xpath("//a[@class='fKDtNb']").text
      str_label=str(result_label)
      print(str_label)
      original_name.append(file_list[i])
      result_context.append(str_label)
      driver.quit()
  export_txtfile(original_name,result_context)
if __name__ == "__main__":
	main()