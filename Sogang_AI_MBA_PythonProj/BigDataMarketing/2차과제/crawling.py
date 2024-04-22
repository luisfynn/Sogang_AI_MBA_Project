import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pandas as pd

SEARCH_KEYWORD = "천연동"
RUNMODE = ""  # crawling: "", parsing: "parsing"


def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow page to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# def search_and_extract_html(search_query, mode):
#     if mode != "parsing":
#         print(f'Searching and extracting HTML for: {search_query}')
#         chrome_options = Options()
#         driver = webdriver.Chrome(options=chrome_options)
#         driver.get('https://www.yogiyo.co.kr/mobile/#')
#
#         try:
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.XPATH, '''//*[@id="search"]/div/form/input'''))
#             )
#             search_box = driver.find_element(By.XPATH, '''//*[@id="search"]/div/form/input''')
#             search_box.clear()
#             search_box.send_keys(search_query)
#
#             search_button = driver.find_element(By.XPATH, '''//*[@id="button_search_address"]/button[2]''')
#             driver.execute_script("arguments[0].click();", search_button)
#
#             # click combo-box
#             WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a'))
#             )
#             search_result = driver.find_element(By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a')
#             driver.execute_script("arguments[0].click();", search_result)
#
#             html_code = []
#             scroll_down(driver)
#             html_code.append(driver.page_source)
#
#             with open('collected_data.html', 'w', encoding='utf-8') as file:
#                 for html in html_code:
#                     file.write(html + '\n')
#
#         finally:
#             driver.quit()
#
#         # Use BeautifulSoup to parse HTML
#         soup = BeautifulSoup(html, 'html.parser')
#
#         # Data list to hold all restaurant information
#         data = []
#
#         # Extract data from each restaurant block
#         restaurants = soup.find_all('div', class_='restaurants-info')
#         for restaurant in restaurants:
#             name = restaurant.find('div', class_='restaurant-name').text.strip()
#             # Find the restaurant link element by its name
#             stars = restaurant.find('span', class_='ico-star1').text.strip() if restaurant.find('span', class_='ico-star1') else ''
#             review_count = restaurant.find('span', class_='review_num').text.strip() if restaurant.find('span', class_='review_num') else ''
#             payment_method = restaurant.find('li', class_='payment-methods').text.strip() if restaurant.find('li', class_='payment-methods') else ''
#             min_price = restaurant.find('li', class_='min-price').text.strip() if restaurant.find('li', class_='min-price') else ''
#             delivery_time = restaurant.find('li', class_='delivery-time').text.strip() if restaurant.find('li', class_='delivery-time') else ''
#
#             # Append the extracted information to the data list as a tuple
#             data.append((name, stars, review_count, payment_method, min_price, delivery_time))
#
#         # Create a DataFrame
#         df = pd.DataFrame(data, columns=['Name', 'url', 'Rating', 'Review Count', 'Payment Method', 'Minimum Order Price', 'Delivery Time'])
#
#         # save to file
#         df.to_csv(f"yogiyo_{SEARCH_KEYWORD}.csv", encoding='utf-8-sig')

# get stores count
def get_stores_count(search_query, mode):
    print(f'Searching and extracting HTML for: {search_query}')
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.yogiyo.co.kr/mobile/#')

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="search"]/div/form/input'''))
        )
        search_box = driver.find_element(By.XPATH, '''//*[@id="search"]/div/form/input''')
        search_box.clear()
        search_box.send_keys(search_query)

        search_button = driver.find_element(By.XPATH, '''//*[@id="button_search_address"]/button[2]''')
        driver.execute_script("arguments[0].click();", search_button)

        # click combo-box
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a'))
        )
        search_result = driver.find_element(By.CSS_SELECTOR, '#search > div > form > ul > li:nth-child(3) > a')
        driver.execute_script("arguments[0].click();", search_result)

        html_code = []
        scroll_down(driver)
        html_code.append(driver.page_source)

        with open('collected_data.html', 'w', encoding='utf-8') as file:
            for html in html_code:
                file.write(html + '\n')

    finally:
        driver.close()
    return
def search_and_extract_html(search_query, mode):
    get_stores_count(search_query, mode)

    return

if __name__ == '__main__':
    search_and_extract_html(SEARCH_KEYWORD, RUNMODE)
