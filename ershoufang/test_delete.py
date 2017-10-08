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

import threading
import Queue
import threadpool

import urllib
import urllib2
import socket
socket.setdefaulttimeout(5)#时间不能设置太短 

import hashlib




r=requests.get(url='http://wh.lianjia.com/ershoufang/104100169615.html')
page=r.content
e_page=etree.HTML(page)

#house_position_origin=re.findall(re_expression.encode('UTF-8'),page)



block_name_re=u'resblockName:\'(.*?)\','
block_name=re.findall(block_name_re.encode('UTF-8'),page)[0]

rooms=e_page.xpath(u'//div[@class="room"]/div[@class="mainInfo"]/text()')[0]

area_re=u'area:\'(.*?)\','
area=re.findall(area_re.encode('UTF-8'),page)[0]+"平"

house_price=e_page.xpath(u'//div[@class="price "]/span[@class="total"]/text()')[0]
house_price=house_price+u'万'

unitPriceValue_re=u'<span class="unitPriceValue">(.*?)<i>'
unitPriceValue=re.findall(unitPriceValue_re.encode('UTF-8'),page)[0]






print block_name,rooms,area,house_price,unitPriceValue