import pymongo
client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.book

correct=db.correct
detect=db.detect
mis=db.mis
mis.drop()
total=0
cc = correct.find()
for doc in cc:
    total += 1

print(total)
# detect.insert_one({
#     "書櫃" : 2,
#     "編號" : 172.1 
# })

# detect.insert_one({
#     "書櫃" : 2,
#     "編號" : 268.4 
# })
# miss = []
# for i in range(1,5):
#     cor = correct.find({
#         "書櫃" : i
#     })
#     c = []#正確資料集合內 書櫃1~4內的編號
#     for co in cor:
#         c.append(co["編號"])
    
#     det = detect.find({
#         "書櫃" : i
#     })
#     d = []#偵測資料集合內 書櫃1~4內的編號
#     for de in det:
#         d.append(de["編號"])

#     m = [ x for x in d if x not in c ]#在d列表中而不在c列表中

#     for j in m:
#         correctresult = correct.find_one({
#             "編號" : j
#         })
#         detectresult = detect.find_one({
#             "編號" : j
#         })
#         mis.insert_one({
#             "編號" : j,
#             "目前位置" : detectresult["書櫃"],
#             "正確位置" : correctresult["書櫃"]
#         })
#         mistake = mis.find_one({
#             "編號" : j
#         })
#         miss.append(mistake)







# #正確資料庫書櫃1的編號143.5 172.1 198.6
# cor1 = correct.find({
#     "書櫃" : 1
# })
# c1 = []
# for co1 in cor1:
#     c1.append(co1["編號"])
# #偵測資料庫書櫃1的編號143.5 250.4
# det1 = detect.find({
#     "書櫃" : 1
# })
# d1 = []
# for de1 in det1:
#     d1.append(de1["編號"])
# #找出錯誤的書 c是list
# c = [ x for x in d1 if x not in c1 ]#在d1列表中而不在c1列表中
# g =[]#正確的data
# gg = []#錯誤的data
# miss = []
# for n in c:
#     result = correct.find_one({
#         "編號" : n
#     })
#     detectresult = detect.find_one({
#         "編號" : n
#     })
#     g.append(result)
#     gg.append(detectresult)
#     mis.drop()
#     mis.insert_one({
#         "編號" : n,
#         "目前位置" : result["書櫃"],
#         "正確位置" : detectresult["書櫃"]
#     })
#     mistake = mis.find_one({
#         "編號" : n
#     })
#     miss.append(mistake)

# print(miss)