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
import glob

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

SEARCH_KEYWORD = "챌린저스"
RUNMODE = "" #crawling : "", parsing : "parsing"
CRAWLING_URL = "https://play.google.com/store/apps/"
CRAWLING_COUNT = 100
WAIT_TIME = 1
WAIT_INFINITE = 1000000

def mouse_scrool_down(browser):
    # 셀레니움 스크롤 끝까지 내려도 계속 내리는 페이지라면
    prev_height = browser.execute_script("return document. body.scrollHeight")
    scrolldown_count = 0

    while True:
        # 첫번째로 스크롤 내리기
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        scrolldown_count += 1
        # 시간대기
        time.sleep(WAIT_TIME)

        # 현재높이 저장
        current_height = browser.execute_script("return document. body.scrollHeight")

        # 현재높이와 끝의 높이가 끝이면 탈출
        if current_height == prev_height:
            print("스크롤 다운 완료")
            break
        elif scrolldown_count >= 5:
            print("스크롤 다운 횟수 초과")
            break
        else:
            print("")
        # 업데이트해줘서 끝낼 수 있도록
        prev_height == current_height
    return

def file_mearge(browser, SEARCH_KEYWORD):
    # 검색할 디렉토리와 패턴 설정
    directory = '.'  # 현재 디렉토리
    pattern = 'htmlCollect_*.txt'

    # 패턴에 일치하는 모든 파일을 찾음
    files = glob.glob(f'{directory}/{pattern}')

    # 결합된 내용을 저장할 문자열
    combined_content = ''

    # 각 파일을 순회하면서 내용을 읽고 결합
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            combined_content += file.read() + '\n'  # 파일 내용을 결합하고, 파일 간 구분을 위해 줄바꿈 추가

    # 결합된 내용을 새 파일에 저장
    combined_file_path = "htmlCollect_{0}.txt".format(SEARCH_KEYWORD)
    with open(combined_file_path, 'w', encoding='utf-8') as combined_file:
        combined_file.write(combined_content)

    print(f'Combined file saved as {combined_file_path}')


def mouse_scrool_down_and_crawling(browser):
    # 셀레니움 스크롤 끝까지 내려도 계속 내리는 페이지라면
    prev_height = browser.execute_script("return document. body.scrollHeight")
    scrolldown_count = 0
    html_code = list()

    while True:
        # crawling data 저장
        html_code.append(browser.page_source)

        # 첫번째로 스크롤 내리기
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        scrolldown_count += 1
        print(scrolldown_count)
        # 시간대기
        # time.sleep(WAIT_TIME/2)

        # 현재높이 저장
        current_height = browser.execute_script("return document. body.scrollHeight")

        # 현재높이와 끝의 높이가 끝이면 탈출
        # if current_height == prev_height:
        #     print("크롤링 스크롤 다운 완료")
        #     break
        if scrolldown_count >= CRAWLING_COUNT:
            print("크롤링 스크롤 다운 횟수 초과")
            break
        else:
            if scrolldown_count !=0 and scrolldown_count / 5000 != 0 and scrolldown_count % 5000 == 0:
                # 5000과 같거나 크면서 5000의 배수일 때 끊어서 저장
                # 문자열 리스트를 하나의 문자열로 결합
                html_code_combined = ''.join(html_code)

                soup = BeautifulSoup(html_code_combined, 'html.parser')
                # 저장할 파일 쓰기
                with open("htmlCollect_{}_{}.txt".format(SEARCH_KEYWORD, scrolldown_count), "w", encoding='utf-8') as file:
                    file.write(str(soup))
                    print("Done! file has been saved.")
                    html_code.clear()
        # 업데이트해줘서 끝낼 수 있도록
        prev_height == current_height
    return html_code, scrolldown_count

def search_and_extract_html(search_query, string):
    if string != "parsing":
        print('search_and_extract_html에서 입력받은 search_query:', search_query)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(CRAWLING_URL)

        # 검색 아이콘 클릭
        wait = WebDriverWait(driver, 10)
        search_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="kO001e"]/header/nav/div/div[1]/button')))
        search_field.click()

        # 검색창에 키워드 입력
        wait = WebDriverWait(driver, 10)
        search_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="kO001e"]/header/nav/c-wiz/div/div/label/input')))
        search_field.send_keys(SEARCH_KEYWORD)
        search_field.send_keys(Keys.ENTER)

        # 검색된 앱 클릭
        wait = WebDriverWait(driver, 10)
        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[3]/div/div/c-wiz/c-wiz[1]/c-wiz/section/div/div/a')))
        search_field.click()

        # 페이지의 끝까지 스크롤
        mouse_scrool_down(driver)

        # 리뷰 모두 보기 클릭
        wait = WebDriverWait(driver, 10)
        search_field = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/c-wiz[5]/section/div/div[2]/div[5]/div/div/button/span')))
        search_field.click()

        # 페이지 스크롤 내리며 크롤링
        crawl_data, scrolldown = mouse_scrool_down_and_crawling(driver)

        # 잔여 내용 저장
        # 문자열 리스트를 하나의 문자열로 결합
        html_code_combined = ''.join(crawl_data)

        soup = BeautifulSoup(html_code_combined, 'html.parser')
        # 저장할 파일 쓰기
        with open("htmlCollect_{}_{}.txt".format(SEARCH_KEYWORD, scrolldown), "w", encoding='utf-8') as file:
            file.write(str(soup))
            print("Done! final file has been saved.")

        # driver 종료
        driver.quit()

        # 파일 모두 열어서 하나의 파일로 저장
        file_mearge(driver, string)

        # # 문자열 리스트를 하나의 문자열로 결합
        # crawl_data_combined = ''.join(crawl_data)
        #
        # soup = BeautifulSoup(crawl_data_combined, 'html.parser')
        # # 저장할 파일 쓰기
        # with open("htmlCollect_{}.txt".format(SEARCH_KEYWORD), "w", encoding='utf-8') as file:
        #     file.write(str(soup))
        # print("Done! file has been saved.")

    # 저장할 파일 열기
    with open("htmlCollect_{0}.txt".format(SEARCH_KEYWORD), "r", encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # 파싱할 변수 생성
    parsing_ID = list()
    parsing_date = list()
    parsing_content = list()
    parsing_score = list()

    for div in soup.find_all('div', {'class': 'X5PpBb'}):
        parsing_ID.append(div.get_text())

    for div in soup.find_all('span', {'class': 'bp9Aid'}):
        parsing_date.append(div.get_text())

    for div in soup.find_all('div', {'class': 'h3YV2d'}):
        parsing_content.append(div.get_text())

    for div in soup.find_all('div', {'class': 'iXRFPc'}):
        parsing_score.append(div['aria-label']) #속성값을 가져와야 함

    # 파일로 저장
    df = pd.DataFrame()
    df['ID'] = parsing_ID
    df['sentences'] = parsing_content
    df['datetime'] = parsing_date
    df['score'] = parsing_score
    df.to_csv("googleAppCrawling_{}.csv".format(SEARCH_KEYWORD), encoding='utf-8-sig')
    return 0

if __name__ == '__main__':
    search_and_extract_html(SEARCH_KEYWORD, RUNMODE)