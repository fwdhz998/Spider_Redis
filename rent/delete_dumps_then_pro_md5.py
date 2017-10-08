import pymongo
import os
import sys
reload(sys)   
sys.setdefaultencoding('utf8') 
clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["Lianjia_by_fw"]

print "db.collection_names======",db.collection_names()

rents_db = db["house_for_renting"]


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

    

    #print 'rents_db.count()=',rents_db.count()

    for item in rents_db.find():
        
        
        md5str=get_md5_value(item["house_name"])
        
       

        if md5_hash.has_key(md5str):
           
          
            rents_db.remove({"house_name":item["house_name"],"house_xyposition":item["house_xyposition"]}) #This is wrong remove({item["house_name"]item["house_xyposition"]})
        else:
            md5_hash[md5str]='1'
            f.write(md5str)
            f.write('\n')
    #print 'rents_db.count()=',rents_db.count()

if __name__ == '__main__':  
    
    print 'rents_db.count()=',rents_db.count()
    run()
    print 'rents_db.count()=',rents_db.count()
    



                