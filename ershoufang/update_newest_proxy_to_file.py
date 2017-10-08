#encoding=utf8
import urllib2
from bs4 import BeautifulSoup
from lxml import etree
import urllib
import socket
import re
socket.setdefaulttimeout(10)
import sys
import os
import time
import random
from user_agents import agents

header = {}
header['User-Agent'] = random.choice(agents)

def get_ip_from_page(page):
    url = 'http://www.xicidaili.com/nn/'+str(page)
    time.sleep(random.randint(10,20))
    print url
    header['User-Agent'] = random.choice(agents)
    req = urllib2.Request(url,headers=header) #this must have headers
    res = urllib2.urlopen(req).read()

    soup =BeautifulSoup(res)
    ips = soup.findAll('tr')
    f = open("proxy_ip","a")

    for x in range(1,len(ips)):
        ip = ips[x]
        tds = ip.findAll("td")
        ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
        # print tds[2].contents[0]+"\t"+tds[3].contents[0]
        f.write(ip_temp)

def update_get_proxy(beginpage,endpage):
    if os.path.exists('proxy_ip'):
        os.remove('proxy_ip')
    for i in range(beginpage,endpage+1):
        get_ip_from_page(i)

if __name__ == '__main__':
    update_get_proxy(1,1)







