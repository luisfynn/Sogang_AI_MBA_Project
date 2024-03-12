# Pycharm에서 selenium 구동 방법
# https://www.geeksforgeeks.org/selenium-python-introduction-and-installation/?ref=lbp
# https://www.softwaretestinghelp.com/selenium-python-tutorial/
#
# 1)	pip install selenium : terminal에서 pip install selenium 입력하여 selenium 설치
# 2)	[PyCharm 프로젝트명 하위]에 geckodriver.exe 파일 다운로드 받아서 저장
#
# [geckodriver.exe 파일 다운로드]
# geckodriver-v0.xxxx-win64.zip 최신버전받아 프로젝트 경로에 넣기
# https://github.com/mozilla/geckodriver/releases/

# 0. Selenium 설정 (PyCharm에서)
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

driver = webdriver.Chrome( )
url = "https://www.google.com"
driver.get(url)

# [3] 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
from selenium import webdriver
from bs4 import BeautifulSoup
import time
driver = webdriver.Chrome( )
url = "https://www.teamblind.com/kr/topics/%EC%A7%80%EB%A6%84%C2%B7%EC%87%BC%ED%95%91"
driver.get(url)

################################
SCROLL_PAUSE_SEC = 1
count = 0
last_height = driver.execute_script("return document.body.scrollHeight") # 스크롤 높이 가져옴
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 끝까지 스크롤 다운 (마우스 이동 효과)
    time.sleep(SCROLL_PAUSE_SEC) # 1초 대기
    count += 1

    new_height = driver.execute_script("return document.body.scrollHeight") # 스크롤 다운 후 스크롤 높이 다시 가져옴
    if new_height == last_height:
        break
    last_height = new_height

    if count == 100:
        #read & parser
        html1 = driver.page_source
        break

######################## 확인
soup = BeautifulSoup(html1, 'html.parser')
title_list = soup.select("div.tit > h3 > a")

titleList = list()
for i in range(0, len(title_list)):
    titleList.append(title_list[i].text)

import pandas as pd

data = {
    'Title': titleList
}
#print(data)
titleDf = pd.DataFrame(data)
print(titleDf.Title[0])
print(titleDf.Title[449])
print(titleDf.Title[899])

# 아이폰 쓰는 형아들 보통 몇년 쓰고 바꿔?
# 다들 이렇게 소비하고 계신가요? 허리휘어요 투표
# 언니들 속옷 어디꺼 많이 입어?


######################## 파일 저장
# title_file = open('title_file.txt', 'w', encoding='UTF8')
# title_file.write(title_file)
# title_file.close()

# # 1. teamblind 웹사이트 크롤링 (화면 아래까지 크롤링)
# # [1] 마우스 이용하여 스크롤 다운한 만큼만 크롤링
# from selenium import webdriver
# from bs4 import BeautifulSoup
# driver = webdriver.Chrome( )
# url = "https://www.teamblind.com/kr/topics/%EC%A7%80%EB%A6%84%C2%B7%EC%87%BC%ED%95%91"
# driver.get(url)
#
# ##### 새로이 생성된 크롬창(teamblind)에서 마우스를 스크롤 다운 시키면, 그 만큼까지의 데이터를 읽어 들일 수 있음
# ##### 마우스 스크롤 다운 없으면 52개만 출력
# ##### 확인
# html1 = driver.page_source
# soup = BeautifulSoup(html1, 'html.parser')
# title_list = soup.select("div.tit > h3 > a")
# len(title_list)
# title_list[90].text

# # [2] 지정한 시간 동안 웹페이지의 가능한 끝까지 스크래핑
# from selenium import webdriver
# from bs4 import BeautifulSoup import datetime
# import time
# driver = webdriver.Chrome( )
# url = "https://www.teamblind.com/kr/topics/%EC%A7%80%EB%A6%84%C2%B7%EC%87%BC%ED%95%91"
# driver.get(url)
#
# ################################# 10초 동안 자동 스크롤 다운 후 출력
# def doScrollDown(whileSeconds):
# start = datetime.datetime.now()
# end = start + datetime.timedelta(seconds=whileSeconds)
# while True:
#     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#     time.sleep(1)
#     if datetime.datetime.now() > end:
#     break
#     doScrollDown(10)
#
# ######################## 확인
# html1 = driver.page_source
# soup = BeautifulSoup(html1, 'html.parser')
# title_list = soup.select("div.tit > h3 > a")
# len(title_list)
# title_list[200].text
# # 참고 자료: https://hello-bryan.tistory.com/194

# # 2. 커피빈 크롤링
# #데이터 과학 기반의 파이썬 빅데이터 분석(이지영/ 한빛 아카데미)
# # 1) 매장 정보 찾기: www.coffeebeankorea.com > store > 매장 찾기 > 지역 검색 > 서울 선택할 때 좌측 하단 표시 보기
# # 2) javascript:storeLocal2(‘서울’) 표시 확인 후 호출
# # 3) HTML 소스 확인 (Ctrl+U): 조회된 매장 목록이 없음 => selenium 이용 필요
# # 4) 홈피로 돌아와서 [자세히 보기]에 마우스 올려 놓으면, javascript:storePop2(‘372’) 등이 나옴
# from bs4 import BeautifulSoup import urllib.request
#
# import pandas as pd
# import datetime
# from selenium import webdriver
# import time
#
# #[CODE 1]
# def CoffeeBean_store(result):
#     CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"
#     wd =webdriver.Chrome( )
#     for i in range(1, 370): #매장 수 만큼 반복
#         wd.get(CoffeeBean_URL)
#         time.sleep(1) #웹페이지 연결할 동안 1초 대기
#         try:
#             wd.execute_script("storePop2(%d)" % i)
#             time.sleep(1)  # 스크립트 실행 할 동안 1초 대기
#             html = wd.page_source
#             soupCB = BeautifulSoup(html, 'html.parser')
#             store_name_h2 = soupCB.select("div.store_txt > h2")
#             store_name = store_name_h2[0].string
#             print(store_name)  # 매장 이름 출력하기
#             store_info = soupCB.select("div.store_txt > table.store_table > tbody > tr > td")
#             store_address_list = list(store_info[2])
#             store_address = store_address_list[0]
#             store_phone = store_info[3].string
#             result.append([store_name] + [store_address] + [store_phone])
#         except:
#             continue
#     return
#
# #[CODE 0]
# def main():
#     result = []
#     print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
#     CoffeeBean_store(result) #[CODE 1]
#     CB_tbl = pd.DataFrame(result, columns=('store', 'address','phone'))
#     CB_tbl.to_csv('C:/CoffeeBean.csv', encoding='cp949', mode='w', index=True)
#
# if __name__  == ' main ':
#     main()
#
