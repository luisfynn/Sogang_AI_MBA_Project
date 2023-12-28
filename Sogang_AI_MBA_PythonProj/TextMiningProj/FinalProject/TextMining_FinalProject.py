# 0. Selenium 설정 (PyCharm에서)
import sys
import io
import numpy as np
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
from bs4 import BeautifulSoup
import time
from selenium.webdriver import ActionChains # ActionChains 를 사용하기 위해서.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import nltk
nltk.download('stopwords')
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 전역 변수 설정
# URL 설정
URL = "https://www.pa.go.kr/research/contents/speech/index.jsp#this_id1"

# 크롤링 URL 최대 페이지 수(테스트 할 경우 2 ~ 13의 값으로 설정하여 테스트 진행하기)
MAX_PAGE = 429
MAX_EXCEL_TEXT = 30000

# 지연 시간 설정
WAIT_TIME = 1

# 크롤링
def RunCrawling(IsRunCrawling, IsCSV):
    print("---크롤링 시작---")
    driver = webdriver.Chrome()
    urlGoogle = "https://www.google.com"
    driver.get(urlGoogle)
    driver = webdriver.Chrome()
    SaveHTML = "" #스크래핑한 html을 기록
    count = 1 # 크롤링 페이지 카운트
    print("---크롤링 기본 설정 완료---")

    if IsRunCrawling == "True":
        driver.get(URL) #URL 접속
        last_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 높이 가져옴
        new_height = 0

        # 연설문 클릭(연설문만 리스트)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        speech_link = soup.find('a', text='연설문')
        speech_link_element = driver.find_element(By.LINK_TEXT, '연설문')
        speech_link_element.click()
        time.sleep(5)  # 대기

        # 크롤링 전체 과정
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")    # 끝까지 스크롤 다운 (마우스 이동 효과)

            SaveHTML = SaveHTML + driver.page_source        # HTML 코드 저장
            count += 1      # 페이지 카운트 증가

            # 최대 페이지에 도달하면 저장하고 종료
            if count == MAX_PAGE + 1:
                print("크롤링 완료")
                title_file = open("대통령 연설문.txt", 'w', encoding='UTF8')  ######################## 파일 저장
                title_file.write(SaveHTML)
                title_file.close()
                break

            if count % 10 == 0:
                # count 변수가 10으로 나누어 떨어지면 다음 페이지로 이동 클릭
                count += 1
                print("다음 페이지로 이동")
                next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
                next_button.click()
            else:
                # 다음 페이지 이동 클릭
                print("%d"%count + " 페이지로 이동")
                number_to_click = driver.find_element(By.LINK_TEXT, str(count))
                number_to_click.click()
            time.sleep(WAIT_TIME)  # 대기
    else:
        print("분석 진행")

    if IsCSV == "False":
        # 대통령 연설문.txt 읽어오기
        title_file = open("대통령 연설문.txt", 'r', encoding = 'UTF8')
        readString = ""

        while True:
            line = title_file.readline()
            readString = readString + line
            if not line: break
        title_file.close()

        soup = BeautifulSoup(readString, 'html.parser')

        # 빈 리스트를 생성하여 데이터를 저장할 준비
        data = {
            '번호': [],
            '대통령': [],
            '형태': [],
            '유형': [],
            '제목': [],
            '연설일자': [],
            '연설문URL': [],
            # '연설내용' : [],
        }

        # "tr" 요소를 찾아서 반복 처리
        for row in soup.find_all('tr'):
            tds = row.find_all('td')
            if len(tds) == 6:
                data['번호'].append(tds[0].text)
                data['대통령'].append(tds[1].text)
                data['형태'].append(tds[2].text)
                data['유형'].append(tds[3].text)
                data['제목'].append(tds[4].text)
                data['연설일자'].append(tds[5].text)
                #연설 내용이 있는 URL 추출
                data['연설문URL'].append("https://www.pa.go.kr/research/contents/speech/index.jsp"+tds[4].find('a')['href'] )

        # 데이터를 데이터프레임으로 변환 후 저장
        df = pd.DataFrame(data)
        df.to_csv('연설문_데이터.csv', index=False, encoding='utf-8-sig')

    print("연설문_데이터.csv에 연설 내용 저장")
    df = pd.read_csv("연설문_데이터.csv", encoding='utf-8-sig')

    for index, contentsURL in df['연설문URL'].items():
        print("%d"%index + "/" + "%d"%len(df['연설문URL']))
        driver.get(contentsURL)  # URL 접속

        # WebDriverWait를 사용하여 content 요소를 로딩할 때까지 기다림
        try:
            content_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'content'))
            )
            print("연설문 문자길이:%d" % len(content_element.text))

            if len(content_element.text) > MAX_EXCEL_TEXT:
                df.loc[index, '연설내용'] = content_element.text[0:MAX_EXCEL_TEXT]
            else:
                df.loc[index, '연설내용'] = content_element.text[0:MAX_EXCEL_TEXT]
        except Exception as e:
            df.loc[index, '연설내용'] = " "
            print("요소를 찾을 수 없거나 로딩하는 동안 문제가 발생했습니다:", str(e))
    df.to_csv('연설문_데이터.csv', index=False, encoding='utf-8-sig')
    return

# 실행 명령어
# 데이터가 많아, 단계별로 백업을 위한 파일을 생성(예: 크롤링한 html을 txt파일로 저장)
# def RunCrawling(IsRunCrawling, IsCSV):
# IsRunCrawling 변수 값:
#   True - 크롤링 + 저장 + 분석
#   False - 저장된 파일을 불러와 분석 진행
# IsCSV 변수 값 :
#   True - csv 파일을 불러와 연설 내용 긁어오기
#   False - html파일을 분석하여 대통령 이름/연설카테고리/연설제목/연설내용URL 등으로 로 구분 후 CSV로 저장 + csv 파일을 불러와 연설 내용 긁어오기
RunCrawling("False", "True")