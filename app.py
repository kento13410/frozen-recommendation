from flask import Flask, render_template
from cs50 import SQL

app = Flask("__name__")
db = SQL("sqlite:///foodname.db")

url = db.execute("SELECT * FROM foodnames")[0]["画像"]
print(url)

@app.route("/")
def index():
 return render_template("home.html", url=url)




