# encoding=utf-8
import sys
reload(sys)   
sys.setdefaultencoding('utf8') 
import requests
from lxml import etree

import urllib2
import re
import time
import random

 
from StringIO import StringIO
import gzip


import zlib
import chardet
import urllib

import cookielib,httplib  


url='http://www.kuaidaili.com/free/outha/'
from selenium import webdriver 


driver = webdriver.Firefox() 
#driver.set_window_size(1366, 768) 
driver.get("http://www.kuaidaili.com/") 
#time.sleep(10) 
bodyStr= driver.find_element_by_tag_name("table").get_attribute("innerHTML") 
driver.quit()

print bodyStr 


    
    
    






    
    
