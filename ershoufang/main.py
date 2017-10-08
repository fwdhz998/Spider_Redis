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

import urllib
import socket


import update_newest_proxy_to_file
import delete_dumps_then_pro_md5

import hashlib




def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def grab_orign(url,proxy):
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
    
    
    '''
    r=requests.get(url=url,headers=header,proxies=proxy)# 一定要带上headers
    if r.status_code == requests.codes.ok:
        return r.content
    else:
        print r.status_code
    '''
    
    
def grab(page,proxy):
    if page=="None_page":
        return
    e_page=etree.HTML(page)
    house_urls=set(e_page.xpath(u'//a[@class="img "]/@href'))
    print "len(house_urls)=",len(house_urls)
    for each_url in house_urls:
        grab_for_detail(grab_orign(each_url,proxy))

def grab_for_detail(page):
    #global rent_count
    if page=="None_page":
        return
    e_page=etree.HTML(page)
    
    house_name=e_page.xpath(u'//h1[@class="main"]/text()')
 

    if(len(house_name)>0):

        md5str=get_md5_value(house_name[0])

        if mutex.acquire():

            if md5_hash.has_key(md5str):
                mutex.release() ######日   这一条一定要有  死锁
                return  
            else:
                md5_hash[md5str]='1'

                write_md5_to_file(md5str)
                global ershoufang_count
                ershoufang_count+=1
                now_ershoufang_count=ershoufang_count

                mutex.release() #####lock must be thrown early and early

                    
                block_name_re=u'resblockName:\'(.*?)\','
                block_name=re.findall(block_name_re.encode('UTF-8'),page)
                if len(block_name)>0:
                    block_name=block_name[0]
                else:
                    block_name='block_None'


                rooms=e_page.xpath(u'//div[@class="room"]/div[@class="mainInfo"]/text()')
                if len(rooms)>0:
                    rooms=rooms[0]
                else:
                    rooms='rooms_None'


                area_re=u'area:\'(.*?)\','
                area=re.findall(area_re.encode('UTF-8'),page)
                if len(area)>0:
                    area=area[0]+u'平'
                else:
                    area='block_None'

                house_price=e_page.xpath(u'//div[@class="price "]/span[@class="total"]/text()')
                if len(house_price)>0:
                    house_price=house_price[0]+u'万'
                else:
                    house_price='house_price_None'


                unitPriceValue_re=u'<span class="unitPriceValue">(.*?)<i>'
                unitPriceValue=re.findall(unitPriceValue_re.encode('UTF-8'),page)
                if len(unitPriceValue)>0:
                    unitPriceValue=unitPriceValue[0]
                else:
                    unitPriceValue=''


                re_expression=u'resblockPosition:\'(.*?),(.*?)\''
                house_position_origin=re.findall(re_expression.encode('UTF-8'),page)#通过网页源码的前几行看出是什么编码，一定要注意解码
                if len(house_position_origin)>0:
                    house_position=house_position_origin[0]
                else:
                    return

                ershoufang_dict=dict()
                #ershoufang_dict[house_name[0]]=house_position#list的内容是可变的，不可hash，因此不能作为dict的keys
                ershoufang_dict["house_name"]=house_name[0]
                ershoufang_dict["house_xyposition"]=house_position
                ershoufang_dict["block_name"]=block_name
                ershoufang_dict["rooms"]=rooms
                ershoufang_dict["area"]=area
                ershoufang_dict["house_price"]=house_price
                ershoufang_dict["unitPriceValue"]=unitPriceValue
                
                 #不能直接threading.Lock().accquire,会报错 release unlocked lock ，因为产生的是一把新锁
                    
                   
                thread = threading.current_thread()
                print thread.getName(),now_ershoufang_count,house_name[0],rooms,area,house_price,unitPriceValue
                print house_position
                #ershoufang_db.insert(ershoufang_dict)
                data_queue.put(ershoufang_dict)

                
    else:
        print "house_name=NULL"


def test_ip():
    
    thread = threading.current_thread()
    t_name=thread.getName()
    while Is_Exit==False:
        print "proxys_queue.qsize()=",proxys_queue.qsize()
        page_num=random.randint(1,100)
        official_url="http://wh.lianjia.com/ershoufang/pg{0}/".format(str(page_num))
        proxy=proxys_queue.get()
        if proxys_queue.empty()==True:
            update_newest_proxy_to_file.update_get_proxy(1,2)
            get_proxy_to_queue()
        
        try:
            
            res=grab_orign(official_url,proxy)
            e_page=etree.HTML(res)
            house_urls=set(e_page.xpath(u'//a[@class="img "]/@href'))
        except Exception,e:

            print t_name,e
            continue

        if(len(house_urls)>0):#YAYAYAYAYAYAYAY cannot put this in try-except  This really hurt me 
            for each_url in house_urls:
                grab_for_detail(grab_orign(each_url,proxy))
            start_page=random.randint(1,50)
            end_page=random.randint(50,100)
            #start_page=1
            #end_page=100
            for i in range(start_page,end_page):
                page_url = "http://wh.lianjia.com/ershoufang/pg{0}/".format(str(i+1))
                print page_url
                grab(grab_orign(page_url,proxy),proxy)
    print t_name,'Quit success*****'

                
      
            
    

def get_proxy_to_queue():#使用IP池的话，一大堆废IP，浪费感情，所以直接取第一面最新的
    global proxys_queue
    f = open("proxy_ip")
    lines = f.readlines()
    for i in range(0,len(lines)):
        ip = lines[i].strip("\n").split("\t")
        proxy_host = "http://"+ip[0]+":"+ip[1]
        proxy_temp = {"http":proxy_host}
        proxys_queue.put(proxy_temp)
    
class MyThread(threading.Thread):

    def __init__(self,threadID):
        threading.Thread.__init__(self)
        self.threadID=threadID
        

    def run(self):
        print 'threadID=',self.threadID
        print '***********************'
        test_ip()

def work_much_thread(num_of_threads):

    for i in range(num_of_threads):
        threadi=MyThread(i+1)
        threadi.setDaemon(True)
        threadi.start()
        

def MongoInit():

    clinet = pymongo.MongoClient("localhost", 27017)
    db = clinet["Lianjia_by_fw"]
    ershoufang_db = db["ershoufang"]
    print"******MongoInit() success*****"
    return ershoufang_db


def md5_file_to_hash():
    md5_hash={}
    md5_file=open('housename_md5.txt')
    lines = md5_file.readlines()
    
    for i in range(0,len(lines)):
        md5=lines[i][:-1]  #This really hurt me  it's i
        md5_hash[md5]='1'
    return md5_hash

def write_md5_to_file(md5str):
    f=open('housename_md5.txt','a')
    f.write(md5str)
    f.write('\n')
'''
def own_ip_for_grab():

    thread = threading.current_thread()
    t_name=thread.getName()
    while True:
        proxy={}
        page_num=1
        official_url="http://wh.lianjia.com/ershoufang/pg{0}/".format(str(page_num))
        
        try:
            res=grab_orign(official_url,proxy)
            e_page=etree.HTML(res)
            house_urls=set(e_page.xpath(u'//a[@class="img "]/@href'))
            if(len(house_urls)>0):
                for each_url in house_urls:
                    time.sleep(2)
                    grab_for_detail(grab_orign(each_url,proxy))
                for i in range(100):
                    page_url = "http://wh.lianjia.com/ershoufang/pg{0}/".format(str(i+1))
                    print page_url
                    time.sleep(2)
                    grab(grab_orign(page_url,proxy),proxy)

                
        except Exception,e:
            print t_name,e,"own_ip******"

'''
def data_queue_to_db(data_queue,ershoufang_db):
    thread = threading.current_thread()
    t_name=thread.getName()
    while True:
        while data_queue.empty()==False:
            print t_name,"data_queue.qsize()=",data_queue.qsize()
            ershoufang_db.insert(data_queue.get())
            


if __name__=='__main__':

    socket.setdefaulttimeout(4)#时间不能设置太短 ，特别是在代理IP时，代理可能导致TCP连接更耗时

    update_newest_proxy_to_file.update_get_proxy(1,2)#从代理IP网站中获取最新的可用IP地址，(1,2)两页

    proxys_queue=Queue.Queue()#代理队列：包括IP PORT

    get_proxy_to_queue()

    delete_dumps_then_pro_md5.run() #md5算法url去重


    global Is_Exit
    Is_Exit=False

    ershoufang_count=0
    
    ershoufang_db=MongoInit()

    data_queue=Queue.Queue() #后台数据采集-存储线程,解析到的数据存储到mongo
    t=threading.Thread(target=data_queue_to_db,args=(data_queue,ershoufang_db))
    t.start()

    md5_hash=md5_file_to_hash()


    mutex=threading.Lock()
    
    num_of_threads=4
    try:
        work_much_thread(num_of_threads)#线程太多，反而不好
        while True: #setDaemon  main thread quit quickly
            pass
    except KeyboardInterrupt:
        

        print '******Now prepare to close All******\n'
        print '******Now prepare to close All******\n'
        print '******Now prepare to close All******\n'
        print '******Now prepare to close All******\n'
        print '******Now prepare to close All******\n'
        print '******Now prepare to close All******\n'

        fi = open("housename_md5.txt")
        lines = len(fi.readlines())
        

        while ershoufang_db.count()!=lines:
            pass

        Is_Exit=True


        print 'ershoufang_db.count()=',ershoufang_db.count()
        print 'housename_md5.txt.lines=',lines
        print '******Now Everything is closed******\n'
    
   # t=threading.Thread(target=own_ip_for_grab)
    #t.start()
    
    