from crypt import methods
from flask import Flask, render_template, request
from cs50 import SQL
# from selenium import webdriver
# from time import sleep
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import random

app = Flask("__name__")
db = SQL("sqlite:///foodname.db")

# @app.route("/search_item")
# def search_item():
#     breakfast = request.form.get("breakfast")
#     lunch = request.form.get("lunch")
#     snack = request.form.get("snack")
#     brName = db.execute("SELECT 食品名 FROM 食品成分 WHERE 食品名 like %?%", breakfast)
#     luName = db.execute("SELECT 食品名 FROM 食品成分 WHERE 食品名 like %?%", lunch)
#     snName = db.execute("SELECT 食品名 FROM 食品成分 WHERE 食品名 like %?%", snack)
#     return render_template("select.html", breakfast=brName, lunch=luName, snack=snName)
#     food_energy = db.execute("SELECT エネルギー FROM 食品成分 WHERE 食品名 like %?% OR 食品名 like %?% OR 食品名 like %?%", breakfast, lunch, snack)


# @app.route("/recommend")
# def recommend():
#     foods = []
#     categorys = db.execute("SELECT category FROM category WHERE user_id = ? AND is_liked = TRUE", session['user_id'])
#     for category in categorys:
#         foods += db.execute("SELECT food FROM foods WHERE category = ?", category['category'])
#     foodsRecommend = random.sample(foods, 3)
#     return render_template("recommend.html", foods = foodsRecommend)


@app.route("/", methods=["GET","POST"])
def index():
    if (request.method == "GET"):
        return render_template("input.html")
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

        # return render_template("test.html", D=D)
        data = db.execute("SELECT * FROM foodnames WHERE カロリー < ?", D)

        return render_template("output.html", data = data)

@app.route("/home",methods=["GET","POST"])
def home():
    if (request.method == "GET"):
        return render_template("home.html")
    else:
        pass
    


# @app.route("/search_item")
# def search_item():
#     options = Options()
#     options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
#     options.add_argument('--headless')

#     browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#     try:
#         url = 'https://fooddb.mext.go.jp/freeword/fword_top.pl'
#         browser.get(url)

#         browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

#         keywordBox = browser.find_element_by_class_name('s-text')
#         search = browser.find_element_by_name('function1')

#         keyword = request.form.get("breakfast")

#         keywordBox.send_keys(keyword)
#         search.click()

#         browser.find_element_by_class_name('result_button').click()

#         foods = []
#         valueNames = browser.find_elements_by_css_selector('#result_table > tbody > tr')
#         for valueName in valueNames:
#             items = valueName.find_elements_by_css_selector('td')
#             for i in range(len(items)):
#                 foods.append(items[0].text)

#             # print(f'{items[0].text}, エネルギー：{items[2].text}kcal, たんぱく質：{items[4].text}g, 脂質：{items[5].text}g,
#             # 炭水化物：{items[6].text}g （100g当たり）')

#     finally:
#         # プラウザを閉じる
#         browser.quit()

#     return render_template("input.html", foods=foods)
