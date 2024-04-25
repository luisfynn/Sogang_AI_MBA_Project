import requests
from bs4 import BeautifulSoup


def get_news_list(company):
    url = "https://search.naver.com/search.naver?"

    headers = {'User-Agent': 'Mozilla/5.0'}
    raw = requests.get("https://search.naver.com/search.naver?query=" + company + "&where=news&ie=utf8&sm=nws_hty", headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, "html.parser")


    titles_tags = html.select(".news_tit")
    descriptions_tags = html.select(".api_txt_lines")

    titles = [titles_tag["title"] for titles_tag in titles_tags]
    hrefs = [titles_tag["href"] for titles_tag in titles_tags]
    descriptions = [descriptions_tag.text for descriptions_tag in descriptions_tags]

    news_list = zip(titles, hrefs, descriptions)

    news_dict_list = []
    for news in news_list:
        news_dict = {
            "title": news[0],
            "url": news[1],
            "description": news[2]
        }

        news_dict_list.append(news_dict)

    return news_dict_list

