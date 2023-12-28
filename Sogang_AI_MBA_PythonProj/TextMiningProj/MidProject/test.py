# # Konlpy에서 Okt를 불러옵니다.
# from konlpy.tag import Okt
# from collections import Counter
# # Okt Class의 생성자를 이용하여 분석기를 생성
# okt = Okt()
#
# # 생성된 객체를 이용하여 형태소를 분석합니다.
# print(okt.nouns("오늘 밤 주인공은 나야 나 나야 나"))
#
# print(Counter(okt.nouns("오늘 밤 주인공은 나야 나 나야 나")).most_common(3))

from bs4 import BeautifulSoup
import bs4.element
import datetime
import requests

# def get_soup_obj(url):
#   head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60'} # 본인 PC에서 User-Agent 정보 검색해서 얻은 값 입력
#   res = requests.get(url, headers = head)
#   soup = BeautifulSoup(res.text, 'html.parser')
#   return soup
#
# get_soup_obj("https://premiumoutlets.co.kr/rpage/store/index/02")
#
# url = "https://premiumoutlets.co.kr/rpage/store"
# soup = get_soup_obj(url)
# print(soup)
#
# import requests
# from bs4 import BeautifulSoup

# # 가져오기 원하는 url 주소
# url = "https://premiumoutlets.co.kr/rpage/store/index/02.html"
#
# response = requests.get(url)
#
# if response.status_code == 200:  # 에러가 발생되지 않으면
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     print(soup)

# import requests
#
# url = "http://premiumoutlets.co.kr/rpage/store/index/02/"
# response = requests.get(url)
#
# if response.status_code == 200:
#     html_code = response.text
#     print(html_code)
# else:
#     print(f"Failed to retrieve HTML. Status code: {response.status_code}")

from selenium import webdriver

# 웹 드라이버 초기화
driver = webdriver.Chrome()

# 웹 페이지 열기
url = "http://premiumoutlets.co.kr/rpage/store/index/02"  # 대상 웹 페이지의 URL로 변경
driver.get(url)

# 페이지 소스 가져오기
page_source = driver.page_source

# 페이지 소스 출력
print(page_source)

# 웹 드라이버 종료
driver.quit()