import pymongo 
import simplejson as json
from pprint import pprint

mng_client = pymongo.MongoClient('localhost', 27017)
mng_db = mng_client['WT'] 
collection_gk = 'GK' 
db_gk = mng_db[collection_gk]
 
# General Knowledge
with open('gk.json', 'r') as data_file:
    data_gk = json.load(data_file)
 
db_gk.remove()
db_gk.insert(data_gk)


# cursor = db_gk.find({})
# for document in cursor: 
#     pprint(document)

#Science & nature,Science:computers
collection_science = 'SCIENCE'
db_science = mng_db[collection_science]
 
with open('science.json', 'r') as data_file:
    data_science = json.load(data_file)
 
db_science.remove()
db_science.insert(data_science)

#Entertainment
collection_entertainment = 'ENTERTAINMENT'
db_entertainment = mng_db[collection_entertainment]
 
with open('entertainment.json', 'r') as data_file:
    data_entertainment = json.load(data_file)
 
db_entertainment.remove()
db_entertainment.insert(data_entertainment)