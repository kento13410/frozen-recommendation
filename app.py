from flask import Flask, render_template, request, redirect, session
import ast
from flask_session import Session
from folder.others import login_required, act_calculate, makeRandomList
from werkzeug.security import check_password_hash, generate_password_hash
from flask_paginate import Pagination, get_page_parameter
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('folder.config')
Session(app)

db = SQLAlchemy(app)

# 絶対dbの下に置くように！
from folder.models.sql import user, person, ingredient, food_liked, food

@app.before_first_request
def init():
    db.create_all()


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # sessionの情報を消す
    session.clear()

    if (request.method == "POST"):

        username = request.form.get("username")
        password = request.form.get("password")
        if not username :
            raise Exception('ユーザー名を入力してください')
        if not password :
            raise Exception('パスワードを入力してください')

        rows = user.query.filter(user.name==username).first()
        if (check_password_hash(rows.hash, password)):
            session["user_id"] = rows.hash
            return redirect("/")

    else:
        return render_template("LOGIN/login.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if (request.method=="GET"):
        return render_template("LOGIN/register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username :
            raise Exception('ユーザー名を入力してください。')
        if not password :
            raise Exception('パスワードを入力してください。')
        if not confirmation:
            raise Exception('確認パスワードも入力してください。')

        if password != confirmation:
            raise Exception('パスワードが一致しません。')

        # データの登録
        user_info = user(
            name = username,
            hash = generate_password_hash(password)
        )
        db.session.add(user_info)
        db.session.commit()

        return redirect("/login")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    session.clear()
    return redirect("/")


@app.route("/", methods=["GET","POST"])
@login_required
def home():
    data = food.query.all()
    count = 0
    return render_template("main/home.html", data=data, count=count)


# meal.htmlに戻る
@app.route("/meal_back", methods=["GET","POST"])
@login_required
def meal_back():
    if request.method == 'POST':
        return render_template("main/meal.html")


# 計算
@app.route("/input", methods=["GET","POST"])
@login_required
def index():
    if (request.method == "GET"):
        try:
            session.pop("level", None)
        except:
            pass
        return render_template("main/activeLevel.html")

    else:
        if 'level' not in session:
            session['level'] = request.form.get("level")
            return render_template("main/meal.html")
        else:
            pass

        # 一人当たりの必要摂取カロリー
        data = person.query.filter(person.user_id == session['user_id']).all()[0]
        age = data.age
        weight = data.weight
        height = data.height
        sex = data.sex
        purpose = data.purpose

        act = act_calculate(sex, weight, height, age, session['level'], purpose)

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

        data = food.query.order_by(X-(food.たんぱく質/P + food.脂質/F + food.炭水化物/CBH)).limit(6)

        # 残しておいてください谷口
        # data2 = []
        # for dat in data:
        #     data2_set = []
        #     data2_set.append(dat)
        #     difP2 = difP - dat['タンパク質']
        #     difF2 = difF - dat['脂質']
        #     difCBH2 = difCBH - dat['炭水化物']
        #     X2 = difP2/P + difF2/F + difCBH2/CBH
        #     data_element2 = db.execute("SELECT * FROM foodnames ORDER BY ? - (タンパク質/? + 脂質/? + 炭水化物/?) LIMIT 10", X2, P, F, CBH)
        #     for i in range(len(data_element2)):
        #         data2_set.append(data_element2[i])
        #         data2.append(data2_set)


        return render_template("main/output.html", data = data, difData=difData)


# 入力と合致する食品の栄養情報を取得
@app.route("/search_item", methods=["GET", "POST"])
def search_item():
    if request.method == "GET":
        page = request.args.get(get_page_parameter(), type=int, default=1)
        if page == 1:
            session['breakfasts'] = request.args.getlist("breakfast")
            session['lunchs'] = request.args.getlist("lunch")
            session['snacks'] = request.args.getlist("snack")
        else:
            pass

        sql = "SELECT * FROM 食品成分 WHERE 食品名 like ?"
        brName = []
        luName = []
        snName = []
        for breakfast in session['breakfasts']:
            if len(breakfast) != 0:
                brName += ingredient.query.filter(ingredient.食品名.contains(breakfast)).all()
        for lunch in session['lunchs']:
            if len(lunch) != 0:
                luName += ingredient.query.filter(ingredient.食品名.contains(lunch)).all()
        for snack in session['snacks']:
            if len(snack) != 0:
                snName += ingredient.query.filter(ingredient.食品名.contains(snack)).all()

        b_rows = brName[(page - 1)*5: page*5]
        b_pagination = Pagination(page=page, total=len(brName),  per_page=5, css_framework='bootstrap4')
        b_Max = (- len(brName) // 3) * -1
        l_rows = luName[(page - 1)*5: page*5]
        l_pagination = Pagination(page=page, total=len(luName),  per_page=5, css_framework='bootstrap4')
        l_Max = (- len(luName) // 3) * -1
        s_rows = snName[(page - 1)*5: page*5]
        s_pagination = Pagination(page=page, total=len(snName),  per_page=5, css_framework='bootstrap4')
        s_Max = (- len(snName) // 3) * -1
        return render_template("main/result.html", breakfast=b_rows, lunch=l_rows, snack=s_rows, CurPage=page, b_pagination=b_pagination, b_Max=b_Max, l_pagination=l_pagination, l_Max=l_Max, s_pagination=s_pagination, s_Max=s_Max)


@app.route("/recommend", methods=["GET","POST"])
def recommend():

    if (request.method == "POST"):
        # お弁当肉系
        beef = request.form.get("beef")
        # お弁当魚系
        fish = request.form.get("fish")
        # 米飯系
        rice = request.form.get("rice")
        # 麺系
        noodle = request.form.get("noodle")

        if (beef):
            beefList = food.query.filter(food.カテゴリ=='お弁当肉系').all()
        else:
            beefList = []
        if (fish):
            fishList = food.query.filter(food.カテゴリ=='おべんとう 魚系').all()
        else:
            fishList = []
        if (rice):
            riceList = food.query.filter(food.カテゴリ=='ごはん系').all()
        else:
            riceList = []
        if (noodle):
            noodleList = food.query.filter(food.カテゴリ=='麺系').all()
        else:
            noodleList = []

        #何かしらの条件に従ってこのリストに入れていく
        selectedList = []
        # リストの連結 [{1},{2},.......{n}]となる
        for element in beefList:
            selectedList.append(element)
        for element in fishList:
            selectedList.append(element)
        for element in riceList:
            selectedList.append(element)
        for element in noodleList:
            selectedList.append(element)


        if(len(selectedList) != 0):
            indexList = makeRandomList(len(selectedList))
            recommendList = []
            for index in indexList:
                recommendList.append(selectedList[index])
            return render_template("main/recommend.html",recommendList=recommendList)
        else:
            return redirect("/")
            # print("categoryが一つもチェックされていない")
    else:
        return render_template("main/recommend.html")


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

        if request.form.get("purpose") == None:
            return render_template("main/purpose.html")
        else:
            purpose = request.form.get("purpose")


        try: #dbが格納されていない場合
            data = person(
                sex = session['sex'],
                age = session['age'],
                weight = session['weight'],
                height = session['height'],
                purpose = purpose
            )


        except: #格納されている場合（そのときはtryでエラーでる
            data = person.query.filter(person.user_id == session['user_id']).all()[0]
            data.sex = session['sex']
            data.age = session['age']
            data.weight = session['weight']
            data.height = session['height']
            data.purpose = purpose

        db.session.add(data)
        db.session.commit()

        return redirect("/")

    else:
        return render_template("main/personal_data.html")


@app.route("/favorite",methods=["GET","POST"])
def favorite():
    if(request.method== "GET"):
        liked_s = food_liked.query.filter(food_liked.user_id==session['user_id']).all()
        submitList = []
        for liked in liked_s:
            data = food.query.filter(food.食品名==liked['product']).all()[0]
            submitList.append(data)
        return render_template("main/favorite.html", submitList =submitList)

    else:
        # output画面からデータを受け取って、foodnamesからデータを取ってくる。
        # one~sixまでが毎回異なっていれば最高
        # one~sixの候補(その賞品を表す固有のものがいい。候補：url,id)←商品名も考えたが、ユニークでないものがあった。lx：牛カルビマヨネーズ
        idList = request.form.getlist("id")
        one = 0
        two = 0
        three = 0
        four = 0
        five =0
        six = 0
        if (len(idList) == 1):
            one = idList[0]
            two = False
            three = False
            four = False
            five = False
            six = False

        elif (len(idList) == 2):
            one = idList[0]
            two = idList[1]
            three = False
            four = False
            five = False
            six = False
        elif (len(idList) == 3):
            one = idList[0]
            two = idList[1]
            three = idList[2]
            four = False
            five = False
            six = False
        elif (len(idList) == 4):
            one = idList[0]
            two = idList[1]
            three = idList[2]
            four = idList[3]
            five = False
            six = False
        elif (len(idList) == 5):
            one = idList[0]
            two = idList[1]
            three = idList[2]
            four = idList[3]
            five = idList[4]
            six = False
        else:
            one = idList[0]
            two = idList[1]
            three = idList[2]
            four = idList[3]
            five = idList[4]
            six = idList[5]


        if(one):
            one_name = food.query.filter(food.id==int(one)).all()
        else:
            one_name = [{"食品名":"sample"}]
        if(two):
            two_name = food.query.filter(food.id==int(two)).all()
        else:
            two_name = [{"食品名":"sample"}]
        if(three):
            three_name = food.query.filter(food.id==int(three)).all()
        else:
            three_name = [{"食品名":"sample"}]
        if(four):
            four_name = food.query.filter(food.id==int(four)).all()
        else:
            four_name = [{"食品名":"sample"}]
        if(five):
            five_name = food.query.filter(food.id==int(five)).all()
        else:
            five_name = [{"食品名":"sample"}]
        if(six):
            six_name = food.query.filter(food.id==int(six)).all()
        else:
            six_name = [{"食品名":"sample"}]

        # product_likedにまだ保存されていない商品ならという条件が必要
        identifyList = food_liked.query.filter(food_liked.user_id==session['user_id']).all()
        name_list = [one_name,two_name,three_name,four_name,five_name,six_name]
        add_list = []

        # 初めてお気に入りを使う場合は、全てを登録する。
        if(len(identifyList)==0):
            for name in name_list:
                if (name[0]["食品名"] != "sample"):
                    add_list.append(name[0]["食品名"])
            for name in add_list:
                liked = food_liked(
                    user_id = session['user_id'],
                    product = name
                )
                db.session.add(liked)
                db.session.commit()

        # productLikedに入っている全ての冷凍食品と一致しないなら、一回だけ追加
        else:
            length = len(identifyList)
            for element in name_list:
                for i in range(length):
                    if (element[0]["食品名"] != identifyList[i]["product"] and element[0]["食品名"] != "sample"):
                        if(i == length - 1):
                            add_list.append(element[0]["食品名"])
                    else:
                        break

            if(len(add_list)!= 0):
                for name in add_list:
                    liked = food_liked(
                        user_id = session['user_id'],
                        product = name
                    )
                    db.session.add(liked)
                    db.session.commit()

        # 入力されたデータを取り出してfavorite画面に送る
        # [{"product":},{"product":}..{"product":}]
        product_liked_s = food_liked.query.filter(food.user_id==session['user_id']).all()
        submitList = []
        for product_liked in product_liked_s:
            data = food.query.filter(food.食品名==product_liked['product']).all()[0]
            submitList.append(data)
        return render_template("main/favorite.html", submitList =submitList)


# Delete favorite
@app.route("/delete",methods=["POST"])
def delete():
    name = request.form.get("name")
    food_liked.query.filter(food_liked.product==name, product_liked.user_id==session['user_id']).delete()
    product_liked_s = food_liked.query.filter(food.user_id==session['user_id']).all()
    submitList = []
    for product_liked in product_liked_s:
        data = food.query.filter(food.食品名==product_liked['product']).all()[0]
        submitList.append(data)
    return render_template("main/favorite.html", submitList =submitList)


@app.route("/tutorial")
def video():
    return render_template("main/tutorial.html")
