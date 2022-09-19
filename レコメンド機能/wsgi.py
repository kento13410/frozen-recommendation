# from cs50 import SQL
# from fivelist import makeRandomList

# db = SQL("sqlite:///foodname.db")
# #　おべんとう 魚系
# beef = False
# # お弁当魚系
# fish = "おべんとう 魚系"
# # 米飯系
# rice = False
# # 麺系
# noodle = False

# if (beef):
#     beefList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",beef)
# else:
#     beefList = []
# if (fish):
#     fishList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",fish)
# else:
#     fishList = []
# if (rice):
#     riceList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",rice)
# else:
#     riceList = []
# if (noodle):
#     noodleList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",noodle)
# else:
#      noodleList = []


# #何かしらの条件に従ってこのリストに入れていく
# selectedList = []
# # リストの連結 [{1},{2},.......{n}]となる
# for element in beefList:
#     selectedList.append(element)
# for element in fishList:
#     selectedList.append(element)
# for element in riceList:
#     selectedList.append(element)
# for element in noodleList:
#     selectedList.append(element)

# print(len(selectedList))

# if(len(selectedList) != 0):
#     indexList = makeRandomList(len(selectedList))
#     recommendList = []
#     for index in indexList:
#         recommendList.append(selectedList[index])
#     # 綺麗に表示する
#     for dict in recommendList:
#         print("---------------------------------------------------------------------------------------------------------------------------")
#         print(dict)
#         print("---------------------------------------------------------------------------------------------------------------------------")
# else:
#     print("categoryが一つもチェックされていない")


# -------------------------------------------------------------------------------------

from flask import Flask, render_template, request,redirect
from cs50 import SQL
from fivelist import makeRandomList

db = SQL("sqlite:///foodname.db")
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def test():
    return render_template("test.html")


@app.route("/recommend", methods=["GET","POST"])
def recommend():
    if (request.method == "POST"):
        beef = request.form.get("beef")
        # お弁当魚系
        fish = request.form.get("fish")
        # 米飯系
        rice = request.form.get("rice")
        # 麺系
        noodle = request.form.get("noodle")

        if (beef):
            beefList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",beef)
        else:
            beefList = []
        if (fish):
            # fishList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",fish)
            fishList = db.execute('SELECT * from foodnames WHERE カテゴリ = "おべんとう 魚系" ')
        else:
            fishList = []
        if (rice):
            riceList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",rice)
        else:
            riceList = []
        if (noodle):
            noodleList = db.execute("SELECT * from foodnames WHERE カテゴリ = ?",noodle)
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
            return render_template("recommend.html",recommendList=recommendList)
        else:
            return redirect("/")
            # print("categoryが一つもチェックされていない")


