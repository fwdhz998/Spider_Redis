import pymongo

if __name__ == '__main__':
    
    clinet = pymongo.MongoClient("localhost", 27017)
    db = clinet["Lianjia_by_fw"]

    print "db.collection_names======",db.collection_names()

    rents_db = db["house_for_renting"]

    rents_db.remove()

    print 'after ents_db.remove() '
    print "db.collection_names======",db.collection_names()
