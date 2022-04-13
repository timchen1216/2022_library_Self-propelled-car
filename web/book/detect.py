import pymongo
client = pymongo.MongoClient("mongodb+srv://timechen:timechen@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.book

correct=db.correct
detect=db.detect
mis=db.mis

correct.drop()
# correct.insert_one({
#      "書櫃":1,
#      "編號":"625.8"
# })

# detect.insert_one({
#     "書櫃":"b",
#     "編號":"714.8"
# })
