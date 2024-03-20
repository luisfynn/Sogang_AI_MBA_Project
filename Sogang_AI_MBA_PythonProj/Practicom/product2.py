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
        if 'file' not in request.files:
            print("File not in request")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # YOLOv9를 사용하여 이미지에서 객체 감지
            labels = run_detection(filepath)
            
            #원본코드 if~else문
            # if labels:
            #     # 첫 번째 감지된 객체의 라벨을 검색어로 사용
            #     search_query = labels[0][0] #라벨 작업이 필요
            #     print("search_query is", search_query)
            #     # 유사 제품 검색 로직 (여기서는 예시로 HTML 코드 추출)
            #     html_code = search_and_extract_html(search_query)
            #     # 결과 페이지로 이동 (실제로는 html_code를 처리하여 결과를 표시해야 함)
            #     return render_template('result.html', html_code=html_code)
            # else:
            #     print("labels", labels)
            #     return "No objects detected."
            
            # 데모용 임시코드 작성
            search_query = "멀티탭"
            print("search_query is", search_query)
            # 유사 제품 검색 로직 (여기서는 예시로 HTML 코드 추출)
            html_code = search_and_extract_html(search_query)
            # 결과 페이지로 이동 (실제로는 html_code를 처리하여 결과를 표시해야 함)
            return render_template('result.html', html_code=html_code)

    return render_template('upload.html')

# 클롤링
def extract_features(image_path):
    # 이미지에서 특징 추출 (여기서는 단순화된 예시로, 실제로는 더 복잡한 로직이 필요)
    img = cv2.imread(image_path, 0)  # 이미지를 그레이스케일로 로드
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return descriptors

# Selenium을 이용한 웹 검색 및 HTML 코드 추출
def search_and_extract_html(search_query):
    print('search_and_extract_html에서 입력받은 search_query:', search_query)
    # Chrome WebDriver 설정
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.danawa.com/')
    # driver.get(f'https://www.google.com/search?q={search_query}')

    # 검색어 설정 - 예제에서는 "멀티탭"을 검색어로 사용
    query = search_query

    # 이미지 검색 접속
    search_box = driver.find_element(By.NAME, "k1")  # 검색창의 HTML name 속성에 따라 다름
    search_box.send_keys(query)  # 검색어 입력
    search_box.send_keys(Keys.RETURN)

    html_code = driver.page_source
    print(html_code)
    render_template('result.html', html_code=html_code)
    driver.quit()
    return html_code

# def search_similar_products(features):
#     # Chrome WebDriver 설정
#     chrome_options = Options()
#     # chrome_options.add_argument("--headless")  # 브라우저 창을 띄우지 않는 옵션
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get('https://www.danawa.com/')
#
#     # 검색어 설정 - 예제에서는 "멀티탭"을 검색어로 사용
#     search_query = 'usb'
#
#     # 이미지 검색 접속
#     search_box = driver.find_element(By.NAME, "k1")  # 검색창의 HTML name 속성에 따라 다름
#     search_box.send_keys('멀티탭')  # 검색어 입력
#     search_box.send_keys(Keys.RETURN)
#
#     html_code = driver.page_source
#
#     # 결과 로딩 대기
#     # time.sleep(2)  # 실제 환경에서는 더 정교한 대기 로직을 구현할 필요가 있음
#
#     # 검색 결과에서 이미지 URL과 링크 추출
#     # results = []
#     # images = driver.find_elements_by_css_selector('img.rg_i.Q4LuWd')
#     # links = driver.find_elements_by_css_selector('a.VFACy.kGQAp.sMi44c.lNHeqe.WGvvNb')
#
#     # for img, link in zip(images, links)[:4]:  # 상위 4개 결과만 처리
#     #     src = img.get_attribute('src')
#     #     href = link.get_attribute('href')
#     #     results.append({"image": src, "url": href})
#     # results.append({"image": "multitap.jpg", "url": 'https://www.danawa.com/'})
#
#     render_template('result.html', html_code=html_code)
#     driver.quit()
#     return html_code

import subprocess
import json

# YOLOv9 detect.py 스크립트 실행 및 결과 파싱
def run_detection(image_path):
    cmd = [
        'python', 'yolov9-main/detect.py',
        '--source', image_path,
        '--img', '640',
        '--device', '0',
        '--weights', 'yolov9-main/yolov9-e-converted.pt',
        '--name', 'yolov9_c_c_640_detect',
        '--save-txt',  # 결과를 txt 파일로 저장
        '--save-conf',  # 감지된 객체의 확률을 저장
        '--exist-ok',  # 이전 결과를 덮어쓰기
    ]
    subprocess.run(cmd, check=True)
    # 결과 파일 경로 생성 (detect.py의 출력 규칙에 따름)
    result_path = f'yolov9-main/yolov9_c_c_640_detect/labels/{image_path.split("/")[-1].replace(".jpg", ".txt")}'
    return parse_detection_result(result_path)

# 결과 파일 파싱
def parse_detection_result(result_path):
    labels = []
    try:
        with open(result_path, 'r') as file:
            for line in file.readlines():
                class_id, *_, conf = line.split()
                labels.append((class_id, conf))
    except FileNotFoundError:
        print("결과 파일을 찾을 수 없습니다.")
    return labels

from selenium import webdriver

if __name__ == '__main__':
    app.run(debug=True)
