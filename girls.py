# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 14:07:45 2018

@author: plato
Self-made scrawler for beautiful Camgirls
抓取花椒直播平台上的漂亮小姐姐！！！
"""
#思路：
#获取直播间id
#获取主播id
#匹配数据

import requests #请求网页库
import re #匹配数据
from bs4 import BeautifulSoup #解析数据
import urllib


def get_Liveid_and_Covers():
    Liveid = set() #抓取直播间id / get streaming room id number
    Cover_link = set()    
    response = requests.get('https://www.huajiao.com/category/2') #请求网页 / request visit website
    soup = BeautifulSoup(response.text,'html.parser') #解析网页输出为text格式 / inspect website code and translate to text
    for link in soup.find_all('img',src=re.compile('(320.jpg)')):
        cover = link.attrs['src']
        Cover_link.add(cover)
   #print(Cover_link)    
    for link in soup.find_all('a',href=re.compile('^(/l/)')):
        href = link.attrs['href']
        id = re.findall('[0-9]+',href)
        Liveid.add(id[0])
    #print('Liveid')
    #print(Liveid)
    return Liveid, Cover_link 
'''
def get_cover():
    Cover = set()
    response = requests.get('https://www.huajiao.com/category/2')
    soup = BeautifulSoup(response.text,'html.parser')
    for link in soup.find_all('img',src=re.compile('(320.jpg)')):
        cover = link.attrs['src']
        Cover.add(cover)
    print(Cover)
    return Cover
'''
  
def get_user_id(Liveid):
    Liveid = list(Liveid)
    userid = set()
    for i in Liveid:
        uid = 'https://www.huajiao.com/l/{id}'.format(id=i)
        response = requests.get(uid)
        soup = BeautifulSoup(response.text,'html.parser')
        #text = soup.title.get_text()
        #user_id = re.findall('[0-9]+',text) #利用这则表达式匹配 / find with regular expression
        id = str(soup.find('div',{'class':'content'}).span)
        user_id = re.findall('[0-9]+',id)
        userid.add(user_id[0])
        #print(userid)
    userid = list(userid)
    #print(userid)
    for i in userid:
        if (len(i)<5):
            userid.remove(i)    
    #print('userid')
    #print(userid)
    return userid
    
def get_user_data(userid):
    image = set()
    for i in userid:
        result = requests.get('https://www.huajiao.com/user/{}'.format(i))
        if result.status_code != 404:           
            soup = BeautifulSoup(result.text,'html.parser')
            userinfo = soup.find('div',id="userInfo") #查找soap中的div标签，div标签中含有id="userInfo"的位置
            data = userinfo.find('div',{'class':'avatar'}).img.attrs['src']
            '''
            大括号中内容就是class=avatar avatar-v personal，和上一行id="userInfo"作用一样
            python中不能使用class=。。。。；
            .attrs['src']作用：提取指定位置src标签后的内容，src为标签名字可按需替换
            '''
            image.add(data)
            #print(data)
    image = list(image)
    return image

def get_save_image(link,name):
    filename = 1
    for url in link:
        urllib.request.urlretrieve(url,'{}{}.jpg'.format(name,filename))
        filename += 1
    
Liveid,Cover_link = get_Liveid_and_Covers()
get_save_image(Cover_link,'cover')
userid = get_user_id(Liveid)
image = get_user_data(userid)  
get_save_image(image,'avatar')