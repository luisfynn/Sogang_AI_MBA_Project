from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from selenium.webdriver.chrome.options import Options

# 이미지 처리를 위한 라이브러리 설치
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

# Flask 앱 설정
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 이미지 업로드 및 처리를 위한 페이지
# upload.html, result.html파일은 templates 폴더안에 위치해야 한다.
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 파일이 존재하는지 확인
        if 'file' not in request.files:
            print("file not in request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # 이미지에서 특징 추출 및 유사 제품 검색 로직
            features = extract_features(filepath)
            results = search_similar_products(features)
            # 결과 페이지로 이동
            return render_template('result.html', results=results)
    return render_template('upload.html')

# 클롤링
def extract_features(image_path):
    # 이미지에서 특징 추출 (여기서는 단순화된 예시로, 실제로는 더 복잡한 로직이 필요)
    img = cv2.imread(image_path, 0)  # 이미지를 그레이스케일로 로드
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return descriptors

def search_similar_products(features):
    # Chrome WebDriver 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.danawa.com/')

    # 검색어 설정 - 예제에서는 "멀티탭"을 검색어로 사용
    search_query = '멀티탭'

    # 이미지 검색 접속
    search_box = driver.find_element(By.NAME, "k1")  # 검색창의 HTML name 속성에 따라 다름
    search_box.send_keys('멀티탭')  # 검색어 입력
    search_box.send_keys(Keys.RETURN)

    # 결과 로딩 대기
    time.sleep(2)  # 실제 환경에서는 더 정교한 대기 로직을 구현할 필요가 있음

    # 검색 결과에서 이미지 URL과 링크 추출
    results = []
    # images = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
    # links = driver.find_elements_by_css_selector('a.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')
    #
    # for img, link in zip(images, links)[:4]:  # 상위 4개 결과만 처리
    #     src = img.get_attribute('src')
    #     href = link.get_attribute('href')
    #     results.append({"image": src, "url": href})
    results.append({"image": "multitap.jpg", "url": 'https://www.danawa.com/'})
    driver.quit()
    return results

if __name__ == '__main__':
    app.run(debug=True)
