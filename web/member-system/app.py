import pymongo
client = pymongo.MongoClient("mongodb+srv://che:che@mycluster.6t3lr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test

from flask import *
app = Flask(
    __name__,
    # static_folder="static",
    # static_url_path = "/"
)
app.secret_key = "any string"
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")

@app.route("/error")
def error():
    message = request.args.get("msg","錯誤")
    return render_template("error.html", message = message)

@app.route("/signup", methods = ["POST"])
def signup():
    #從前端接收資料
    nickname = request.form["nickname"]
    email = request.form["email"]
    password =  request.form["password"]
    #檢查接收到的資料和資料庫互動
    collection = db.user
    #檢查是否有相同email
    result = collection.find_one({
        "email" : email
    })
    if result != None:
        return redirect("/error?msg=信箱已被註冊")
        
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/success")
@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/signin", methods = ["POST"])
def signin():
    #從前端使取得使用者的輸入
    email = request.form["email"]
    password = request.form["password"]
    #和資料庫作互動
    collection = db.user
    #檢查帳密是否正確
    result = collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    #找不到對應的帳號
    if result == None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    #登入成功，在session紀錄會員資訊，導向會員網頁
    session["nickname"] = result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
    #移除session中的會員資訊
    del session["nickname"]
    return redirect("/")

app.run(port = 1345)