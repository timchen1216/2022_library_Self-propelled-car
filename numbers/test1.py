import re, sqlite3
from flask import Flask, render_template, url_for, request
app = Flask(__name__)


number = '270.3'
dp = '2'

con = sqlite3.connect('LibraryWeb.db')
cur = con.cursor()
cur.execute(f"INSERT INTO detect (`number`, `dp`) VALUES ('{number}','{dp}')")
con.commit()
con.close()