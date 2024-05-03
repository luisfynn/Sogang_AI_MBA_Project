from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_news_list(company):
    url = f"https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query={company}"

    # Chrome WebDriver 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저를 표시하지 않고 백그라운드에서 실행
    chrome_options.add_argument("--no-sandbox")  # 보안 설정
    chrome_options.add_argument("--disable-dev-shm-usage")  # 보안 설정

    # Selenium을 사용하여 브라우저 시뮬레이션 실행
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        html = driver.page_source

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(html, "html.parser")

    # 뉴스 제목과 링크 추출
    titles_tags = soup.select(".news_tit")
    hrefs = [titles_tag["href"] for titles_tag in titles_tags]
    titles = [titles_tag.text for titles_tag in titles_tags]

    # 뉴스 설명 추출
    descriptions_tags = soup.select(".api_txt_lines")
    descriptions = [descriptions_tag.text for descriptions_tag in descriptions_tags]

    # 뉴스 데이터를 딕셔너리로 구성
    news_dict_list = []
    for title, href, description in zip(titles, hrefs, descriptions):
        news_dict = {
            "title": title,
            "url": href,
            "description": description
        }
        news_dict_list.append(news_dict)

    return news_dict_list