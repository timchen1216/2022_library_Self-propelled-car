from flask import Flask 
# 建立 application 物件
from flask import request
from flask import render_template
from flask import session

app = Flask(
    __name__,
    static_folder = "static" , # 靜態檔案的資料夾
    static_url_path = "/" #靜態資料夾對應的網址路徑
)
app.secret_key = "any string" #設定session密鑰
# 所有在 static 資料夾下的檔案都對應到網址路徑 /www/檔案名稱
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/show")
def show():
    name = request.args.get("n","")
    return "歡迎光臨," + name

@app.route("/page")
def page():
    return render_template("page.html")

@app.route("/hello")
def hello():
    name = request.args.get("name", "")
    session["username"] = name
    return "你好 " + name

@app.route("/talk")
def talk():
    name = session["username"]
    return name + " 很高興認識你"


@app.route("/Data")
def data():
    return "My Data"

@app.route("/user/<username>")
def user(username):
    return "Hello " + username

@app.route("/SUM")
def SUM():
    maxNumber = request.args.get("max" , 100)
    maxNumber = int(maxNumber)
    minNumber = request.args.get("min" , 1)
    minNumber = int(minNumber)
    result = 0 
    for n in range(minNumber , maxNumber + 1):
        result += n 
    return render_template("result.html",data=result)  

app.run(port = 1345)