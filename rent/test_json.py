
# encoding=utf-8
import pymongo
import os
import sys
import json
reload(sys)   
sys.setdefaultencoding('utf8') 
clinet = pymongo.MongoClient("localhost", 27017)
db = clinet["Lianjia_by_fw"]

print "db.collection_names======",db.collection_names()

rents_db = db["house_for_renting"]

#{"coord":[120.14322240845,30.236064370321],"elevation":21}

f=open("house_elevation_coord_data.json","w")

f.write("[")
f.write("[")
count=0
for item in rents_db.find():

    count+=1

    price=int(item["house_name"].split()[2][:-1])

    item_position=item["house_xyposition"]

    coord=[float(each) for each in item_position]

    #print price,coord

    json_dict={}

    json_dict["coord"]=coord

    json_dict["elevation"]=price

    json_dict["housename"]=item["house_name"]

    json_data=json.dumps(json_dict)

    f.write(json_data)
    
    if(count!=rents_db.count()):
        f.write(",")


f.write("]")
f.write("]")

f.close()