import numpy as np
import pymongo

client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client.book

correct=db.correct
detect=db.detect
mis=db.mis

b = '1'
a = [1, 2, 3, 4]

detect.insert_one({
    "書櫃":b,
    "編號":b,
})