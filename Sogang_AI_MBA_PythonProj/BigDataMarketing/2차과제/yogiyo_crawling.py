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

# CITY_KEYWORD = ['천연동','홍제1동','홍제2동','홍제3동','홍은1동','홍은2동','남가좌1동','남가좌2동','북가좌1동','북가좌2동','충현동','북아현동','신촌동','연희동']
CITY_KEYWORD = ['홍제1동','홍제2동','홍제3동','홍은1동','홍은2동','남가좌1동','남가좌2동','북가좌1동','북가좌2동','충현동','북아현동','신촌동','연희동']
BRAND_KEYWORD = '굽네치킨' #굽네치킨, BBQ, 60계치킨
METHOD = 'crawling_parse' #'crawling_parse' or 'parse'

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
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def go_page(driver, region):
    driver.get("https://www.yogiyo.co.kr/mobile/#")
    driver.maximize_window()

    # 지역 검색창이 로드될 때까지 대기
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="search"]/div/form/input')))
    search_input.clear()
    search_input.send_keys(region)

    # 검색 버튼 클릭
    search_button = driver.find_element(By.XPATH, '//*[@id="button_search_address"]/button[2]')
    search_button.click()

    # 주소 검색 결과 클릭 대기
    search_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a')))
    search_result.click()

    # 첫 번째 카테고리 항목 클릭
    first_list_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="category"]/ul/li[1]')))
    first_list_item.click()

    # 검색 입력란에 BRAND_KEYWORD 입력
    search_input = driver.find_element(By.NAME, 'category_keyword')
    search_input.clear()
    search_input.send_keys(BRAND_KEYWORD)

    # 검색 버튼 찾기 및 클릭
    search_button = driver.find_element(By.ID, 'category_search_button')
    search_button.click()

    # 결과 페이지 로딩 대기
    time.sleep(5)  # 필요에 따라 시간 조절 가능


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

    return restaurant_names

def save_html(driver, filename="page.html"):
    #현재 페이지의 HTML을 파일로 저장
    with open(filename, 'w', encoding='utf-8=sig') as file:
        file.write(driver.page_source)

def parse_html(filename):
    with open(filename, 'r', encoding='utf-8=sig') as file:
        soup = BeautifulSoup(file, 'html.parser')
    return soup

def get_reviews(store_name):
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
            time.sleep(1)  # 페이지 로딩 대기
        except:
            print(f"더 보기 버튼을 찾을 수 없습니다.count = {count}")
            print("html 저장")
            save_html(driver, f"{store_name}_final_page.html")  # HTML 저장
            break

        # 페이지 맨 아래로 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # 스크롤 후에 페이지 로딩을 위해 대기



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
        print("move scroll down")
        scroll_down(driver)
        time.sleep(5)
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
        time.sleep(3)

        # 클린 리뷰 찾아 클릭
        # Accessing the reviews tab
        # 'ng-click' 속성이 'toggle_tab("review")'인 a 태그를 찾아 클릭
        review_tab_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[ng-click="toggle_tab(\\"review\\")"]'))
        )
        review_tab_link.click()
        time.sleep(3)

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

        # 첫번째 가게와 나머지 가게 검색방법이 달라 구분함
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
            time.sleep(5)

            # 검색 버튼을 찾아 클릭
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "category_search_button"))
            )
            search_button.click()

            # 결과 페이지 로딩 대기
            time.sleep(5)

            print("go to store")
            goto_store(driver, num, store_text)
            # 대기
            time.sleep(5)
        else:
            driver.back()
            driver.implicitly_wait(5)
            print(num + 1, '뒤로가기 완료')
            time.sleep(5)

            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element((By.ID, "spinner"))
            )

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
            time.sleep(5)

            # 검색 버튼을 찾아 클릭
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "category_search_button"))
            )
            search_button.click()

            # 결과 페이지 로딩 대기
            time.sleep(5)

            print("go to store")
            goto_store(driver, num, store_text)

            print("move scrool to top")
            scroll_top(driver)
            # 대기
            time.sleep(5)
    # driver 종료
    # driver.quit()

def only_parse_html_files(folder_path):
    # List all files in the given folder
    html_files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
    print(f"html_files:{html_files}")

    # Loop through each file
    for html_file in html_files:
        file_path = os.path.join(folder_path, html_file)
        print(f"Processing file: {file_path}")

        # Open and read the HTML file
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()
            html_source = BeautifulSoup(content, 'html.parser')
            # print(f"{html_source}")

            order_items = [div.get_text(strip=True) for div in html_source.find_all('div', class_='order-items')]
            print(f"Extracted {len(order_items)} order_items")
            # order_items = [r.text for r in order_items]
            print(f"dates Texts: {order_items}")  # Check the text extraction

            dates = html_source.find_all('span', attrs={'class': 'review-time ng-binding',
                                                     'ng-bind': "review.time|since"})
            print(f"Extracted {len(dates)} dates")
            dates = [r.text for r in dates]
            print(f"dates Texts: {dates}")  # Check the text extraction

            reviews = html_source.find_all('p', attrs={'ng-show': 'review.comment',
                                                       'ng-bind-html': 'review.comment|strip_html'})
            print(f"Extracted {len(reviews)} reviews")
            reviews = [r.text for r in reviews]
            print(f"Review Texts: {reviews}")  # Check the text extraction

            taste_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                             'ng-show': "review.rating_taste > 0"})
            print(f"Extracted {len(taste_star)} taste_star")
            taste_star = [t.text for t in taste_star]
            print(f"taste_star Texts: {taste_star}")  # Check the text extraction

            quantity_star = html_source.find_all('span', attrs={'class': 'points ng-binding',
                                                                'ng-show': "review.rating_quantity > 0"})
            print(f"Extracted {len(quantity_star)} quantity_star")
            quantity_star = [q.text for q in quantity_star]
            print(f"quantity_star Texts: {quantity_star}")  # Check the text extraction

            delivery_star = html_source.find_all('span', attrs={'class': 'points ng-binding ng-hide',
                                                                'ng-show': "review.rating_delivery > 0"})
            print(f"Extracted {len(delivery_star)} delivery_star")
            delivery_score = [d.text for d in delivery_star]
            print(f"delivery_score Texts: {delivery_score}")  # Check the text extraction

            time.sleep(2)
            save_data_to_csv(html_file, dates, order_items, reviews, taste_star, quantity_star, delivery_score)


if __name__ == '__main__':
    if METHOD == 'crawling_parse':
        with initialize_driver() as driver:
            for city in CITY_KEYWORD:
                region = city
                process_data(region, driver)
    # else:
    only_parse_html_files('C:\\Users\\medit\\Desktop\\WorkSpace\\pythonProject\\BigDataMarketing\\')
