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
#Redis的Set是string类型的无序集合。集合成员是唯一的，这就意味着集合中不能出现重复的数据。
#Redis 中 集合是通过哈希表实现的，所以添加，删除，查找的复杂度都是O(1)。
#集合中最大的成员数为 232 - 1 (4294967295, 每个集合可存储40多亿个成员)。

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


class Mongo(object):
    """docstring for ClassName"""
    def __init__(self):
        self.clinet=pymongo.MongoClient("localhost", 27017)
        self.db=self.clinet["Lianjia_by_redis"]
    def MongoInit(self):
        rents_db =self.db["rents"]
        print"******MongoInit() success*****"
        return rents_db



class Redis_Rents(object):
    """docstring for Redis_Ershoufang"""
    def __init__(self):
        try:
            self.r=redis.Redis(host='115.156.186.125',port=6379)
        except Exception as e:
            print e
        

    def grab_orign(self,url,proxy):
        time.sleep(random.randint(1,3))
        #User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
        header = {}
        header['User-Agent'] = random.choice(agents)
        
        try:
            res = urllib.urlopen(url,proxies=proxy).read()
            return res
        except Exception,e:
            print e
            return "None_page"
    
    
    def grab_for_detail(self,page):
        #global rent_count
        if page=="None_page":
            return
        e_page=etree.HTML(page)
        re_expression=u'resblockPosition:\'(.*?),(.*?)\''
        house_name=e_page.xpath(u'//h1[@class="main"]/text()')
        if(len(house_name)>0):
            house_position_origin=re.findall(re_expression.encode('UTF-8'),page)#通过网页源码的前几行看出是什么编码，一定要注意解码
            if len(house_position_origin)>0:
                house_position=house_position_origin[0]
            else:
                return
            rents_dict=dict()
            #rents_dict[house_name[0]]=house_position#list的内容是可变的，不可hash，因此不能作为dict的keys
            rents_dict["house_name"]=house_name[0]
            rents_dict["house_xyposition"]=house_position
            
             #不能直接threading.Lock().accquire,会报错 release unlocked lock ，因为产生的是一把新锁
                
               
            thread = threading.current_thread()
            print thread.getName(),house_name[0],house_position
            rents_db.insert(rents_dict)
        else:
            return "None_house_name"



    def start_work(self):
        proxy_is_good=False
        proxy={}
        thread = threading.current_thread()
        t_name=thread.getName()
        while True:
            
            rent_url = self.r.spop('rents_urls')
            print t_name,"proxy_queue.qsize()=",Proxy_Obj.proxy_queue.qsize()
            if proxy_is_good==False:
                proxy=Proxy_Obj.proxy_queue.get()
                if Proxy_Obj.proxy_queue.empty()==True:
                    Proxy_Obj.update_get_proxy(1,2)
                    Proxy_Obj.get_proxy_to_queue()

            res=self.grab_orign(rent_url,proxy)
            if res=="None_page":
                proxy_is_good=False
                self.r.sadd('rents_urls',rent_url)#没有得到请求页面的要上交给master
                print t_name,'res=="None_page",then give it back to redis’'
                continue
            else:
                house_name=self.grab_for_detail(res)
                if house_name=="None_house_name":
                    self.r.sadd('rents_urls',rent_url)#没有正确解析的要上交给master
                    print t_name,"house_name=NULL,then give it back to redis"
                    proxy_is_good=False
                else:
                    proxy_is_good=True

                
    def redis_threads_work(self,num_threads):
        for i in range(num_threads):
            threadi=threading.Thread(target=self.start_work)
            #threadi.setDaemon(True)
            threadi.start()


if __name__ == '__main__':

    Proxy_Obj=Proxy(proxy_queue_maxsize=200,randsleep_t_min=5,randsleep_t_max=10)
    Proxy_Obj.update_get_proxy(beginpage=1,endpage=2)
    Proxy_Obj.get_proxy_to_queue()

    ###print proxy_queue.qsize()

    Mongodb=Mongo()
    rents_db=Mongodb.MongoInit()


    Redis_Obj=Redis_Rents()
    Redis_Obj.redis_threads_work(4)
