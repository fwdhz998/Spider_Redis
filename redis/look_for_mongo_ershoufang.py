import pymongo


if __name__ == '__main__':
    
    clinet = pymongo.MongoClient("localhost", 27017)
    db = clinet["Lianjia_by_redis"]
    print "db.collection_names==",db.collection_names()
    ershoufang_db = db["ershoufang"]
    i=0
    for item in ershoufang_db.find():
        i+=1
        print i,item["house_name"],item["house_price"],item["house_xyposition"]

