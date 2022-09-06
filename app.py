from flask import Flask, render_template, request
from cs50 import SQL
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
import re
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager

app = Flask("__name__")


@app.route("/")
def index():
    return render_template("input.html")


@app.route("/search_item")
def search_item():
    option = Options()
    option.add_argument('--headless')

    browser = webdriver.Chrome('ChromeDriverManager().install()')

    try:
        url = 'https://fooddb.mext.go.jp/freeword/fword_top.pl'
        browser.get(url)

        browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))

        keywordBox = browser.find_element_by_class_name('s-text')
        search = browser.find_element_by_name('function1')

        keyword = request.form.get("breakfast")

        keywordBox.send_keys(keyword)
        search.click()

        browser.find_element_by_class_name('result_button').click()

        foods = []
        valueNames = browser.find_elements_by_css_selector('#result_table > tbody > tr')
        for valueName in valueNames:
            items = valueName.find_elements_by_css_selector('td')
            for i in range(len(items)):
                foods.append(items[0].text)

            # print(f'{items[0].text}, エネルギー：{items[2].text}kcal, たんぱく質：{items[4].text}g, 脂質：{items[5].text}g,
            # 炭水化物：{items[6].text}g （100g当たり）')

    finally:
        # プラウザを閉じる
        browser.quit()

    return render_template("input.html", foods=foods)
