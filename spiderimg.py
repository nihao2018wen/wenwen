# -*- coding: utf-8 -*-
import os
import time
import json
import urllib.request
import datetime
import subprocess
import configparser
import sys 
from selenium import webdriver

finishname_list = list()
fa123 = open('E:\\spiderdata\\finish.txt','r', encoding="utf-8")
with open('E:\\spiderdata\\finish.txt',"r", encoding="utf-8") as f123:
    lines = f123.readlines()
    for line in lines:
        line = line.strip()
        finishname_list.append(line)
fa123.close()

finishmark_list = list()
ma123 = open('E:\\spiderdata\\finishmark.txt','r', encoding="utf-8")
with open('E:\\spiderdata\\finishmark.txt',"r", encoding="utf-8") as m123:
    lines = m123.readlines()
    for line in lines:
        line = line.strip()
        finishname_list.append(line)
ma123.close()


def DownPIC(url,path):
    flag = True
    try:
        filename = os.path.basename(url)
        path=os.path.join(path,filename)
        urllib.request.urlretrieve(url,path)
        return flag
    except:
        flag = False
        return flag

def DownPIC2(url,path):
    flag = True
    try:
        urllib.request.urlretrieve(url,path)
        return flag
    except:
        flag = False
        return flag
		
def FetchAll(browser,path):
    try:
        burl = browser.find_element_by_css_selector("div#picPlusAd.photo.none>img.bpic")
        bhref = burl.get_attribute("src")
        num = bhref.rfind(".j")
        bhref='%s.%s' % (bhref[0:num],'jpg')
        #print(bhref)
        flagdown1 = DownPIC(bhref, path)
        browser.find_element_by_css_selector("div.arrow_right.arrow-box>span.iconfont").click()
        FetchAll(browser,path)
    except Exception as e:
        print("pp")
        #browser.back()
		
def isElementExists(browser,element):
    flag=True
    try:
        browser.find_element_by_link_text(element)
        return flag
    except:
        flag=False
        return flag
		
def isElementExist(browser,element):
    flag=True
    try:
        browser.find_element_by_css_selector(element)
        return flag
    except:
        flag=False
        return flag
		
		
def GetPIC(url,name):
    browser = webdriver.Firefox()
    browser.get(url)
    flag= isElementExist(browser,"#t_q_tab_star li")
    if flag :
        browser.find_element_by_css_selector("a#q_tab_star.black_link").click()
        imglist=browser.find_elements_by_css_selector("ul#t_q_tab_star.starlst.clear.qtable>li")       
        imglen = len(imglist)
        if imglen < 1:
            print ("imglen not")
        else:
            url_list = list()
            path_list = list()
            markimage_list = list()
            namemark_list = list()
            for img in imglist:
                markimage = img.find_element_by_css_selector('img').get_attribute("src")
                markimage_list.append(markimage)
				
                urlcode = img.find_element_by_css_selector('a').get_attribute("href")
                url_back = urlcode				
                url_list.append(url_back)
                #urlcode = https://www.tvmao.com/star/Yi0vHy8=
				
                username = img.find_element_by_css_selector('a').get_attribute("title")

                urlcode = ''.join(urlcode.split('https://www.tvmao.com/'))
                urlcode = '_'.join(urlcode.split('/'))
                namemark_list.append(urlcode)
                starpath = "E:\spiderImages\%s_%s" % (username,urlcode)
                path_list.append(starpath)
				
				
            for i in range(0, len(path_list)):			
                namemark = namemark_list[i]
                namemark = namemark.strip()
                if namemark in finishmark_list:
                    continue
					
                path = path_list[i]		
                if not os.path.exists(path):
                    os.mkdir(path)				
                tvfilename = "tvmark.jpg"
                tvpath=os.path.join(path,tvfilename)
                flagdown = DownPIC2(markimage_list[i], tvpath)
                if flagdown == False:
                    continue

                browser2 = webdriver.Firefox()
                browser2.get(url_list[i])
                
                print (url_list[i])
                flag1= isElementExists(browser2, "图BB")
                if flag1 :
                    browser2.find_element_by_link_text("图BB").click()
                    FetchAll(browser2,path)
                else:
                    print ("no BB")

                finishmark_list.append(namemark)
                fbc = open('E:\\spiderdata\\finishmark.txt','a', encoding="utf-8")
                fbc.write(namemark)
                fbc.write("\n")
                fbc.close()
		
                browser2.quit()

    else:
        print ("no star")
    browser.quit()

	
	
inidir = "E:\\spiderdata\\urldata_name.txt"
fo = open(inidir,"r", encoding="utf-8")
with open(inidir,"r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        name = line.strip()
        if name in finishname_list:
            continue
        
        iurl = "https://www.tvmao.com/query.jsp?keys=" + name
        GetPIC(iurl, name)

        finishname_list.append(name)		
        fa = open('E:\\spiderdata\\finish.txt','a', encoding="utf-8")
        fa.write(line)
        fa.close()
        print (name)
fo.close()

