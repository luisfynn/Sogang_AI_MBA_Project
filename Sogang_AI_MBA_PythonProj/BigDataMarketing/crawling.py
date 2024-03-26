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

USER_EMAIL = "luisfynn1@gmail.com"
USER_ID ="itaehwan162444"
USER_PASS = "@kj0224kj@"

def search_and_extract_html(search_query, start, stop, string):
    FMon, FDay, FYear = start.split('/')
    TMon, TDay, TYear = stop.split('/')

    if string != "parsing":
        print('search_and_extract_html에서 입력받은 search_query:', search_query)
        chrome_options = Options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://twitter.com/home?lang=ko')
        time.sleep(5)

        # 로그인창이 나오면 로그인 요소를 찾아
        search_box = driver.find_element(By.LINK_TEXT, "로그인")  #검색창 html의 name이 'q'여서 q다 # 검색창의 HTML name 속성에 따라 다름
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        # "휴대폰 번호"를 포함하는 <span> 요소 클릭-1
        # search_box = driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]").click()

        # "휴대폰 번호"를 포함하는 <span> 요소 클릭-2
        input_field_selector = "input[type='text'][name='text']" #동적 요소 제거
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        input_field.click()

        # "휴대폰 번호"를 포함하는 창에 아이디 입력 및 다음 버튼 클릭
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '휴대폰 번호')]/ancestor::label//input")))
        input_field.send_keys(USER_EMAIL)  # 입력할 텍스트로 교체해야 합니다.

        wait = WebDriverWait(driver, 10)
        phone_number_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '다음')]")))
        phone_number_span.click()

        # "휴대폰 번호"를 포함하는 창에 아이디 입력2
        # 분기가 있을 수 있어 try exception 구문 사용
        # 첫번째 분기 : 잦은 로그인 오류로 아이디 입력창(확인용) - 패스워드 입력창 순으로 뜨는 분기
        # 두번째 분기 : 바로 패스워드 입력창 순으로 뜨는 분기
        wait = WebDriverWait(driver, 10)
        try:
            input_field = wait.until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '휴대폰 번호')]/ancestor::label//input")))
            input_field.send_keys(USER_ID)

            wait = WebDriverWait(driver, 10)
            phone_number_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '다음')]")))
            phone_number_span.click()
        except TimeoutException:
            print("지정된 시간 내에 원하는 요소를 찾지 못하여, 다음 단계를 진행")

        input_field = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '비밀번호')]/ancestor::label//input")))
        input_field.send_keys(USER_PASS)

        wait = WebDriverWait(driver, 10)
        phone_number_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), '로그인하기')]")))
        phone_number_span.click()

        # 검색창 찾아 클릭하여 입력모드로 전환 후 검색어 입력, 클릭
        input_field_selector = "input[data-testid='SearchBox_Search_Input']"
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        input_field.click()
        input_field.send_keys(search_query)
        input_field.send_keys(Keys.RETURN)

        # 추가 검색을 위한 More(... 표기) 버튼 클릭
        button_selector = "[data-testid='searchBoxOverflowButton']"
        button_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, button_selector))
        )
        button_field.click()
        time.sleep(2)

        # Advanced search 클릭
        wait = WebDriverWait(driver, 10)
        advanced_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Advanced search')]")))
        advanced_span.click()
        time.sleep(2)

        # 검색어 재입력
        # time.sleep(100)
        input_field_selector = "input[type='text'][name='allOfTheseWords']" #동적 요소 제거
        input_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, input_field_selector))
        )
        input_field.click()
        input_field.send_keys(search_query)
        time.sleep(2)

        # BeautifulSoup 객체를 생성, html 코드 파싱하여 모든 SELECTOR_로 시작하는 모든 id 가져오기
        # id 가 동적으로 변경될 수 있으므로, 전부 가져와서 사용
        html_code = driver.page_source
        soup = BeautifulSoup(html_code, 'html.parser')
        selector_ids = [tag['id'] for tag in soup.find_all(id=True) if tag['id'].startswith('SELECTOR_')]
        print(selector_ids)

        # From 연/월/일 선택
        month_select = Select(driver.find_element(By.ID, selector_ids[3]))
        month_select.select_by_value(FMon)
        day_select = Select(driver.find_element(By.ID, selector_ids[5]))
        day_select.select_by_value(FDay)
        year_select = Select(driver.find_element(By.ID, selector_ids[7]))
        year_select.select_by_value(FYear)

        # To 연/월/일 선택
        month_select = Select(driver.find_element(By.ID, selector_ids[9]))
        month_select.select_by_value(TMon)
        day_select = Select(driver.find_element(By.ID, selector_ids[11]))
        day_select.select_by_value(TDay)
        year_select = Select(driver.find_element(By.ID, selector_ids[13]))
        year_select.select_by_value(TYear)
        time.sleep(2)

        # search 버튼 클릭
        wait = WebDriverWait(driver, 10)
        advanced_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Search')]")))
        advanced_span.click()
        time.sleep(2)

        # lastest 버튼 클릭
        wait = WebDriverWait(driver, 10)
        advanced_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Latest')]")))
        advanced_span.click()
        time.sleep(2)

        # Initialize the scroll_location variable
        scroll_location = 0
        html_code = list()

        while True:
            # 현재 스크롤 위치에 1000을 더해 스크롤 이동
            scroll_location += 1000
            driver.execute_script("window.scrollTo(0, {})".format(scroll_location))

            # 페이지 로딩 대기
            time.sleep(2)

            # 새 스크롤 위치 확인
            after_location = driver.execute_script("return window.pageYOffset")

            # 스크롤 위치와 새 위치 비교
            if scroll_location > after_location:
                break
            else:
                # HTML 코드 수집
                html_code.append(driver.page_source)

        # driver 종료
        driver.quit()

        # 문자열 리스트를 하나의 문자열로 결합
        html_combined = ''.join(html_code)

        soup = BeautifulSoup(html_combined, 'html.parser')

        # 스타일 값을 키로, 해당 div를 값으로 저장하는 딕셔너리
        divs_by_style = {}

        for div in soup.find_all('div', {'data-testid': 'cellInnerDiv'}):
            style = div.get('style')
            if style not in divs_by_style:
                divs_by_style[style] = div

        # 저장할 파일 쓰기
        with open("htmlCollect_{0}.txt".format(TYear), "w", encoding='utf-8') as file:
            for div in divs_by_style.values():
                # 파일에 div와 그 내용을 쓰기
                file.write(str(div))
                file.write("\n\n")  # 가독성을 위해 두 div 사이에 공백 라인 추가
        print("Done! unique_divs.txt has been saved.")

    # 저장할 파일 열기
    ID = list()
    with open("htmlCollect_{0}.txt".format(TYear), "r", encoding='utf-8') as file:
        html_content = file.read()

    # ID parsing
    soup = BeautifulSoup(html_content, "html.parser")

    for div in soup.find_all('div', {'data-testid': 'cellInnerDiv'}):
        # For each div, find the first (and only) instance of a div with data-testid="User-Name"
        user_name_div = div.find('div', {'data-testid': 'User-Name'})
        if user_name_div:
            # Add the text of the User-Name div to the list
            ID.append(user_name_div.get_text())

    # 개수 확인
    print(ID)
    print(len(ID))

    # Sentences parsing
    sentences = []

    for div in soup.find_all('div', {'data-testid': 'cellInnerDiv'}):
        user_name_div = div.find('div', {'data-testid': 'User-Name'})
        if user_name_div:
            sentence = " ".join(span.get_text() for span in div.find_all('span', class_="css-1qaijid r-bcqeeo r-qvutc0 r-poiln3"))
            sentences.append(sentence)

    # 개수 확인
    print(sentences)
    print(len(sentences))

    # date parsing
    date = []

    for div in soup.find_all('div', {'data-testid': 'cellInnerDiv'}):
        user_name_div = div.find('div', {'data-testid': 'User-Name'})
        if user_name_div:
            # Find the <time> tag within this div
            time_tag = div.find('time')
            if time_tag:
                # Extract the datetime attribute and add it to the list
                date.append(time_tag['datetime'])

    # 개수 확인
    print(date)
    print(len(date))

    # 파일로 저장
    df = pd.DataFrame()
    df['ID'] = ID
    df['sentences'] = sentences
    df['datetime'] = date
    df.to_csv("twitCrawling_{}_{}.csv".format(search_query, TYear), encoding='utf-8-sig')

    return html_content

if __name__ == '__main__':
    # search_and_extract_html('#챌린저스', "1/1/2024", "3/26/2024", "parsing")
    search_and_extract_html('#챌린저스', "1/1/2022", "12/31/2022", "") #crawling