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
import sys
import io
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

######################## 변수 설정
url = [
    "https://www.teamblind.com/kr/topics/%EC%A7%80%EB%A6%84%C2%B7%EC%87%BC%ED%95%91", #연습용_팀블라인드
    "https://www.aitimes.com/news/articleList.html?", #AI 타임즈
    "https://techcrunch.com/", #techcrunch,
    "https://www.forbes.com/ai/"
]

fileList =[
    "teamblind.txt",
    "aitimes.txt",
    "techcrunch.txt",
    "forbes.txt"
]

CloudList =[
    "teamblind.png",
    "aitimes.png",
    "techcrunch.png",
    "forbes.png"
]

#NotIncludeWord = ['drink', 'now', 'wine', 'flavor', 'flavors']
PATH = "C:\\Users\\luisf\\OneDrive\\바탕 화면\\WorkSpace\\SeleniumExer\\BareunBatangM.ttf"

GLOBAL_MAX = 1000  #220 #크롤링 사이트 갯수 정의
SLEEP_TIME = 1 #지연시간(초)
MAX_WORD = 10

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

global CrawlDf
######################## 크롤링 & 워드클라우드 함수
def wordCloud(dataframe, locaton, selyear):
    # 모든 description을 한 문장(str)으로 만들어줍니다.
    text = ''.join(v for v in dataframe["Title"])

    if locaton == 2:
        stopwords = nltk.corpus.stopwords.words('english')
    else:
        stopwords = set(STOPWORDS)
        stopwords.update(STOPWORDS)  # 제거할 단어들

    print("run wordcloud")
    wordcloud = WordCloud(background_color='white', max_words=300, width=1600, height=1000, stopwords=stopwords,
                          scale=3, font_path=PATH).generate(text)

    print(wordcloud)
    plt.figure()
    plt.axis('off')  # 눈금 삭제
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig("%d_"%selyear + CloudList[locaton])
    return

def CrawlingReadCloudFunc(location, Crawling, IsWordCloud, selyear):
    if Crawling == "true":
        print("start crawling")
        driver = webdriver.Chrome()
        urlGoogle = "https://www.google.com"
        driver.get(urlGoogle)

    if location == 0:
        if Crawling == "true":
            print("start crawling")
            driver = webdriver.Chrome()
            urlGoogle = "https://www.google.com"
            driver.get(urlGoogle)

            # 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
            driver = webdriver.Chrome()
            driver.get(url[location])

            count = 0
            last_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 높이 가져옴

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 끝까지 스크롤 다운 (마우스 이동 효과)
                time.sleep(SLEEP_TIME) #대기
                count += 1
                new_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 다운 후 스크롤 높이 다시 가져옴

                if count == GLOBAL_MAX:
                    # read & parser
                    html1 = driver.page_source

                    ######################## 파일 저장
                    title_file = open(fileList[location], 'w', encoding='UTF8')
                    title_file.write(html1)
                    title_file.close()
                    break

        title_file = open(fileList[location], 'r', encoding='UTF8')

        readString = ""
        while True:
            # print("run reading")
            line = title_file.readline()
            readString = readString + line
            if not line: break
        title_file.close()

        # blind 파싱
        soup = BeautifulSoup(readString, 'html.parser')
        title_list = soup.select("div.tit > h3 > a")

        titleList = list()
        for i in range(0, len(title_list)):
            titleList.append(title_list[i].text)

        data = {
            'Title': titleList
        }
        # print(data)
        CrawlDf = pd.DataFrame(data)

        if selyear == 0:
            SelCrawDf = CrawlDf
        else:
            print("Sel year:%d"%selyear)
            SelCrawDf = CrawlDf[CrawlDf['Year'] == '%d'%selyear]
            print(SelCrawDf.head(6))
            print(SelCrawDf['Year'].unique())
            SelCrawDf = SelCrawDf.reset_index()
            print(SelCrawDf.head(5))
        if IsWordCloud:
            wordCloud(SelCrawDf, location, selyear)
        else:
            make_top_word_graph(location, SelCrawDf, MAX_WORD, selyear)
        print("Finish")
        return

    elif location == 1:
        print("enter %d"%location)
        # 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
        count = 0
        readString = ""
        html1 = ""

        if Crawling == "true":
            print("start crawling")
            driver = webdriver.Chrome()
            urlGoogle = "https://www.google.com"
            driver.get(urlGoogle)

            # 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
            driver = webdriver.Chrome()

        for i in range(0, GLOBAL_MAX):
            if Crawling == "true":
                urlTotal = url[location] + "page=%d" % (i+1) + "&total=13788&box_idxno=&view_type=sm"
                #urlTotal = url[location] + "page="+(i+1)
                print(urlTotal)
                driver.get(urlTotal)

                last_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 높이 가져옴

                # while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 끝까지 스크롤 다운 (마우스 이동 효과)
                time.sleep(SLEEP_TIME)  #대기

                new_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 다운 후 스크롤 높이 다시 가져옴

                # read & parser
                html1 = html1 + driver.page_source

                ######################## 파일 저장
                title_file = open(fileList[location], 'w', encoding='UTF8')
                title_file.write(html1)
                title_file.close()

        title_file = open(fileList[location], 'r', encoding='UTF8')
        print("-----------------------------------------------------")

        while True:
            # print("run reading")
            line = title_file.readline()
            readString = readString + line
            if not line: break
        title_file.close()

        print("location: {0}", location)
        # print(readString)
        soup = BeautifulSoup(readString, 'html.parser')
        # print(soup)

        # Extract the desired information
        titleList = list()
        dataList = list()
        descList = list()

        #title
        h4_elements = soup.find_all('h4', class_='titles')
        print("title length: %d" % len(h4_elements))

        for i in range(0, len(h4_elements)):
            titleList.append(h4_elements[i].text)

        # #data and time
        span_elements = soup.find_all('span', class_='byline')
        print("span_elements: %d" % len(span_elements))

        for i in range(0, len(span_elements)):
             dataList.append(span_elements[i].text)

        # #description
        # desc_elements = soup.find_all('p', class_='lead line-6x2')
        # for i in range(0, len(desc_elements)):
        #      descList.append(desc_elements[i].text)

        data = {
            'Data' : dataList,
            'Title': titleList,
            # 'desc' : descList,
            'Year': dataList,
            'Month': dataList,
            'Date': dataList,
        }

        # pd.set_option("display.max.colwidth", 200)
        CrawlDf = pd.DataFrame(data)

        # Time 전처리
        # slice를 이용하여 연/월/일/시간으로 분리
        import re
        for i in range(0, len(CrawlDf['Title'])):
            # OilDataFrame['Time'][i] = re.sub(r'[at]', ' ', OilDataFrame['Time'][i])
            CrawlDf['Year'][i] = CrawlDf['Data'][i][-17:-13]
            CrawlDf['Month'][i] = CrawlDf['Data'][i][-12:-10]
            CrawlDf['Date'][i] = CrawlDf['Data'][i][-8:-6]

        print(CrawlDf['Year'].unique())
        print(CrawlDf['Month'].unique())
        print(CrawlDf['Date'].unique())
        #print(CrawlDf['Year'])

        if selyear == 0:
            SelCrawDf = CrawlDf
        else:
            print("Sel year:%d"%selyear)
            SelCrawDf = CrawlDf[CrawlDf['Year'] == '%d'%selyear]
            print(SelCrawDf.head(6))
            print(SelCrawDf['Year'].unique())
            SelCrawDf = SelCrawDf.reset_index()
            print(SelCrawDf.head(5))
        if IsWordCloud:
            wordCloud(SelCrawDf, location, selyear)
        else:
            make_top_word_graph(location, SelCrawDf, MAX_WORD, selyear)
        print("Finish")
        return

    elif location == 2:
        print("버튼 위치로 이동시 버튼이 보이지 않는 오류를 해결하기 위해 크롬 보기를 축소시켜야함")
        print("크롬 설정 모양- 확대설정 65% 이하")
        print("enter %d"%location)

        # 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
        readString = ""
        html1 = ""

        if Crawling == "true":
            print("start crawling")
            driver = webdriver.Chrome()
            urlGoogle = "https://www.google.com"
            driver.get(urlGoogle)
            driver = webdriver.Chrome()

            driver.get(url[location])
            print(url[location])

            last_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 높이 가져옴
            print("[0]last_height:", last_height)
            new_height = 0
            count = 0
            print("count:", count)

            while True:
                try:
                    # 브라우저를 최대 20초까지 기다린다. (xpath의 값이 나올때까지)
                    elem = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="tc-main-content"]/div[3]/div/div/button/span'))
                    )

                    # id가 something 인 element 를 찾음
                    target_location = driver.find_element(By.XPATH, '//*[@id="tc-main-content"]/div[3]/div/div/button/span')
                    print("target_location: ", target_location)
                    driver.execute_script("arguments[0].scrollIntoView();", target_location)

                    new_height = driver.execute_script("return document.body.scrollHeight")     # 스크롤 다운 후 스크롤 높이 다시 가져옴
                    print("[0]new_height:", new_height)

                    # "Next" 버튼 클릭
                    print("run next page")
                    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div[3]/div/div/button/span").click()
                    count = count + 1

                    if count == GLOBAL_MAX:
                        # read & parser
                        html1 = driver.page_source

                        title_file = open(fileList[location], 'w', encoding='UTF8')  ######################## 파일 저장
                        title_file.write(html1)
                        title_file.close()
                        break
                except:
                    print("continue")
                    time.sleep(SLEEP_TIME)  # 대기

        title_file = open(fileList[location], 'r', encoding='UTF8')
        print("-----------------------------------------------------")

        while True:
            # print("run reading")
            line = title_file.readline()
            readString = readString + line
            if not line: break
        title_file.close()

        print("location: {0}", location)

        # Extract the desired information
        titleList = list()
        TimeList = list()
        descList = list()
        MonthList = list()

        # BeautifulSoup을 사용하여 제목 추출
        soup = BeautifulSoup(readString, 'html.parser')
        # print(soup)
        title_element = soup.select("h2.post-block__title > a.post-block__title__link")

        for title in title_element:
            titleList.append(title.text)
        print("titleList length: ", len(titleList))

        date_element = soup.select("time.river-byline__full-date-time")

        import re

        for date in date_element:
            TimeList.append(date.text)

            string = date.text.split("•")
            #print(string)
            # string[1] = re.sub('[^A-Za-z]', '', string[1])
            string[1] = re.sub('[^A-Za-z]', '', string[1])
            #print(string[1])
            MonthList.append(string[1])
        print("TimeList length: ", len(TimeList))

        content_element = soup.select("div.post-block__content")
        for content in content_element:
            descList.append(date.text)
        print("descList length: ", len(descList))

        data = {
            'Title': titleList,
            'Time' : TimeList,
            'Year' : TimeList,
            'Month': MonthList,
            'Date': TimeList,
            'description' : descList,
        }

        pd.set_option("display.max.colwidth", 200)
        CrawlDf = pd.DataFrame(data)

        # Time 전처리
        # slice를 이용하여 연/월/일/시간으로 분리
        for i in range(0, len(CrawlDf['Date'])):
            CrawlDf['Year'][i] = CrawlDf['Time'][i][-4:]
            CrawlDf['Date'][i] = CrawlDf['Time'][i][-8:-6]

        if selyear == 0:
            SelCrawDf = CrawlDf
        else:
            print("Sel year:%d"%selyear)
            SelCrawDf = CrawlDf[CrawlDf['Year'] == '%d'%selyear]
            print(SelCrawDf.head(6))
            print(SelCrawDf['Year'].unique())
            SelCrawDf = SelCrawDf.reset_index()
            print(SelCrawDf.head(5))
        if IsWordCloud:
            wordCloud(SelCrawDf, location, selyear)
        else:
            make_top_word_graph(location, SelCrawDf, MAX_WORD, selyear)
        print("Finish")
        return

    elif location == 3:
        print("버튼 위치로 이동시 버튼이 보이지 않는 오류를 해결하기 위해 크롬 보기를 축소시켜야함")
        print("크롬 설정 모양- 확대설정 65% 이하")
        print("enter %d"%location)

        # 웹페이지의 끝 지점까지 지정하여 스크래핑 (계속)
        readString = ""
        html1 = ""

        if Crawling == "true":
            print("start crawling")
            driver = webdriver.Chrome()
            urlGoogle = "https://www.google.com"
            driver.get(urlGoogle)
            driver = webdriver.Chrome()

            driver.get(url[location])
            print(url[location])

            last_height = driver.execute_script("return document.body.scrollHeight")  # 스크롤 높이 가져옴
            print("[0]last_height:", last_height)
            new_height = 0
            count = 0
            print("count:", count)
            btnNumber = 0

            while True:
                try:
                    # More Articles 버튼을 찾기 위한 XPath
                    button_xpath = "//button[@data-testid='variants']"

                    # More Articles 버튼 요소 찾기
                    button_element = driver.find_element(By.XPATH, button_xpath)

                    # JavaScript를 사용하여 해당 요소까지 스크롤
                    driver.execute_script("arguments[0].scrollIntoView();", button_element)

                    # 버튼을 클릭하기 위해 ActionChains 사용
                    actions = ActionChains(driver)
                    actions.move_to_element(button_element).click().perform()

                    new_height = driver.execute_script("return document.body.scrollHeight")     # 스크롤 다운 후 스크롤 높이 다시 가져옴
                    #print("[0]new_height:", new_height)

                    count = count + 1
                    print("count:", count)

                    if count == GLOBAL_MAX:
                        # read & parser
                        html1 = driver.page_source
                        title_file = open(fileList[location], 'w', encoding='UTF8')  ######################## 파일 저장
                        title_file.write(html1)
                        title_file.close()
                        break
                except:
                    print("continue")
                    time.sleep(SLEEP_TIME)  # 대기

        title_file = open(fileList[location], 'r', encoding='UTF8')
        print("-----------------------------------------------------")

        while True:
            # print("run reading")
            line = title_file.readline()
            readString = readString + line
            if not line: break
        title_file.close()

        print("location: {0}", location)

        # Extract the desired information
        titleList = list()
        TimeList = list()
        descList = list()

        # BeautifulSoup을 사용하여 제목 추출
        soup = BeautifulSoup(readString, 'html.parser')
        # print(soup)
        title_element = soup.select("p.A7hAxSNa > span.ULACyEdG")

        for title in title_element:
            titleList.append(title.text)
        print("titleList length: ", len(titleList))

        contents = soup.select("p.A7hAxSNa > span.ULACyEdG")
        # print(contents[0])
        # print(contents[0].text)
        # print(len(contents))
        for i in range(0, len(contents)):
            descList.append(contents[i].text)
        print("descList length: ", len(descList))

        date_element = soup.select("div.B6j66vzQ > div.ptbNeM0K")
        # print(date_element)
        # print("date_element: ", date_element[0].text)
        for date in date_element:
            TimeList.append(date.text)
        print("TimeList length: ", len(TimeList))

        data = {
            'Title': titleList,
            'Time' : TimeList,
            'Year' : TimeList,
            'Month': TimeList,
            'Date': TimeList,
            'description' : descList,
        }

        pd.set_option("display.max.colwidth", 20)
        CrawlDf = pd.DataFrame(data)

        # Time 전처리
        # slice를 이용하여 연/월/일/시간으로 분리
        for i in range(0, len(CrawlDf['Time'])):
            CrawlDf['Year'][i] = CrawlDf['Time'][i][-4:]
            CrawlDf['Date'][i] = CrawlDf['Time'][i][4:6]
            CrawlDf['Month'][i] = CrawlDf['Time'][i][ :3]

        print("Sel 2020:")
        print(CrawlDf[CrawlDf['Year'] == '%d'%2020])
        # print(CrawlDf.head(6))
        # print(CrawlDf['Year'].head(6))
        # print(CrawlDf['Month'].head(6))
        # print(CrawlDf['Date'].head(6))
        # print(CrawlDf['Year'].unique())

        if selyear == 0:
            SelCrawDf = CrawlDf
        else:
            print("Sel year:%d"%selyear)
            SelCrawDf = CrawlDf[CrawlDf['Year'] == '%d'%selyear]
            print(SelCrawDf.head(6))
            print(SelCrawDf['Year'].unique())
            SelCrawDf = SelCrawDf.reset_index()
            print(SelCrawDf.head(5))
        if IsWordCloud:
            wordCloud(SelCrawDf, location, selyear)
        else:
            make_top_word_graph(location, SelCrawDf, MAX_WORD, selyear)
        print("Finish")
        return

# make noun frequency graph per religion
def make_top_word_graph(location, result, top, selyear):
    print("top type: ", type(top))
    if location == 3 or location == 2:
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        stop_words = set(stopwords.words('english'))
        print("stop_words length: ", len(stop_words))

        #불용어 사전 다운로드 from 사이킷런
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words
        # len(sklearn_stop_words)  # 318
        # len(set(stop_words).union(set(sklearn_stop_words)))  # 합집합 개수
        stopwords = set(stop_words).union(set(sklearn_stop_words))
        # print("stopwords: ", stopwords)
        print("union stop_words length: ", len(stopwords))
        # print(result.head(6))
        print(result.head(3))
        # print(len(result['Title'][0]))
        # print(result['Title'][0])
        wordString = ""

        for i in range(0, len(result['Title'])):
            wordString = wordString + result['Title'][i]

        # print(wordString)
        letters_only = re.sub('[^a-zA-Z0-9]', ' ', wordString)
        words = letters_only.lower().split()
        meaningful_words = [w for w in words if not w in stopwords]
        # print("meaningful_words: ", meaningful_words)

        word_count = dict()
        for word in meaningful_words:
            word_count[word] = word_count.get(word, 0) + 1

        sorted_word_count = sorted(word_count, key=word_count.get, reverse=True)

        n = sorted_word_count[:top][::-1]   # 지정된 단어 갯수 추출
        w = [word_count[key] for key in n] # 추출된 단어에 대해 빈도를 추출
        bar = plt.barh(range(len(n)), w, tick_label=n)  # 수평 막대그래프

        # 각 막대에 값(데이터) 추가
        for i, v in enumerate(w):
            plt.text(v, i, str(v), va='center', fontsize=8, fontweight='bold')

        # 그래프 제목 및 축 레이블 설정 (선택 사항)
        plt.title('Horizontal Bar Chart with Values')
        plt.xlabel('Count')
        plt.subplots_adjust(left=0.2)  # 왼쪽 여백을 조절
        plt.savefig("%d_"%location + '%d_'%selyear + 'top-word-graph.png', dpi=400, pad_inches= 2)

        # 단어 빈도 추출
        # Counter(word_count).most_common(top)
    else:
        stringConCat = ''.join(result['Title'])
        tokens = stringConCat.split(" ")  # 문자열을 공백 기준으로 구분
        text = nltk.Text(tokens)  # nltk

        #-------------------------------------
        # 한글 불용어 처리
        title_file = open("stopwords.txt", 'r', encoding='UTF8')
        print("-----------------------------------------------------")
        readStops = list()
        while True:
            line = title_file.readline()
            readStops.append(line)
            if not line: break
        title_file.close()

        readStops.append('2022]')
        readStops.append('\'AI')
        readStops.append('위한')
        readStops.append('수')
        readStops.append(' ')
        readStops.append('AI로')
        readStops.append('2022')

        # 불용어 제거한 텍스트 생성
        filtered_text = nltk.Text([word for word in text if word not in readStops and len(word) >= 2])
        #---------------------------------------

        topWord = filtered_text.vocab().most_common(top)  # top n word

        count = MAX_WORD  # top word on graph
        xlist = [a[0] for a in topWord[:count]]
        ylist = [a[1] for a in topWord[:count]]

        plt.figure(0)
        # font_name = font_manager.FontProperties(fname='./font/font.ttf', size=7).get_name()
        # rc('font', family=font_name)  # 한글 적용
        # 폰트 경로 지정
        import matplotlib
        matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        matplotlib.rcParams['axes.unicode_minus'] = False

        plt.xlabel('Word')
        # plt.xticks(rotation=70)  # x축 라벨 회전
        plt.ylabel('Count')
        plt.title('keyword' + ' TOP ' + str(count) + ' WORD')
        plt.ylim([10, 1000])  # y축 범위 (최대값을 기준으로 동일하게 설정하기 위함)
        #plt.plot(xlist, ylist)

        # 각 막대 위에 값을 표기
        for i, v in enumerate(ylist):
            plt.text(xlist[i], v + 10, str(v), ha='center', va='bottom')

        plt.bar(xlist, ylist)

        plt.savefig("%d_"%location + '%d_'%selyear + 'top-word-graph.png', dpi=400, pad_inches= 2)
        # print("korean")
        # from konlpy.tag import Kkma
        # stringConCat = ''.join(result['Title'])
        # print(len(stringConCat))
        #
        # # 한글 불용어 처리
        # title_file = open("stopwords.txt", 'r', encoding='UTF8')
        # print("-----------------------------------------------------")
        # readStops = list()
        # while True:
        #     line = title_file.readline()
        #     readStops.append(line)
        #     if not line: break
        # title_file.close()
        # # readStops = ""
        # # while True:
        # #     # print("run reading")
        # #     line = title_file.readline()
        # #     readStops = readStops + line
        # #     if not line: break
        # # title_file.close()
        #
        # # Kkma 객체 생성
        # kkma = Kkma()
        #
        # # 명사 추출
        # title_nouns = kkma.nouns(stringConCat)
        #
        # # 불용어 제거 & 두 글자 이상의 명사 필터링
        # #filtered_nouns = [noun for noun in title_nouns if noun not in readStops and len(noun) >= 3]
        # filtered_nouns = [noun for noun in title_nouns if len(noun) >= 3]
        #
        # # # 빈도 계산
        # # noun_freq = Counter(filtered_nouns)
        # #
        # # # 상위 명사 10개 추출
        # # top_nouns = noun_freq.most_common(MAX_WORD)
        # # print(top_nouns)
        #
        # # 빈도 계산
        # noun_freq = Counter(filtered_nouns)
        #
        # # 상위 명사 10개 추출
        # top_nouns = noun_freq.most_common(MAX_WORD)
        # print(top_nouns)
        #
        # # 폰트 경로 지정
        # import matplotlib
        # matplotlib.rcParams['font.family'] = 'Malgun Gothic'
        # matplotlib.rcParams['axes.unicode_minus'] = False
        #
        # # 그래프 그리기
        # plt.figure(figsize=(10, 6))
        # plt.bar(range(len(top_nouns)), [count for _, count in top_nouns], tick_label=[noun for noun, _ in top_nouns])
        # plt.title('Top 10 Nouns (2 or more characters) in Text')
        # plt.xlabel('Noun')
        # plt.ylabel('Frequency')
        # plt.xticks(rotation=45)
        # # plt.show()
        # plt.subplots_adjust(left=0.2)  # 왼쪽 여백을 조절
        # plt.savefig("%d_"%location + '%d_'%selyear + 'top-word-graph.png', dpi=400, pad_inches= 2)
    return

######################## 실행 명령어
#CrawlingReadCloudFunc(1, "false", False, 2023)
CrawlingReadCloudFunc(1, "false", False, 2021)
#CrawlingReadCloudFunc(1, "false", False, 2021)
# CrawlingReadCloudFunc(2, "false", False, 2023)
# CrawlingReadCloudFunc(2, "false", True, 2023)
# CrawlingReadCloudFunc(3, "false", False, 2020)
# CrawlingReadCloudFunc(3, "false", True, 2020)


#######################jdk 관련 error 발생시 https://clsrn4561.tistory.com/1 참조