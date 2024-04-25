import os
# os.system('pip install --upgrade selenium')

from selenium import webdriver #virtual driver를 연다.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from flask import Flask, render_template, request

app = Flask(__name__)

#Test Data in DB
users = {
    'mk':'1234',
    'mj':'5678'
}

@app.route('/')
def index():
    # return render_template("index.html")
    return render_template("bootstrapIndex.html")

@app.route('/naver')
def naver():
    article_titles = list()
    with webdriver.Chrome() as driver:
        wait = WebDriverWait(driver, 15)
        url = "https://news.naver.com/section/100"
        driver.get(url)

        try:
            xpath_info = "/html/body/div/header/div/div[2]/div/div/ul/li[2]/a/span"  # full xpath
            wait.until(EC.visibility_of_element_located((By.XPATH, xpath_info))).send_keys(Keys.ENTER)
            xpath_info = "/html/body/div/div[2]/div[2]/div[2]"  # full xpath
            element = WebDriverWait(driver, 5).until(
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
    return render_template("naver_articles.html", context = article_titles)

@app.route('/login')
def login():
    return render_template("login.html")


# e.g http://127.0.0.1:5000/handle_get?username=mk&password=1234
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')

@app.route('/help')
def help():
    return render_template("help.html")

if __name__ == "__main__" :
    app.run()
