import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm


def initialize_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument("--start-maximized")
    return webdriver.Chrome(options=options)


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

    # 검색 입력란 찾기 및 '굽네 치킨' 입력
    search_input = driver.find_element(By.NAME, 'category_keyword')
    search_input.clear()
    search_input.send_keys('굽네 치킨')

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

def goto_store(driver, num):
    store_name = None
    try:
        scroll_down(driver)
        try:
            # Wait until the element is clickable
            element_to_click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div/div[5]/div/div/div[{num}]'))
            )

            # Scroll the element into view (if necessary) and click using JavaScript
            driver.execute_script("arguments[0].scrollIntoView(true);", element_to_click)
            element_to_click.click()
            print("Element has been clicked successfully.")

        except Exception as e:
            print(f"Error clicking on the element: {e}")

        # # Targeting the store element
        # in_store_xpath = f'''//*[@id="content"]/div/div[3]/div/div[2]/div[{num+1}]/div/table/tbody/tr/td[2]'''
        # in_store = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.XPATH, in_store_xpath))
        # )
        # print(f"in_store: {in_store}")

        # store_name = in_store.text
        # print('Store name:', store_name)
        #
        # # Scroll the element into view and click using JavaScript
        # driver.execute_script("arguments[0].scrollIntoView(true);", in_store)
        # driver.execute_script("arguments[0].click();", in_store)
        #
        # # Accessing the reviews tab
        # review_btn_xpath = '//*[@id="content"]/div[2]/div[1]/ul/li[2]/a'
        # review_btn = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, review_btn_xpath))
        # )
        # driver.execute_script("arguments[0].click();", review_btn)
        # print(f'Accessed review tab for: {store_name}')

    except Exception as e:
        print(f'Error navigating to store {num + 1}: {e}')

    return store_name

# def goto_store(driver, num):
#     try:
#         scroll_down(driver)
#
#         # Targeting the store element
#         in_store_xpath = f'''//*[@id="content"]/div/div[3]/div/div[2]/div[{num+1}]/div/table/tbody/tr/td[2]'''
#         WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, in_store_xpath))
#         )
#         in_store = driver.find_element(By.XPATH, in_store_xpath)
#         time.sleep(1)  # Ensure any overlay has time to disappear
#         store_name = in_store.text
#         print('Store name:', store_name)
#
#         # Scroll the element into view and click using JavaScript
#         driver.execute_script("arguments[0].scrollIntoView(true);", in_store)
#         time.sleep(3)
#         driver.execute_script("arguments[0].click();", in_store)
#         time.sleep(3)
#
#         # Accessing the reviews tab
#         review_btn_xpath = '//*[@id="content"]/div[2]/div[1]/ul/li[2]/a'
#         review_btn = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, review_btn_xpath))
#         )
#         driver.execute_script("arguments[0].click();", review_btn)
#
#         print(f'Accessed review tab for: {store_name}')
#
#     except Exception as e:
#         print(f'Error navigating to store {num + 1}: {e}')
#         store_name = None
#
#     return store_name


def get_reviews(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    reviews = [review.text for review in soup.find_all('p', {'ng-show': 'review.comment'})]
    return reviews


# def process_data(region, driver):
#     go_page(driver, region)
#     stores = get_info(driver)
#     results = []
#     for num, store in enumerate(stores):
#         goto_store(driver, num)
#         reviews = get_reviews(driver)
#         results.append((store.text, reviews))
#         driver.back()
#     return results

def process_data(region, driver):
    go_page(driver, region)
    stores = get_info(driver)
    results = []

    # # Cache texts to avoid stale element reference
    # store_texts = [store.text for store in stores]
    # print(f"Store texts: {store_texts}")

    for num, store_text in enumerate(stores):
        print(f"num: {num}, store_text:{store_text}")
        goto_store(driver, num)
    #     reviews = get_reviews(driver)
    #     results.append((store_text, reviews))
    #     driver.back()

    return results

def save_to_dataframe(results):
    df = pd.DataFrame(columns=['Name', 'Review'])
    for name, reviews in results:
        for review in reviews:
            df = df.append({'Name': name, 'Review': review}, ignore_index=True)
    return df


if __name__ == '__main__':
    with initialize_driver() as driver:
        region = '구의동'
        results = process_data(region, driver)
        df = save_to_dataframe(results)
        print(df)
