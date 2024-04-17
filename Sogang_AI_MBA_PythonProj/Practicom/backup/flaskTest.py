from flask import Flask, render_template, request, redirect, render_template_string
from werkzeug.utils import secure_filename
from selenium.webdriver.chrome.options import Options
import subprocess
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re

# Flask 앱 설정
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# 이미지 업로드 및 처리를 위한 페이지
# upload.html은 templates 폴더안에 위치해야 한다.
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
            filename = secure_filename(file.filename) #보안처리
            image_path = filename
            print("image_path:", image_path)
            file.save(image_path)
            command = [
                'python',
                'yolov9-main/detect.py',
                '--weights', 'yolov9-main/yolov9-e-converted.pt',
                '--imgsz', '640',  # 올바른 옵션은 --imgsz 입니다.
                '--conf-thres', '0.25',
                '--source', image_path,
                '--save-txt'
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            print("type_result:", type(result))
            print("dir_result:", dir(result))
            print("return code_result:", result.__str__())

            # stderr에서 경로 추출
            pattern = re.compile(r"labels saved to (.+?)\n")

            # 이제 result.stderr에 있는 문자열에서 경로를 추출
            match = pattern.search(result.stderr)
            if match:
                save_directory = match.group(1)
                print(f"Labels are saved in: {save_directory}")

            image_path = image_path[:-3]
            image_path = image_path +"txt"

            f = open(save_directory +"\\"+ image_path, 'r')
            line = f.readline()
            print(line)
            f.close()

            print("search_query is", line[0:2])

            # 인덱스 변환(추후 작업 필요)
            if line[0:2] == '67':
                search_query = "멀티탭"
            else:
                search_query = "usb 허브"

            # 유사 제품 검색 로직 (여기서는 예시로 HTML 코드 추출)
            html_code = search_and_extract_html(search_query)

            # 결과 페이지로 이동 (실제로는 html_code를 처리하여 결과를 표시해야 함)
            # return render_template('result.html', html_code=html_code)
            return render_template_string(html_code)

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
    chrome_options = Options()
    # 크롤링을 숨기려면 하기 코드 활성화
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # chrome_options.add_argument("--disable-gpu")  # Applicable for windows os only
    # chrome_options.add_argument("--disable-software-rasterizer")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.danawa.com')

    # 검색어 설정 - 예제에서는 "멀티탭"을 검색어로 사용
    query = search_query

    # 이미지 검색 접속
    search_box = driver.find_element(By.NAME, "k1")  #검색창 html의 name이 'q'여서 q다 # 검색창의 HTML name 속성에 따라 다름
    search_box.send_keys(query)  # 검색어 입력
    search_box.send_keys(Keys.RETURN)

    html_code = driver.page_source
    driver.quit()
    return html_code

# server startup
# Once the server starts up, it goes into a loop that waits for requests and services them.
# This loop continues until the application is stopped, for example by hitting Ctrl-C.
if __name__ == '__main__':
    app.run(debug=True)
