from crypt import methods
from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from cs50 import SQL
import random
import ast
from helpers import login_required, act_calculate

app = Flask("__name__")
db = SQL("sqlite:///foodname.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET","POST"])
def index():
    if (request.method == "GET"):
        return render_template("input_tester.html")
    else:
        # 一人当たりの必要摂取カロリー
        age = request.form.get("age")
        intAge = int(age)
        weight = request.form.get("weight")
        intWeight = int(weight)
        height = request.form.get("height")
        intHeight = int(height)
        budget = request.form.get("budget")
        intBudget = int(budget)
        # 性別
        sex = request.form.get("sex")
        # 活動レベル
        level = request.form.get("level")
        # 目的
        activity = request.form.get("activity")

        # 必要摂取カロリーの計算
        act = act_calculate(sex, intWeight, intHeight, intAge, level, activity)

# --------------------------------------------------------------------
# D = act - (朝で摂取したエネルギー + 昼で摂取したエネルギー) [kcal]
# --------------------------------------------------------------------

        total_energy = 0
        total_protein = 0
        total_lipid = 0
        total_carbohydrate = 0
        fDicts = request.form.getlist("select_food")
        for fDict in fDicts:
            Dict = ast.literal_eval(fDict)
            total_energy += int(Dict['エネルギー'])
            total_protein += int(Dict['たんぱく質'])
            total_lipid += int(Dict['脂質'])
            total_carbohydrate += int(Dict['炭水化物'])

        # 1日に必要な三大栄養素
        P = 2 * intWeight
        F = act * 0.25
        CBH = act - P - F

        # 夜に必要な三大栄養素
        difP = P - total_protein
        difF = F - total_lipid
        difCBH = CBH - total_carbohydrate

        D = act - total_energy

        # -カロリー*0.3< カロリー - act< カロリー*0.3
        # db.execute("SELECT * FROM foodnames WHERE
        data = db.execute("SELECT * FROM foodnames WHERE カロリー < ?", D)

        return render_template("output_tester.html", data = data)


@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    if request.method == "POST":
        breakfasts = request.form.getlist("breakfast")
        lunchs = request.form.getlist("lunch")
        snacks = request.form.getlist("snack")
        sql = "SELECT * FROM 食品成分 WHERE 食品名 like ?"
        brName = []
        luName = []
        snName = []
        for breakfast in breakfasts:
            if len(breakfast) != 0:
                brName += db.execute(sql, "%" + breakfast + "%")
        for lunch in lunchs:
            if len(lunch) != 0:
                luName += db.execute(sql, "%" + lunch + "%")
        for snack in snacks:
            if len(snack) != 0:
                snName += db.execute(sql, "%" + snack + "%")
        return render_template("input_tester.html", breakfast=brName, lunch=luName, snack=snName)


@app.route("/select_item", methods=["GET", "POST"])
def select_item():
    if request.method == "POST":
        total = 0
        fDicts = request.form.getlist("select_food")
        for fDict in fDicts:
            total += fDict['エネルギー']
        return render_template("input_tester.html")


@app.route("/back")
def back():
    return render_template("input_tester.html")




# -------------------------------------------------------上がテスター------------------------------------------------------------------




@app.route("/recommend", methods=["GET","POST"])
def recommend():
    foods = []
    if (request.method == "POST"):
        # favs : [value1, value2, value3, ・・・]
        favs = request.form.getlist("fav")
        for fav in favs:
            foods += db.execute("SELECT * FROM foodnames WHERE カテゴリ = ?", fav)
        foodsRecommend = random.sample(foods, 3)
        return render_tempalate("output.html", foods=foodsRecommend)



@app.route("/home",methods=["GET","POST"])
def home():
    if (request.method == "GET"):
        return render_template("home.html")
    else:
        pass


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        name = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", name)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

