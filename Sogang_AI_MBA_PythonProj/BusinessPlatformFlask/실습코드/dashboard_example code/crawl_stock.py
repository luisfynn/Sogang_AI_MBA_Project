import requests
from bs4 import BeautifulSoup


def get_daily_stock_prices():
    url = "https://finance.naver.com/item/sise_day.nhn?"

    params = {
        "code": '005380',
        "page": 1,
    }

    raw = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    html = BeautifulSoup(raw.text, "html.parser")

    tr_list = html.body.find_all(name='tr', attrs={'onmouseover':'mouseOver(this)'})

    price_list = []
    for tr in tr_list:
        price_list.append([td.span.string.strip() for td in tr.find_all(name='td')])

    daily_price_list = [{"date": price[0], "price": price[1]} for price in price_list]

    return daily_price_list


def get_today_price(code):
    url = "https://finance.naver.com/item/sise_day.nhn?"

    params = {
        "code": code,
        "page": 1,
    }

    raw = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    html = BeautifulSoup(raw.text, "html.parser")

    tr_list = html.body.find_all(name='tr', attrs={'onmouseover': 'mouseOver(this)'})

    price_list = []
    for tr in tr_list:
        price_list.append([td.span.string.strip() for td in tr.find_all(name='td')])

    today_price = price_list[0]

    today_price_dict = {
        "price": today_price[3],
        "top_price": today_price[4],
        "lowest_price": today_price[5],
        "volume": today_price[6]
    }

    return today_price_dict
