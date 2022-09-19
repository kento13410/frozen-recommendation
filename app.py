from crypt import methods
from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
import random
import ast
from flask_session import Session
from helpers import login_required, act_calculate, loading_black, loading_colorful
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask("__name__")

#_________________________________Sessionのdictオブジェクトを作成__________________________________________
app.config["SESSION_PERMANENT"] = False
# セッションの保存期間を指定
app.config["SESSION_TYPE"] = "filesystem"
#　ファイルとしてflask_sessionというセッションデータベースを作成する。
Session(app)
# 作成したセッションファイルとアプリを接続
#---------------------------------------------------------------------------------------------------------

# sqliteをデータベースに接続する
db = SQL("sqlite:///foodname.db")
db1 =SQL("sqlite:///users.db")

#------------------------------
#     LOGIN機能の実装:
#------------------------------

#----------------------------------------ログイン画面(login)--------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
@login_required
def login():
    """Log user in"""

    # sessionの情報を消す
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if (request.method == "POST"):

        # Ensure username was submitted
        username = request.form.get("username")
        password = request.form.get("password")
        if not username :
            raise Exception('ユーザー名を入力してください！！！')
        if not password :
            raise Exception('パスワードを入力してください！！！')

        # Query database for username
        rows = db1.execute("SELECT * FROM users WHERE username = ?", username)

        if (check_password_hash(rows[0]["hash"], password)):

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
# ---------------------------------------------------------------------------------------------------------------

# --------------------------------------登録画面(register)---------------------------------------------------
@app.route("/register",methods=["GET","POST"])
def register():
    if (request.method=="GET"):
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username :
            raise Exception('ユーザー名を入力してください！！！')
        if not password :
            raise Exception('パスワードを入力してください！！！')
        if not confirmation:
            raise Exception('確認パスワードも入力してください！！！')

        if password != confirmation:
            raise Exception('パスワードが一致してないでよ！')

        # データの登録
        db1.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, generate_password_hash(password))

        return redirect("/login")


# ------------------------------------------------------------------------------------------------------------

#______________________________________ログアウト画面(logout)__________________________________________________
@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
#______________________________________________________________________________________________



# ------------------------------------ホーム画面(home)--------------------------------------------------------
@app.route("/",methods=["GET","POST"])
@login_required
# @loading_black
def home():
    data = db.execute("SELECT * FROM foodnames")
    count = 0
    return render_template("main/home.html", data=data, count=count)
# -------------------------------------------------------------------------------------------------------------


# ------------------------------------------入力画面(input)----------------------------------------------------
@app.route("/input", methods=["GET","POST"])
@login_required
def index():
    if (request.method == "GET"):
        return render_template("main/input.html")

    else:
        # 一人当たりの必要摂取カロリー
        personal_data = db1.execute("SELECT * FROM personal_data WHERE user_id = ?", session['user_id'])[0]
        age = personal_data['age']
        weight = personal_data['weight']
        height = personal_data['height']
        sex = personal_data['choice']
        activity = personal_data['activity']

        level = request.form.get("level")
        budget = request.form.get("budget")
        act = act_calculate(sex, weight, height, age, level, activity)


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
            total_energy += abs(int(Dict['エネルギー']))
            total_protein += abs(int(Dict['たんぱく質']))
            total_lipid += abs(int(Dict['脂質']))
            total_carbohydrate += abs(int(Dict['炭水化物']))

        # 1日に必要な三大栄養素
        P = 2 * weight
        P_cal = P * 4
        F_cal = act * 0.25
        F = F_cal / 9
        CBH_cal = act - P_cal - F_cal
        CBH = CBH_cal / 4

        # 夜に必要な三大栄養素
        difP = P - total_protein
        difF = F - total_lipid
        difCBH = CBH - total_carbohydrate

        # 三大栄養素の不足分
        X = difP/P + difF/F + difCBH/CBH

        D = act - total_energy

        difData = {'カロリー': D, 'タンパク質': difP, '脂質': difF, '炭水化物': difCBH}

        data = db.execute("SELECT * FROM foodnames ORDER BY ? - (タンパク質/? + 脂質/? + 炭水化物/?) LIMIT 30", X, P, F, CBH)

        data2 = []
        for dat in data:
            data2_set = []
            data2_set.append(dat)
            difP2 = difP - dat['タンパク質']
            difF2 = difF - dat['脂質']
            difCBH2 = difCBH - dat['炭水化物']
            X2 = difP2/P + difF2/F + difCBH2/CBH
            data_element2 = db.execute("SELECT * FROM foodnames ORDER BY ? - (タンパク質/? + 脂質/? + 炭水化物/?) LIMIT 10", X2, P, F, CBH)
            for i in range(len(data_element2)):
                data2_set.append(data_element2[i])
                data2.append(data2_set)


        return render_template("output_tester.html", data = data, data2 = data2, difData=difData)
# ----------------------------------------------------------------------------------------


# -----------------------------入力と合致する食品の栄養情報を取得---------------------------

@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    if request.method == "POST":
        breakfasts = request.form.getlist("breakfast")
        lunches = request.form.getlist("lunch")
        snacks = request.form.getlist("snack")
        sql = "SELECT * FROM 食品成分 WHERE 食品名 like ?"
        brName = []
        luName = []
        snName = []
        for breakfast in breakfasts:
            if len(breakfast) != 0:
                brName += db.execute(sql, "%" + breakfast + "%")
        for lunch in lunches:
            if len(lunch) != 0:
                luName += db.execute(sql, "%" + lunch + "%")
        for snack in snacks:
            if len(snack) != 0:
                snName += db.execute(sql, "%" + snack + "%")

        return render_template("input.html", breakfast=brName, lunch=luName, snack=snName)

# -------------------------------------------------------------------------------------------------------------



@app.route("/back")
def back():
    return render_template("input.html")


# -------------------------recommend--------------------------------------------------------------------------------

@app.route("/recommend", methods=["GET","POST"])
def recommend():
    if (request.method == "POST"):
    # クリックされたカテゴリの取得

        # お弁当肉系
        beaf = request.form.get("beaf")
        # お弁当魚系
        fish = request.form.get("fish")
        # 米飯系
        rice = request.form.get("rice")
        # 麺系
        noodle = request.form.get("noodle")

        if (beaf):
            beafList = db.execute("SELECT * FROM foodnames WHERE カテゴリ = ?",beaf)
        else:
            beafList = []
        if (fish):
            fishList = db.execute("SELECT * FROM foodnames WHERE カテゴリ = ?",fish)
        else:
            fishList = []
        if (rice):
            riceList = db.execute("SELECT * FROM foodnames WHERE カテゴリ = ?",rice)
        else:
            riceList = []
        if (noodle):
            noodleList = db.execute("SELECT * FROM foodnames WHERE カテゴリ = ?",noodle)
        else:
            noodleList = []


        #何かしらの条件に従ってこのリストに入れていく
        selectedList = []
        # リストの連結 [{1},{2},.......{n}]となる
        for element in beafList:
            selectedList.append(element)
        for element in fishList:
            selectedList.append(element)
        for element in riceList:
            selectedList.append(element)
        for element in noodleList:
            selectedList.append(element)

        # recommnedで表示する冷凍食品リストを
        recommendList = []
        # ５つの商品をランダムにとってくる。
        for i in range(5):
            index = random.randrange(len(selectedList))
            recommendList.append(selectedList[index])
        return render_template("recommend.html",recommendList=recommendList)

# ------------------------------------------------------------------------------------------------------------------





@app.route("/personal_data", methods=['GET', 'POST'])
def personal_data():
    if request.method == 'POST':
        try:
            session['age'] = int(request.form.get("age"))
            session['weight'] = int(request.form.get("weight"))
            session['height'] = int(request.form.get("height"))
            session['sex'] = request.form.get("sex")
        except:
            pass

        if request.form.get("activity") == Non:
            return render_template("main/purpose.html")
        else:
            # 目標
            activity = request.form.get("activity")


        try:
            db1.execute("INSERT INTO personal_data (user_id, sex, age, weight, height, activity) VALUES (?, ?, ?, ?, ?, ?)", session['user_id'], session['sex'], session['age'], session['weight'], session['heightj'], activity)
        except:
            db1.execute("UPDATE personal_data SET sex=?, age=?, weight=?, height=?, activity=? WHERE user_id=?", session['sex'], session['age'], session['weight'], session['height'], activity, session['user_id'])

        return redirect("/")

    else:
        return render_template("main/input.html")



@app.route("/favorite")
def favorite():
    product_liked_s = db.execute("SELECT product FROM product_liked WHERE user_id = ?", session['user_id'])
    for product_liked in product_liked_s:
        data = db.execute("SELECT * FROM foodnames WEHRE 食品名 = ?", product_liked['product'])
    return render_template("favorite.html", data = data)

