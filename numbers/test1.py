import re, sqlite3
from flask import Flask, render_template, url_for, request
app = Flask(__name__)

con = sqlite3.connect('LibraryWeb.db')
cur = con.cursor()

# number = '123.4'
# dp = '4'
# cur.execute(f"INSERT INTO detect (`number`, `dp`) VALUES ('{number}','{dp}')")

correct = {}
for cor in cur.execute(f'SELECT * FROM correct'):
    correct[cor[1]] = int(cor[2])
print(correct)

miss = []
detect = []
total = 0
for det in cur.execute(f'SELECT * FROM detect'):
    print(correct[det[1]])    
    if correct[det[1]] != int(det[2]):        
        total += 1
        number, dp, cp = det[1], det[2], correct[det[1]]
        m = [number, dp, cp]
        miss.append(m)    

for mis in miss:
    cur.execute(f"INSERT INTO miss (`number`, `dp`, `cp`) VALUES ('{mis[0]}','{mis[1]}','{mis[2]}')")

con.commit()
con.close()