import pymongo
from bson.objectid import ObjectId
client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
collection = db.users

# data = collection.find_one(ObjectId("623aabe39b85d74d11a41ae0"))
# print(data)
# print(data["_id"])
# print(data["name"])
cursor = collection.find()
print(cursor)
for doc in cursor:
    print(doc["name"])
# print("資料新增成功")
