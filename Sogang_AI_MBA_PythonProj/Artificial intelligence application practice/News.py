# 4. 뉴스 요약 전달
# 경제-금융 뉴스 상위 10건 title과 url추출 함수
import requests
from bs4 import BeautifulSoup
import bs4.element
import datetime
import lxml

UserAgentKey = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'

#뉴스 크롤링 원할화 작업
def get_soup_obj(url):
    head = {
        'User-Agent': UserAgentKey
    }  # 본인 PC에서 User-Agent 정보 검색해서 얻은 값 입력
    res = requests.get(url, headers=head)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup

# 경제-금융 뉴스 상위 10건 title과 url추출 함수
# naver 사이트에서 f12키 누름
def get_top_news_info(area):
    soup = get_soup_obj(area)
    news_list = []
    list10 = soup.find('ul', class_='type06_headline').find_all("li", limit=10)  # 경제-부동산 뉴스 상위 10건
    for li in list10:
        news_info = {
            "title": li.img.attrs.get('alt') if li.img else li.a.text,
            "news_url": li.a.attrs.get('href'),
        }
        news_list.append(news_info)
    return news_list

# 경제-금융 뉴스 url
area_url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=260"
soup = get_soup_obj(area_url)
soup

get_top_news_info(area_url)
len(get_top_news_info(area_url))

#######################################################################
#경제-금융 뉴스 상위 10건 본문 contents 추출 함수
# url 건별 뉴스 본문 내용(contents) 추출 함수
def get_news_contents(url):
    soup = get_soup_obj(url)
    body = soup.find('div', id="dic_area") #div, id 가 dic_area 내용을 찾아 body에 저장
    news_contents = ''
    for content in body:
        if type(content) is bs4.element.NavigableString and len(content) > 30: # 30 글자 이상 문장만 포함
            news_contents += content.strip() + ' ' # 뉴스 요약 위해 마침표 뒤에 한 칸 띄기
    return news_contents

# 10건의 url로부터 뉴스 본문 내용으로 연결 및 content 추출 함수
def get_news_contents_list(url):
    news_list10 = get_top_news_info(url)
    news_content_list = []
    for url_i in news_list10:
        urli = url_i['news_url']
        news_content = get_news_contents(urli)
        news_content_list.append(news_content)
    return news_content_list

# 네이버 경제-부동산 뉴스 10건의 본문 내용 추출
area_url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=101&sid2=260"
get_news_contents_list(area_url)
#len(get_news_contents_list(area_url))
get_news_contents_list(area_url)[1]

#######################################################################
#크롤링한 네이버 뉴스 요약
#pip install gensim==3.8.3 # gensim 버전 지정하여 설치 할 것
#pycharm 21.3 버전과 python 3.9 버전 사용(그 외엔 gensim 3.8.3 설치 실패함_230705)


import gensim
from gensim.summarization.summarizer import summarize
news_cont10 = get_news_contents_list(area_url)
news_cont10

# 뉴스 요약하기
snews_cont10 = []
for news_info in news_cont10:
    try: # 20 단어 이상이면 가능하면 20단어 이하로 요약
        snews_contents = summarize(news_info, word_count=20)
    except: # 20 단어 이하면 원래 뉴스 전체 보고
        snews_contents = news_info
    snews_cont10.append(snews_contents)

# 요약 결과: 첫번째 뉴스
print("== 첫번째 뉴스 ==")
print(news_cont10[0])
len(news_cont10[0])
print("\n=== 첫번째 뉴스 요약문 ===")
print(snews_cont10[0])
len(snews_cont10[0])

#뉴스 요약 결과 검토
#원래 뉴스 단어 수
word_num1 =[]
for i in news_cont10:
    num_i = len(i.split())
    word_num1.append(num_i)

# 요약한 뉴스 단어 수
word_num2 =[]
for j in snews_cont10:
    num_j = len(j.split())
    word_num2.append(num_j)

# 단어 수 비교
word_num1
word_num2

#######################################################################