import os
import sys
for s in sys.path:
    print(s)
#sys.path.append("/Users/krutheekarajkumar/PycharmProjects/Proj1env/bin")
from pymongo import MongoClient
from scrapper import formatted as data
from pprint import pprint
from datetime import date

today = date.today()
from random import randint

#client = MongoClient("mongodb+srv://KrutheekaMongo:NaaGeDt7tvUw8Ze@cluster0.syo7x.mongodb.net/test&ssl_cert_reqs=CERT_NONE")
client = MongoClient("mongodb+srv://KrutheekaMongo:NaaGeDt7tvUw8Ze@cluster0.syo7x.mongodb.net/test", ssl=True,ssl_cert_reqs='CERT_NONE')
#client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db=client.Proj0

vals = data()
print(vals)
mongoinserts = {}
toadd = []
newEntries = 0
print("Total Entries previously: ", db.Collection1.count_documents({}))
for val in vals:
    for k,v in val.items():
        mongoinserts[k] = v
        #mongoinserts['DateAdded'] = today
    if mongoinserts['JobID'] not in db.Collection1.distinct('JobID'):
        toadd.append(mongoinserts.copy())
        newEntries += 1
try:
    db.Collection1.insert_many(toadd)
    print("Total number of new entries added to the database: ", newEntries)
except:
    print("Database upto date and no new entries")
