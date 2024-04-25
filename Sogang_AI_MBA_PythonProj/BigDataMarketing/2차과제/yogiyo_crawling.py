import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import csv
import os

# CITY_KEYWORD =   ['성북구 돈암1동', '성북구 돈암2동', '성북구 안암동', '성북구 보문동', '성북구 정릉1동', '성북구 정릉2동', '성북구 정릉3동', '성북구 정릉4동', '성북구 길음1동', '성북구 길음2동', '성북구 월곡1동', '성북구 월곡2동', '성북구 장위1동', '성북구 장위2동', '성북구 장위3동', '성북구 성북동', '성북구 삼선동', '성북구 동선동', '성북구 종암동', '성북구 석관동']
# 강남구: ['강남구 신사동', '강남구 개포3동', '강남구 논현1동', '강남구 논현2동', '강남구 삼성1동', '강남구 삼성2동', '강남구 대치1동', '강남구 대치2동', '강남구 대치4동', '강남구 역삼1동', '강남구 역삼2동', '강남구 도곡1동', '강남구 도곡2동', '강남구 개포1동', '강남구 개포2동', '강남구 개포4동', '강남구 일원본동', '강남구 일원1동', '강남구 수서동', '강남구 세곡동', '강남구 압구정동', '강남구 청담동']
# 강동구: ['강동구 명일1동', '강동구 명일2동', '강동구 고덕1동', '강동구 고덕2동', '강동구 암사1동', '강동구 암사2동', '강동구 암사3동', '강동구 천호1동', '강동구 천호2동', '강동구 천호3동', '강동구 성내1동', '강동구 성내2동', '강동구 성내3동', '강동구 길동', '강동구 둔촌1동', '강동구 둔촌2동', '강동구 강일동', '강동구 상일1동', '강동구 상일2동']
# 강북구: ['강북구 번1동', '강북구 번2동', '강북구 번3동', '강북구 수유1동', '강북구 수유2동', '강북구 수유3동', '강북구 삼양동', '강북구 미아동', '강북구 송중동', '강북구 송천동', '강북구 삼각산동', '강북구 우이동', '강북구 인수동']
# 강서구: ['강서구 염창동', '강서구 등촌1동', '강서구 등촌2동', '강서구 등촌3동', '강서구 화곡본동', '강서구 화곡2동', '강서구 화곡3동', '강서구 화곡4동', '강서구 화곡6동', '강서구 화곡8동', '강서구 가양1동', '강서구 가양2동', '강서구 가양3동', '강서구 발산1동', '강서구 공항동', '강서구 방화1동', '강서구 방화2동', '강서구 방화3동', '강서구 화곡1동', '강서구 우장산동']
# 관악구: ['관악구 보라매동', '관악구 청림동', '관악구 행운동', '관악구 낙성대동', '관악구 중앙동', '관악구 인헌동', '관악구 남현동', '관악구 서원동', '관악구 신원동', '관악구 서림동', '관악구 신사동', '관악구 신림동', '관악구 난향동', '관악구 조원동', '관악구 대학동', '관악구 은천동', '관악구 성현동', '관악구 청룡동', '관악구 난곡동', '관악구 삼성동', '관악구 미성동']
# 광진구: ['광진구 화양동', '광진구 군자동', '광진구 중곡1동', '광진구 중곡2동', '광진구 중곡3동', '광진구 중곡4동', '광진구 능동', '광진구 구의1동', '광진구 구의2동', '광진구 구의3동', '광진구 광장동', '광진구 자양1동', '광진구 자양2동', '광진구 자양3동', '광진구 자양4동']
# 구로구: ['구로구 신도림동', '구로구 구로1동', '구로구 구로2동', '구로구 구로3동', '구로구 구로4동', '구로구 구로5동', '구로구 고척1동', '구로구 고척2동', '구로구 개봉2동', '구로구 개봉3동', '구로구 오류1동', '구로구 오류2동', '구로구 수궁동', '구로구 가리봉동', '구로구 개봉1동', '구로구 항동']
# 금천구: ['금천구 가산동', '금천구 독산1동', '금천구 독산2동', '금천구 독산3동', '금천구 독산4동', '금천구 시흥1동', '금천구 시흥2동', '금천구 시흥3동', '금천구 시흥4동', '금천구 시흥5동']
# 노원구: ['노원구 월계1동', '노원구 월계2동', '노원구 월계3동', '노원구 공릉2동', '노원구 하계1동', '노원구 하계2동', '노원구 중계본동', '노원구 중계1동', '노원구 중계4동', '노원구 상계1동', '노원구 상계2동', '노원구 상계5동', '노원구 상계8동', '노원구 상계9동', '노원구 상계10동', '노원구 상계3.4동', '노원구 상계6.7동', '노원구 중계2.3동', '노원구 공릉1동']
# 도봉구: ['도봉구 쌍문1동', '도봉구 쌍문2동', '도봉구 쌍문3동', '도봉구 쌍문4동', '도봉구 방학1동', '도봉구 방학2동', '도봉구 방학3동', '도봉구 창1동', '도봉구 창2동', '도봉구 창3동', '도봉구 창4동', '도봉구 창5동', '도봉구 도봉1동', '도봉구 도봉2동']
# 동대문구: ['동대문구 회기동', '동대문구 휘경1동', '동대문구 휘경2동', '동대문구 청량리동', '동대문구 용신동', '동대문구 제기동', '동대문구 전농1동', '동대문구 전농2동', '동대문구 답십리1동', '동대문구 답십리2동', '동대문구 장안1동', '동대문구 장안2동', '동대문구 이문1동', '동대문구 이문2동']
# 동작구: ['동작구 노량진2동', '동작구 상도1동', '동작구 상도2동', '동작구 상도3동', '동작구 상도4동', '동작구 사당1동', '동작구 사당3동', '동작구 사당4동', '동작구 사당5동', '동작구 대방동', '동작구 신대방1동', '동작구 신대방2동', '동작구 흑석동', '동작구 노량진1동', '동작구 사당2동']
# 마포구: ['마포구 용강동', '마포구 대흥동', '마포구 염리동', '마포구 신수동', '마포구 서교동', '마포구 합정동', '마포구 망원1동', '마포구 망원2동', '마포구 연남동', '마포구 성산1동', '마포구 성산2동', '마포구 상암동', '마포구 도화동', '마포구 서강동', '마포구 공덕동', '마포구 아현동']
# 서대문구: ['서대문구 천연동', '서대문구 홍제1동', '서대문구 홍제2동', '서대문구 홍제3동', '서대문구 홍은1동', '서대문구 홍은2동', '서대문구 남가좌1동', '서대문구 남가좌2동', '서대문구 북가좌1동', '서대문구 북가좌2동', '서대문구 충현동', '서대문구 북아현동', '서대문구 신촌동', '서대문구 연희동']
# 서초구: ['서초구 서초1동', '서초구 서초2동', '서초구 서초3동', '서초구 서초4동', '서초구 잠원동', '서초구 반포본동', '서초구 반포1동', '서초구 반포2동', '서초구 반포3동', '서초구 반포4동', '서초구 방배본동', '서초구 방배1동', '서초구 방배2동', '서초구 방배3동', '서초구 방배4동', '서초구 양재1동', '서초구 양재2동', '서초구 내곡동']
# 성동구: ['성동구 왕십리2동', '성동구 마장동', '성동구 사근동', '성동구 행당1동', '성동구 행당2동', '성동구 응봉동', '성동구 금호1가동', '성동구 금호4가동', '성동구 성수1가1동', '성동구 성수1가2동', '성동구 성수2가1동', '성동구 성수2가3동', '성동구 송정동', '성동구 용답동', '성동구 왕십리도선동', '성동구 금호2.3가동', '성동구 옥수동']
# 성북구: ['성북구 돈암1동', '성북구 돈암2동', '성북구 안암동', '성북구 보문동', '성북구 정릉1동', '성북구 정릉2동', '성북구 정릉3동', '성북구 정릉4동', '성북구 길음1동', '성북구 길음2동', '성북구 월곡1동', '성북구 월곡2동', '성북구 장위1동', '성북구 장위2동', '성북구 장위3동', '성북구 성북동', '성북구 삼선동', '성북구 동선동', '성북구 종암동', '성북구 석관동']
# 송파구: ['송파구 풍납1동', '송파구 풍납2동', '송파구 거여1동', '송파구 거여2동', '송파구 마천1동', '송파구 마천2동', '송파구 방이1동', '송파구 방이2동', '송파구 오륜동', '송파구 오금동', '송파구 송파1동', '송파구 송파2동', '송파구 석촌동', '송파구 삼전동', '송파구 가락본동', '송파구 가락1동', '송파구 가락2동', '송파구 문정1동', '송파구 문정2동', '송파구 장지동', '송파구 위례동', '송파구 잠실본동', '송파구 잠실2동', '송파구 잠실3동', '송파구 잠실4동', '송파구 잠실6동', '송파구 잠실7동']
# 양천구: ['양천구 목1동', '양천구 목2동', '양천구 목3동', '양천구 목4동', '양천구 목5동', '양천구 신월1동', '양천구 신월2동', '양천구 신월3동', '양천구 신월4동', '양천구 신월5동', '양천구 신월6동', '양천구 신월7동', '양천구 신정1동', '양천구 신정2동', '양천구 신정4동', '양천구 신정3동', '양천구 신정6동', '양천구 신정7동']
# 영등포구: ['영등포구 여의동', '영등포구 당산1동', '영등포구 당산2동', '영등포구 양평1동', '영등포구 양평2동', '영등포구 신길1동', '영등포구 신길3동', '영등포구 신길4동', '영등포구 신길5동', '영등포구 신길6동', '영등포구 신길7동', '영등포구 대림1동', '영등포구 대림2동', '영등포구 대림3동', '영등포구 영등포본동', '영등포구 영등포동', '영등포구 도림동', '영등포구 문래동']
# 용산구: ['용산구 후암동', '용산구 용산2가동', '용산구 남영동', '용산구 원효로2동', '용산구 효창동', '용산구 용문동', '용산구 이촌1동', '용산구 이촌2동', '용산구 이태원1동', '용산구 이태원2동', '용산구 서빙고동', '용산구 보광동', '용산구 청파동', '용산구 원효로1동', '용산구 한강로동', '용산구 한남동']
# 은평구: ['은평구 녹번동', '은평구 불광1동', '은평구 갈현1동', '은평구 갈현2동', '은평구 구산동', '은평구 대조동', '은평구 응암1동', '은평구 응암2동', '은평구 신사1동', '은평구 신사2동', '은평구 증산동', '은평구 수색동', '은평구 진관동', '은평구 불광2동', '은평구 응암3동', '은평구 역촌동']
# 종로구: ['종로구 사직동', '종로구 삼청동', '종로구 부암동', '종로구 평창동', '종로구 무악동', '종로구 교남동', '종로구 가회동', '종로구 종로1.2.3.4가동', '종로구 종로5.6가동', '종로구 이화동', '종로구 혜화동', '종로구 창신1동', '종로구 창신2동', '종로구 창신3동', '종로구 숭인1동', '종로구 숭인2동', '종로구 청운효자동']
# 중구: ['중구 소공동', '중구 회현동', '중구 명동', '중구 필동', '중구 장충동', '중구 광희동', '중구 을지로동', '중구 신당5동', '중구 황학동', '중구 중림동', '중구 신당동', '중구 다산동', '중구 약수동', '중구 청구동', '중구 동화동']
# 중랑구: ['중랑구 면목2동', '중랑구 면목4동', '중랑구 면목5동', '중랑구 면목7동', '중랑구 상봉1동', '중랑구 상봉2동', '중랑구 중화1동', '중랑구 중화2동', '중랑구 묵1동', '중랑구 묵2동', '중랑구 망우3동', '중랑구 신내1동', '중랑구 신내2동', '중랑구 면목본동', '중랑구 면목3.8동', '중랑구 망우본동']

BRAND_KEYWORD = '굽네' #굽네, BHC, 60계
METHOD = 'crawling_parse' #'crawling_parse' or 'parse'

# PATH = "C:\\Users\\luisf\\OneDrive\\바탕 화면\\WorkSpace\\Sogang_AI_MBA_Project\\Sogang_AI_MBA_PythonProj\\BigDataMarketing\\2차과제\\"
PATH ="C:\\Users\\medit\\Desktop\\WorkSpace\\pythonProject\\BigDataMarketing\\"
TIME_DELAY = 1

def initialize_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)

# 페이지 최상단으로 스크롤 올리기
def scroll_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")

# 페이지 최하단으로 스크롤 내리기
def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(TIME_DELAY)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def go_page(driver, region):
    # 크롤링 페이지 열기
    driver.get("https://www.yogiyo.co.kr/mobile/#")
    # driver.maximize_window()
    driver.set_window_size(1920, 1080)
    time.sleep(TIME_DELAY)
    
    # 지역 검색창이 로드될 때까지 대기
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search"]/div/form/input')))
    search_input.clear()
    search_input.send_keys(region)
    time.sleep(TIME_DELAY)

    # 검색 버튼 클릭
    search_button = driver.find_element(By.XPATH, '//*[@id="button_search_address"]/button[2]')
    search_button.click()
    time.sleep(TIME_DELAY)

    # 주소 검색 결과 클릭 대기
    search_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a')))
    search_result.click()
    time.sleep(TIME_DELAY)

    # 첫 번째 카테고리 항목 클릭
    first_list_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]/ul/li[1]')))
    first_list_item.click()
    time.sleep(TIME_DELAY)

    # 검색 입력란에 BRAND_KEYWORD 입력
    search_input = driver.find_element(By.NAME, 'category_keyword')
    search_input.clear()
    search_input.send_keys(BRAND_KEYWORD)
    time.sleep(TIME_DELAY)

    # 검색 버튼 찾기 및 클릭
    search_button = driver.find_element(By.ID, 'category_search_button')
    search_button.click()
    time.sleep(TIME_DELAY)


def get_info(driver):
    scroll_down(driver)
    try:
        # 레스토랑 요소 모두 찾기
        stores = driver.find_elements(By.CLASS_NAME, 'col-sm-6')
        restaurant_names = []

        # 각 레스토랑 이름 추출
        for store in stores:
            try:
                # 현재 store 요소 내에서 레스토랑 이름을 찾음
                restaurant_name_element = store.find_element(By.CSS_SELECTOR, 'div.restaurant-name.ng-binding')
                restaurant_name = restaurant_name_element.get_attribute('innerText')
                # print("Restaurant Name:", restaurant_name)
                restaurant_names.append(restaurant_name)
            except Exception as e:
                print("Error finding restaurant name in store:", e)

    finally:
        print("Restaurant Names:", restaurant_names)

    filtered_restaurants = [name for name in restaurant_names if BRAND_KEYWORD in name]
    print("Restaurant Names:", filtered_restaurants)
    return filtered_restaurants

def save_html(driver, filename="page.html"):
    #현재 페이지의 HTML을 파일로 저장
    with open(filename, 'w', encoding='utf-8=sig') as file:
        file.write(driver.page_source)

def parse_html(filename):
    with open(filename, 'r', encoding='utf-8=sig') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

def get_reviews(store_name):
    # 파일이 이미 존재하는지 확인
    filename = f"{store_name}_final_page.html"
    if os.path.exists(filename):
        print(f"{filename} 파일이 이미 존재합니다. 추가 작업 없이 반환합니다.")
        return

    count = 0
    # 무한 스크롤 및 더보기 요소 클릭 반복하여 html 코드 획득
    while True:
        try:
            # "더 보기" 버튼이 클릭 가능할 때까지 대기
            more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[.//span[contains(text(),"더 보기")]]'))
            )
            more_button.click()  # 버튼 클릭
            # print("더 보기 버튼이 클릭되었습니다.")
            time.sleep(TIME_DELAY)
        except:
            print(f"더 보기 버튼을 찾을 수 없습니다.count = {count}")
            print("html 저장")
            save_html(driver, f"{store_name}_final_page.html")  # HTML 저장
            break

        # 페이지 맨 아래로 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(TIME_DELAY)



def save_data_to_csv(store_name, dates, order_items, reviews, taste_score, quantity_score, delivery_score):
    # CSV 파일로 저장
    file_name = f"{store_name}_reviews.csv"
    with open(file_name, mode='w', newline='', encoding='utf-8=sig') as file:
        writer = csv.writer(file)
        writer.writerow(['dates', 'order_items', 'reviews', 'taste_score', 'quantity_score', 'delivery_score'])  # 헤더 작성
        for dates, order_items, reviews, taste_score, quantity_score, delivery_score in zip(dates, order_items, reviews, taste_score, quantity_score, delivery_score):
            writer.writerow([dates, order_items, reviews, taste_score, quantity_score, delivery_score])  # 데이터 작성
def goto_store(driver, num, store_name):
    try:
        # 스크롤 내리기
        print("move scroll down")
        scroll_down(driver)
        time.sleep(TIME_DELAY)
        print(f"num:{num}")

        # store_name 찾아 클릭
        # 'restaurants-info' 클래스를 가진 div를 찾음
        restaurants_info = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "restaurants-info"))
        )

        # 'restaurant-name ng-binding' 클래스를 가진 div를 찾아 클릭
        restaurant_name = WebDriverWait(restaurants_info, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.restaurant-name.ng-binding"))
        )
        restaurant_name.click()
        time.sleep(TIME_DELAY)

        # 클린 리뷰 속성을 찾아 클릭
        # 'ng-click' 속성이 'toggle_tab("review")'인 a 태그를 찾아 클릭
        review_tab_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[ng-click="toggle_tab(\\"review\\")"]'))
        )
        review_tab_link.click()
        time.sleep(TIME_DELAY)

        # 리뷰를 긁어서 html로 저장, 분석 함수는 별도로 구현
        get_reviews(store_name)
        
    except Exception as e:
        print(f'Error navigating to store {num + 1}: {e}')
        store_name = None

    return store_name

def process_data(region, driver):
    go_page(driver, region)
    stores = get_info(driver)

    for num, store_text in enumerate(stores):
        print(f"num: {num}, store_text:{store_text}")

        # 첫번째 가게와 그 외 가게 검색 방법이 달라 구분함
        if num == 0:
            # 사전에 추출한 가게이름을 활용하여 검색
            # 텍스트가 '검색'인 a 태그를 찾아 클릭
            search_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-default ico-search1' and text()='검색']"))
            )
            search_link.click()

            # 검색창에 접근
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "category_keyword"))
            )

            # 검색창에 store_text 변수의 값 입력
            store_text = store_text
            search_input.send_keys(store_text)
            time.sleep(TIME_DELAY)

            # 검색 버튼을 찾아 클릭
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "category_search_button"))
            )
            search_button.click()
            time.sleep(TIME_DELAY)

            print("go to store")
            goto_store(driver, num, store_text)
            time.sleep(TIME_DELAY)
        else:
            # 페이지 뒤로 가기
            driver.back()
            driver.implicitly_wait(5)
            print(num + 1, '뒤로가기 완료')
            time.sleep(TIME_DELAY)

            # 오동작 방지를 위한 구문: ID가 spinner 인 태그가 보이지 않을때까지 대기
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element((By.ID, "spinner"))
            )

            # 매장 검색
            # 텍스트가 '검색'인 a 태그를 찾아 클릭
            search_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[@class='btn btn-default ico-search1' and text()='검색']"))
            )
            search_link.click()
            time.sleep(TIME_DELAY)

            # 검색창에 접근하여 store_text 변수의 값 입력
            search_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "category_keyword"))
            )
            store_text = store_text
            search_input.send_keys(store_text)
            time.sleep(TIME_DELAY)

            # 검색 버튼을 찾아 클릭
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "category_search_button"))
            )
            search_button.click()
            time.sleep(TIME_DELAY)

            # 매장으로 이동
            print("go to store")
            goto_store(driver, num, store_text)

            # 스크롤 올리기
            print("move scrool to top")
            scroll_top(driver)
            time.sleep(TIME_DELAY)
    # driver 종료
    # driver.quit()

def only_parse_html_files(folder_path):
    # 폴더 내 html파일을 모두 찾아 리스트 생성
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    print(f"html_files:{html_files}")

    # 각 리스트(파일)별로 분석
    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        print(f"Processing file: {file_path}")

        # Open and read the HTML file
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            html_source = BeautifulSoup(content, 'html.parser')
            # print(f"{html_source}")

            # 주문 제품
            order_items = [div.get_text(strip=True) for div in html_source.find_all('div', class_='order-items')]
            print(f"Extracted {len(order_items)} order_items")
            # order_items = [r.text for r in order_items]
            print(f"dates Texts: {order_items}")

            # 리뷰 날짜
            dates = html_source.find_all('span', attrs={'class': 'review-time ng-binding',
                                                     'ng-bind': "review.time|since"})
            print(f"Extracted {len(dates)} dates")
            dates = [r.text for r in dates]
            print(f"dates Texts: {dates}")

            # 리뷰 내용
            reviews = html_source.find_all('p', attrs={'ng-show': 'review.comment',
                                                       'ng-bind-html': 'review.comment|strip_html'})
            print(f"Extracted {len(reviews)} reviews")
            reviews = [r.text for r in reviews]
            print(f"Review Texts: {reviews}")

            # 맛 점수
            taste_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                             'ng-show': "review.rating_taste > 0"})
            print(f"Extracted {len(taste_star)} taste_star")
            taste_star = [t.text for t in taste_star]
            print(f"taste_star Texts: {taste_star}")

            # 양 점수
            quantity_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                                'ng-show': "review.rating_quantity > 0"})
            print(f"Extracted {len(quantity_star)} quantity_star")
            quantity_star = [q.text for q in quantity_star]
            print(f"quantity_star Texts: {quantity_star}")

            # 배달 점수
            # 태그가 두 종류가 있어서, "points ng-binding"로 시작하는 태그를 전부 찾도록 코드 개선
            delivery_star = html_source.find_all('span', attrs={'class': lambda value: value and value.startswith('points ng-binding'),
                                                                'ng-show': "review.rating_delivery > 0"})
            print(f"Extracted {len(delivery_star)} delivery_star")
            delivery_score = [d.text for d in delivery_star]
            print(f"delivery_score Texts: {delivery_score}")

            time.sleep(TIME_DELAY)
            save_data_to_csv(html_file, dates, order_items, reviews, taste_star, quantity_star, delivery_score)


def make_donglist():
    try:
        # Load the CSV file and skip the first two header rows
        data = pd.read_csv("C:\\Users\\medit\\Desktop\\WorkSpace\\pythonProject\\BigDataMarketing\\분석에 활용한 데이터\\행정구역(동별)_20240422135054.csv", skiprows=2)

        # Drop unnecessary columns
        data = data.drop(['동별(1)'], axis=1)
        print(data.head(5))

        # Group by '동별(2)' and transform '동별(3)' into lists within a dictionary
        grouped_data = data.groupby('동별(2)')['동별(3)'].apply(list).to_dict()

        # Create a new list with modified neighborhood names to prevent duplication
        new_list = []
        for district, neighborhoods in grouped_data.items():
            modified_neighborhoods = [f"{district} {neighborhood}" for neighborhood in neighborhoods]
            new_list.append(modified_neighborhoods)

        # Remove a specific item from the list if present
        if "송파구 오륜동" in new_list:
            new_list.remove("송파구 오륜동")

        update_list = []

        for index in new_list:
            for number in index:
                update_list.append(number)

        return update_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []



if __name__ == '__main__':
    # 서울 행정구, 행정동 데이터로 딕셔너리 생성
    dong_list = make_donglist()
    print(type(dong_list))
    print(f"dong_list: {dong_list}")
    print(f"dong_list length: {len(dong_list)}")
    # if METHOD == 'crawling_parse':
    #     with initialize_driver() as driver:
    #         for district, neighborhoods in sample_dictionary.items():
    #             # print(f"{district}: {neighborhoods}")
    #             for gu in district:
    #                 for dong in neighborhoods:
    #                     print(f"run {gu}_{dong} crawling")
    #                     process_data(gu, dong, driver)

    if METHOD == 'crawling_parse':
        with initialize_driver() as driver:
            for city in dong_list:
                print(f"run {city} crawling")
                region = city
                process_data(region, driver)
    else:
        print("start parsing")
        only_parse_html_files(PATH)
