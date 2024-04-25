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
# os.system('pip install --upgrade selenium')

from selenium import webdriver #virtual driver를 연다.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index2.html")

@app.route('/naver')
def naver():
    article_titles = list()
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 15)
        url = "https://news.naver.com/section/100"
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)

        #reservation
        #원하는 페이지 작성할 것
        try:
            xpath_info = "/html/body/div/div[2]/div[2]/div[2]/div[1]/div[2]/a"  # full xpath
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_info))).send_keys(Keys.ENTER)

            xpath_info = "/html/body/div/div[2]/div[2]/div[2]/div[1]/div[1]/ul"  # full xpath
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_info))
            )
            # <ul> Tag들의 리스트
            eles = element.find_elements(By.TAG_NAME, "li")
            for index, ele in enumerate(eles):
                target_ele = ele.find_element(By.TAG_NAME, "strong")
                print(target_ele.text)
                text_format = f">>> Index : [{index}], \nContent is below : \n{target_ele.text}"
                article_titles.append(text_format)
        except Exception as e:
            print("Error")

    return render_template("naver_articles2.html", context = article_titles)

@app.route('/help')
def help():
    return render_template("help2.html")

if __name__ == "__main__" :
    app.run()
