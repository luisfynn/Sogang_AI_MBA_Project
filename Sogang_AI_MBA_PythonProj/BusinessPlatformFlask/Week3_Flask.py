########<1>########
# from flask import Flask
# from flask import render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# def hello():
#     print(__name__)
#     # return "Hello world!"
#     return render_template('index.html')
#
# @app.route('/info')
# def info():
#     return render_template('info.html')
#
# if __name__ == "__main__":
#     app.run()

########<2>########
import os
os.system('pip install --upgrade selenium')

from selenium import webdriver #virtual driver를 연다.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/naver')
def naver():
    article_titles = list()
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 15)
        url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
        driver.get(url)

    #reservation

    return render_template("naver_articles.html", context = article_titles)

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__" :
    app.run()
