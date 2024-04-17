# 이미지 처리를 위한 라이브러리 설치
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains

def extract_features(image_path):
    # 이미지에서 특징 추출 (여기서는 단순화된 예시로, 실제로는 더 복잡한 로직이 필요)
    img = cv2.imread(image_path, 0)  # 이미지를 그레이스케일로 로드
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(img, None)
    return descriptors

def search_similar_products(features):
    print("크롤링 시작")
    driver = webdriver.Chrome()
    # Danawa.com에서 제품 검색 (실제 코드는 다를 수 있음)
    driver.get('https://www.danawa.com/')
    time.sleep(2)

    # 검색 신규 문법
    # find_element(By.ID, 'id명')
    # find_element(By.XPATH, '경로')
    # find_element(By.NAME, '이름')
    # find_element(By.TAG_NAME, '태그 이름')
    # find_element(By.CLASS_NAME, '클래스 이름')
    # find_element(By.LINK_TEXT, '링크 문자')
    # find_element(By.CSS_SELECTOR, 'css 선택자')

    search_box = driver.find_element(By.NAME, "k1")  # 검색창의 HTML name 속성에 따라 다름
    search_box.send_keys('멀티탭')  # 검색어 입력
    search_box.send_keys(Keys.RETURN)

    # click the item
    action = ActionChains(driver)
    action.click(on_element=search_box)
    time.sleep(2)  # 페이지 로딩 대기

    # 검색 결과 처리 로직 (여기서는 단순화됨)
    # ...
    html1 = ""
    html1 = html1 + driver.page_source

    ######################## 파일 저장
    title_file = open("product.html", 'w', encoding='UTF8')
    title_file.write(html1)
    title_file.close()
    driver.quit()


# 실제 사용 예
image_path = 'multitap.jpg'
features = extract_features(image_path)
print(features)
search_similar_products(features)
