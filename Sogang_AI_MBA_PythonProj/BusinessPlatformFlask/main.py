from flask import Flask, render_template, jsonify
from crawl.crawl_stock import get_today_price, get_daily_stock_prices
from crawl.crawl_news import get_news_list
from crawl.crawl_bitcoin import get_bitcoin_price
from crawl.crawl_us_stock import get_us_stock_price
from crawl.crawl_weather import get_weather_info
import requests

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

@app.route('/')
def dashboard():
    hyundai_price = get_today_price('005380')
    company1_stock = {'title': "현대자동차", "today_price": hyundai_price}
    company1_news_list = get_news_list("현대자동차")

    shinsegae_price = get_today_price('004170')
    company2_stock = {'title': "신세계", "today_price": shinsegae_price}
    company2_news_list = get_news_list("신세계")

    us_stock_price = {'title': "tesla", 'today_price': get_us_stock_price('tesla')}
    bitcoin_price = get_bitcoin_price()

    weather_info = get_weather_info()

    return render_template('index.html',
                           company1_stock=company1_stock,
                           company1_news_list=company1_news_list,
                           company2_stock=company2_stock,
                           company2_news_list=company2_news_list,
                           us_stock_price=us_stock_price,
                           bitcoin_price=bitcoin_price,
                           weather_info=weather_info
                           )


@app.route('/weather_forecast')
def get_weather_forecast_info():
    result = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=37.413294&lon=126.734086&exclude=current,minutely,hourly,alerts&appid=3c9021aa10b48b8251d6555460a9f989&units=metric')
    json_result = result.json()
    print(type(json_result))
    print(type(json_result['daily']))
    return jsonify(json_result['daily'])


@app.route('/daily_prices')
def get_daily_prices():
    daily_price_list = get_daily_stock_prices()
    print(type(daily_price_list))
    return jsonify(daily_price_list)

import quandl
import datetime

def get_camping_sites(api_key, latitude, longitude):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {
        "query": "캠핑장",
        "y": latitude,
        "x": longitude,
        "radius": 15000,
        "sort": "distance"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()['documents'][:10]

@app.route('/line')
def camping_sites():
    api_key = '9ed5f80886ee41609fe7650e7d5431ad'
    # 서울 시청 기준 좌표
    latitude = '37.5665'
    longitude = '126.9780'
    sites = get_camping_sites(api_key, latitude, longitude)
    places = ['x']
    distances = ['Distance to Camping Sites']
    for site in sites:
        places.append(site['place_name'])
        distances.append(site['distance'])
    return jsonify([places, distances])



# @app.route('/line')
# def get_line_chart_data():
#     quandl.ApiConfig.api_key = "mFJ-d-Lj4n2fvywxg_DN"  # 여기에 실제 API 키를 넣으세요.
#
#     # 오늘 날짜와 7일 전 날짜 계산
#     end_date = datetime.date.today()
#     start_date = end_date - datetime.timedelta(days=7)
#
#     # Quandl에서 데이터 가져오기
#     data = quandl.get("WIKI/AAPL", start_date=start_date, end_date=end_date)
#
#     # 데이터를 리스트로 변환하여 차트에 사용할 수 있게 함
#     # 예를 들어 'Close' 가격만 사용한다고 가정
#     prices = data['Close'].tolist()
#     dates = data.index.strftime('%Y-%m-%d').tolist()
#     return jsonify([dates, prices])

# @app.route('/line')
# def get_line_chart_data():
#     # Quandl API 키 설정
#     quandl.ApiConfig.api_key = "mFJ-d-Lj4n2fvywxg_DN"
#
#     # 오늘 날짜와 7일 전 날짜 계산
#     end_date = datetime.date.today()
#     start_date = end_date - datetime.timedelta(days=7)
#
#     # 데이터 가져오기
#     data = quandl.get("WIKI/AAPL", start_date=start_date, end_date=end_date)
#     # return jsonify(['data1', 30, 200, 100, 400, 150, 250])
#     return jsonify(['data1', data])


@app.route('/pie')
def get_pie_chart_data():
    return jsonify([['A', 30], ['B', 50], ['C', 20]])


if __name__ == '__main__':
    app.run()
