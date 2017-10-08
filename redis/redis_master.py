# encoding=utf-8
import requests
from lxml import etree
import re
import pymongo
import random
import time
from user_agents import agents
import sys
reload(sys)   
sys.setdefaultencoding('utf8') 
from bs4 import BeautifulSoup
import os

import threading
import Queue
#import threadpool


import socket
import urllib2
import urllib

import hashlib


import redis

class Proxy(object):
    """docstring for Proxy"""
    def __init__(self,proxy_queue_maxsize,randsleep_t_min,randsleep_t_max):
        self.proxy_queue=Queue.Queue(proxy_queue_maxsize)
        self.header={}
        self.randsleep_t_min=randsleep_t_min
        self.randsleep_t_max=randsleep_t_max

    def get_ip_from_page(self,page_num):
        proxy_url = 'http://www.xicidaili.com/nn/'+str(page_num)
        time.sleep(random.randint(self.randsleep_t_min,self.randsleep_t_max))
        self.header['User-Agent'] = random.choice(agents)
        try:
            req = urllib2.Request(proxy_url,headers=self.header) #this must have headers
            res = urllib2.urlopen(req).read()
        except Exception,e:
            print e
            return 

        soup =BeautifulSoup(res,"lxml")
        ips = soup.findAll('tr')
        f = open("proxy_ip","a")

        for x in range(1,len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
            f.write(ip_temp)

    def update_get_proxy(self,beginpage,endpage):
        if os.path.exists('proxy_ip'):
            os.remove('proxy_ip')
        for i in range(beginpage,endpage+1):
            self.get_ip_from_page(i)

    def get_proxy_to_queue(self):#使用IP池的话，一大堆废IP，浪费感情，所以直接取第一面最新的
        f = open("proxy_ip")
        lines = f.readlines()
        for i in range(0,len(lines)):
            ip = lines[i].strip("\n").split("\t")
            proxy_host = "http://"+ip[0]+":"+ip[1]
            proxy_temp = {"http":proxy_host}
            self.proxy_queue.put(proxy_temp)
          


class Redis_Master(object):
    """docstring for Redis"""
    def __init__(self):  
        try:
            self.pool = redis.ConnectionPool(host='localhost', port=6379)
            self.r=redis.Redis(connection_pool=self.pool)
        except Exception,e:
            print e 
        
    
    def grab_orign(self,url,proxy):
        time.sleep(random.randint(1,3))
        header = {}
        header['User-Agent'] = random.choice(agents)
        
        try:
            res = urllib.urlopen(url,proxies=proxy).read()
            return res
        except Exception,e:
            print e
            return "None_page"        
        
    def rents_update(self):
        proxy_is_good=False
        proxy={}
        thread = threading.current_thread()
        t_name=thread.getName()
        while True:
            if proxy_is_good==False:
                proxy=Proxy_Obj.proxy_queue.get()
                if Proxy_Obj.proxy_queue.empty()==True:
                    Proxy_Obj.update_get_proxy(1,2)
                    Proxy_Obj.get_proxy_to_queue()

            page_num=random.randint(1,100)
            official_url="http://wh.lianjia.com/zufang/pg{0}/".format(str(page_num))
            res=self.grab_orign(official_url,proxy)
            if res=="None_page":
                proxy_is_good=False
                print t_name,'res=="None_page"'
                continue
            else:
                e_page=etree.HTML(res)
                rents_house_urls=set(e_page.xpath(u'//div[@class="pic-panel"]/a[@target="_blank"]/@href'))
                if len(rents_house_urls)>0:
                    for each_rent_url in rents_house_urls:
                        self.r.sadd('rents_urls',each_rent_url)
                        print t_name,each_rent_url,'("rents_urls")=',self.r.scard("rents_urls")
                proxy_is_good=True
            

    def ershoufang_update(self):
        proxy_is_good=False
        proxy={}
        thread = threading.current_thread()
        t_name=thread.getName()
        while True:
            if proxy_is_good==False:
                proxy=Proxy_Obj.proxy_queue.get()
                if Proxy_Obj.proxy_queue.empty()==True:
                    Proxy_Obj.update_get_proxy(1,2)
                    Proxy_Obj.get_proxy_to_queue()

            page_num=random.randint(1,100)
            official_url="http://wh.lianjia.com/ershoufang/pg{0}/".format(str(page_num))
            res=self.grab_orign(official_url,proxy)
            if res=="None_page":
                proxy_is_good=False
                print t_name,'res=="None_page"'
                continue
            else:
                e_page=etree.HTML(res)
                ershou_house_urls=set(e_page.xpath(u'//a[@class="img "]/@href'))
                if len(ershou_house_urls)>0:
                    for each_ershou_url in ershou_house_urls:
                        self.r.sadd('ershoufang_urls',each_ershou_url)
                        print t_name,each_ershou_url,'("ershoufang_urls")=',self.r.scard("ershoufang_urls")
                proxy_is_good=True


    def redis_thread_work(self):
        t1=threading.Thread(target=self.rents_update)
        #t1.setDaemon(True)
        t1.start()
        t2=threading.Thread(target=self.ershoufang_update)
        #t2.setDaemon(True)
        t2.start()
            

        
if __name__ == '__main__':


    
    Proxy_Obj=Proxy(proxy_queue_maxsize=200,randsleep_t_min=5,randsleep_t_max=10)

    Proxy_Obj.update_get_proxy(beginpage=1,endpage=2)

    Proxy_Obj.get_proxy_to_queue()

    ###print proxy_queue.qsize()

    Redis_Obj=Redis_Master()
    Redis_Obj.redis_thread_work()




   

        
        
        


























'''
class Redis(object):
    """docstring for Red"""
    def __init__(self, arg):
        super(Red, self).__init__()
        self.arg = arg

  
        






r.set('foo','Bar')
'''