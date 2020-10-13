from pymongo import MongoClient
from scrapper import formatted as data
from pprint import pprint

from random import randint

#client = MongoClient("mongodb+srv://KrutheekaMongo:NaaGeDt7tvUw8Ze@cluster0.syo7x.mongodb.net/test&ssl_cert_reqs=CERT_NONE")
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db=client.Proj0

vals = data()
mongoinserts = {}
toadd = []
for val in vals:
    for k,v in val.items():
        mongoinserts[k] = v
    print(mongoinserts)
    toadd.append(mongoinserts.copy())
    print("****")
db.Collection1.insert_many(toadd)
