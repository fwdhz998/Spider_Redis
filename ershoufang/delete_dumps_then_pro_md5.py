import pymongo
import os
import sys
reload(sys)   
sys.setdefaultencoding('utf8') 
clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["Lianjia_by_fw"]

print "db.collection_names======",db.collection_names()

ershoufang_db = db["ershoufang"]


import hashlib

def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest

def run():
    md5_hash=dict()

    if os.path.exists('housename_md5.txt'):
        os.remove('housename_md5.txt')
    f=open('housename_md5.txt','w')

    

    #print 'ershoufang_db.count()=',ershoufang_db.count()

    for item in ershoufang_db.find():
        
        
        md5str=get_md5_value(item["house_name"])
        
       

        if md5_hash.has_key(md5str):
           
          
            ershoufang_db.remove({"house_name":item["house_name"]}) #This is wrong remove({item["house_name"]item["house_xyposition"]})
        else:
            md5_hash[md5str]='1'
            f.write(md5str)
            f.write('\n')
    #print 'ershoufang_db.count()=',ershoufang_db.count()

if __name__ == '__main__':  
    
    print 'ershoufang_db.count()=',ershoufang_db.count()
    run()
    print 'ershoufang_db.count()=',ershoufang_db.count()

                