import pymongo
client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.book

correct=db.correct
detect=db.detect
mis=db.mis

from flask import *
app = Flask(
    __name__,
    # static_folder="static",
    # static_url_path = "/"
)
app.secret_key = "any string"

#主頁
@app.route("/")
def index():
    return render_template("index.html")
#檢查操作
@app.route("/detectdata")
def detectdata():
    mis.drop()
    miss = []
    for i in range(1,5):
        cor = correct.find({
            "書櫃" : i
        })
        c = []#正確資料集合內 書櫃1~4內的編號
        for co in cor:
            c.append(co["編號"])
        
        det = detect.find({
            "書櫃" : i
        })
        d = []#偵測資料集合內 書櫃1~4內的編號
        for de in det:
            d.append(de["編號"])

        m = [ x for x in d if x not in c ]#在d列表中而不在c列表中

        for j in m:
            correctresult = correct.find_one({
                "編號" : j
            })
            detectresult = detect.find_one({
                "編號" : j
            })
            mis.insert_one({
                "編號" : j,
                "目前位置" : detectresult["書櫃"],
                "正確位置" : correctresult["書櫃"]
            })
            mistake = mis.find_one({
                "編號" : j
            })
            miss.append(mistake)

    total = 0
    misbook = mis.find()
    for doc in misbook:
        total += 1
    return render_template("check.html",miss = miss, total = total)
app.run()