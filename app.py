from flask import Flask, render_template, request
from cs50 import SQL

app = Flask("__name__")
db = SQL("sqlite:///foodname.db")

# ---------------------------------------input route start----------------------------------------
@app.route("/",methods=["GET","POST"])
def index():
    if (request.method == "GET"):
        return render_template("input.html")
    else:
        # 一人当たりの必要摂取カロリー
        age = request.method("age")
        intAge = int(age)
        weight = request.method("weight")
        intWeight = int(weight)
        height = request.method("height")
        intHeight = int(height)
        budget = request.method("budget")
        intBudget = int(budget)
        # 性別
        sex = request.method("sex")
        # 活動レベル
        level = request.method("level")
        # 目的
        activity = request.method("activity")

    #とりあえず、仮で決める。
        # 朝で摂取したエネルギー + 昼で摂取したエネルギー
        # 男性:1800 (kcal)
        # 女性:1350 (kcal)


# --------------------------------------------------------------------
# 一人当たりの必要摂取カロリー
# act = b * o * g [kcal]
# --------------------------------------------------------------------
        # 基礎代謝(B)の計算
            # 男性： 10×体重kg＋6.25×身長cmー5×年齢＋5
            # 女性： 10×体重kg+6.25×身長cmー５×年齢-16
        b = 0
        # 「活動量を入れた代謝量」を求めるために掛ける値
        oDict = {"one":1.2,"two":1.55,"three":1.725}
        # G(食事の目的)
        gDict ={"増量":1.2,"現状維持":1.0,"減量":0.8}
        # bo: b * o　のこと
        bo = 0

        if (sex == "男"):
            b = 10 * intWeight + 6.25 * intHeight - 5 * intAge + 5
            # boを計算する
            if (level == "one"):
                bo = b * oDict["one"]
            elif (level == "two"):
                bo = b * oDict["two"]
            elif (level == "three"):
                bo = b * oDict["three"]
            # actを計算する。
            if (activity == "増量"):
                act = bo * gDict["増量"]
            elif (activity == "現状維持"):
                act = bo * gDict["現状維持"]
            elif (activity == "減量"):
                act = bo * gDict["減量"]


        if (sex == "女"):
            b = 10 * intWeight + 6.25 * intHeight - 5 * intAge - 16
            # boを計算する
            if (level == "one"):
                bo = b * oDict["one"]
            elif (level == "two"):
                bo = b * oDict["two"]
            elif (level == "three"):
                bo = b * oDict["three"]
            # actを計算する。
            if (activity == "増量"):
                act = bo * gDict["増量"]
            elif (activity == "現状維持"):
                act = bo * gDict["現状維持"]
            elif (activity == "減量"):
                act = bo * gDict["減量"]

#---------------------------------------------------------------------


# --------------------------------------------------------------------
# D = act - (朝で摂取したエネルギー + 昼で摂取したエネルギー) [kcal]
# --------------------------------------------------------------------

    #とりあえず、仮で決める。
    # 朝で摂取したエネルギー + 昼で摂取したエネルギー
        # 男性:1800 (kcal)
        # 女性:1350 (kcal)
        D = 0
        if (sex == "男"):
            D = act - 1800

        elif (sex == "女"):
            D = act - 1350

# --------------------------------------------------------------------
        return render_template("output.html")





























