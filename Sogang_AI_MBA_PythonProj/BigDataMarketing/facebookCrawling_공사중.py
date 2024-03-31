import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time
import csv
from bs4 import BeautifulSoup
import requests

#selenium v4.x.x(here: 4.18.1)
# driver.find_element(By.CLASS_NAME, "")
# driver.find_element(By.ID, "")
# driver.find_element(By.CSS_SELECTOR, "")
# driver.find_element(By.NAME, "")
# driver.find_element(By.TAG_NAME, "")
# driver.find_element(By.XPATH, "")
# driver.find_element(By.LINK_TEXT, "")
# driver.find_element(By.PARTIAL_LINK_TEXT, "")
# (복수형 driver.find_elements(By.~~, "")

#selenium 요소를 조작하기
#메서드/       속성설명
#clear()        글자를 지운다
#click()	    요소를 클릭
#get_attribute(name)	요소 속성중 name에 해당하는 속성 값을 추출
#is_displayed()	요소가 화면에 출력되는지 확인
#is_enabled()	요소가 활성화돼 있는지 확인
#is_selected()	체크박스 등의 요소가 선택된 상태인지 확인
#screenshot(filename)	스크린샷
#send_keys(value)	키를 입력
#submit()	입력 양식을 전송
#value_of_css_property(name)	name에 해당하는 css속성 값을 추출
#id	id
#location	요소의 위치
#parent	부모요소
#rect	크기와 위치 정보를 가진 사전자료형 리턴
#screenshot_as_base64	스크린샷을 base64로 추출
#screenshot_as_png	스크린샷을 png형식의 바이너리로 추출
#size	요소의 크리
#tag_name	태그 이름
#text	요소의 내부 글자

FACEBOOK_ID = "luisfynn1@gmail.com"
FACEBOOK_PASS = "@kj0224kj@"
TIME_SLEEP = 1
INFINITE_TIME_SLEEP = 5000
SCROLL_COUNT = 10
KEY_WORD = '챌린저스'
FROM_DATE = '1/1/2024'
TO_DATE = '3/26/2024'
RUN_CRAWLING = '' # select '' or 'parsing'

# [주의사항] facebook 로그인 후 "facebook 권한 요청"은 수동으로 선택해줘야 함

def search_and_extract_html(search_query, start, stop, string):
    FMon, FDay, FYear = start.split('/')
    TMon, TDay, TYear = stop.split('/')

    if string != "parsing":
        print('search_and_extract_html에서 입력받은 search_query:', search_query)
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.facebook.com/')
        time.sleep(TIME_SLEEP)

        # 로그인
        input_field_selector = "input[id='email'][placeholder='이메일 또는 전화번호']"
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        input_field.click()
        input_field.send_keys(FACEBOOK_ID)

        input_field_selector = "input[id='pass'][placeholder='비밀번호']"
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        input_field.click()
        input_field.send_keys(FACEBOOK_PASS)

        wait = WebDriverWait(driver, 10)
        login_sapn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '로그인')]")))
        login_sapn.click()
        time.sleep(TIME_SLEEP)

        # 검색어 입력 및 검색
        input_field_selector = "input[aria-label='Facebook 검색'][type='search']"
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        print("Input Field: ", input_field)
        time.sleep(TIME_SLEEP)
        input_field.send_keys(search_query)
        input_field.send_keys(Keys.ENTER)

        # 검색 세부 조정(불가능)
        # wait = WebDriverWait(driver, 10)
        # login_sapn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '게시물')]")))
        # login_sapn.click()
        time.sleep(TIME_SLEEP * 10)

        # 스크롤 내리면서 html code 가져오기
        # Initialize the scroll_location variable
        scroll_location = 0
        scroll_cnt = 0
        html_code = list()

        while True:
            # 현재 스크롤 위치에 500을 더해 스크롤 이동
            scroll_location += 500
            driver.execute_script("window.scrollTo(0, {})".format(scroll_location))
            driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_location)

            # 페이지 로딩 대기
            time.sleep(TIME_SLEEP)

            # HTML 코드 수집
            scroll_cnt += 1
            if scroll_cnt >= SCROLL_COUNT:
                print("crwaling has been stopped")
                break
            html_code.append(driver.page_source)

        # driver 종료
        driver.quit()

        # 문자열 리스트를 하나의 문자열로 결합
        html_combined = ''.join(html_code)

        # 저장할 파일 쓰기
        with open("htmlCollect_{0}.txt".format(TYear), "w", encoding='utf-8') as file:
            file.write(html_combined)
            file.write("\n\n")  # 가독성을 위해 두 div 사이에 공백 라인 추가
        print("Done! textfile has been saved.")

    # 저장할 파일 열기
    with open("htmlCollect_{0}.txt".format(TYear), "r", encoding='utf-8') as file:
        html_combined = file.read()

    # ID parsing
    soup = BeautifulSoup(html_combined, 'html.parser')

    # parsing
    ID_list = []
    contents_list = []
    date_list = []

    # 모든 'div' 태그를 찾아 반복 처리
    for div in soup.find_all('div', attrs={"aria-posinset": True}):
        number = div.get('aria-posinset')
        # 중복되지 않는 number 기준으로 content 추출
        if number and div.find('h3', attrs={"id": True}):
            content = div.find('h3', attrs={"id": True}).text
            # if content != "팔로우" and content != "가입":
            ID_list.append(content)
            # content[number] = content

        if number:
            # content 추출
            texts = div.find_all('div', dir="auto", style="text-align: start;")
            combined_text = ''.join([text.get_text(strip=True) for text in texts])
            contents_list.append(combined_text)

            # date 추출
            for div in soup.find_all('a', {
                'class': 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm'}):
                date_list.append(div.get_text())

    print("------------------")
    print(ID_list)
    print(len(ID_list))
    print("------------------")
    print(contents_list)
    print(len(contents_list))
    print("------------------")
    print(date_list)
    print(len(date_list))
    print("------------------")
    return 0

if __name__ == '__main__':
    search_and_extract_html(KEY_WORD, FROM_DATE, TO_DATE, RUN_CRAWLING)