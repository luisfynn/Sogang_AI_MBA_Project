from flask import Flask, render_template, jsonify, request
from crawl.crawl_stock import get_daily_stock_prices
from crawl.crawl_news import get_news_list
import json
import requests
import xmltodict
import pandas as pd

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )

@app.route('/')
def dashboard():
    news_list = get_news_list("부동산")
    return render_template('index.html',company1_news_list=news_list)

########################################################################################################################
serviceKey = "r366v2G%2BVbUTB2DXIusTs%2BI5xgtb3Kfhsa2jvFf74TIGkhmUwrKzNI5SZL04S%2BnMdfEQFLbNoXl7r2tKyP0VWQ%3D%3D"
########################################################################################################################
# 서대문구
def get_df(lawd_cd, deal_ymd):
    global serviceKey
    base_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?serviceKey=" + serviceKey
    base_url += f'&LAWD_CD={lawd_cd}'
    base_url += f'&DEAL_YMD={deal_ymd}'

    res = requests.get(base_url)
    data = json.loads(json.dumps(xmltodict.parse(res.text)))
    df = pd.DataFrame(data['response']['body']['items']['item'])
    return df

def realPrice():
    # base_date = "2024.04"  # 필요한 데이터의 연도 + 월
    # gu_code = '11410'  # 법정동 코드의 앞자리 5글자만 입력하면 법정 구코드가 됨. 예시는 서대문구 천연동
    df = get_df(11410, 202404)  # 서대문구 2024.04월 실거래가 조회
    return df

@app.route('/boxChart')
def box_chart():
    df = realPrice()  # Ensure this function returns a DataFrame with a '거래금액' column
    df['거래금액'] = df['거래금액'].str.replace(',', '').astype(float)

    # Define bin edges
    bin_edges = [0, 50000, 100000, 150000, 200000]  # Modify as necessary for your data range

    # Bin the data
    bins = pd.cut(df['거래금액'], bins=bin_edges, right=False)  # right=False makes intervals left-inclusive
    bin_counts = bins.value_counts().sort_index()

    # Prepare response data with bin intervals as strings
    response_data = [{'bin': f"{int(bin.left)}-{int(bin.right)-1}", 'count': count} for bin, count in bin_counts.items()]
    return jsonify(response_data)

@app.route('/pieChart')
def pie_chart():
    df = realPrice()
    df['법정동_카테고리'] = df['법정동'].astype('category')
    counts = df['법정동_카테고리'].value_counts()

    # 데이터 전달
    formatted_data = [[district, count] for district, count in zip(counts.index.tolist(), counts.values.tolist())]
    print(f"Formatted Data for C3: {formatted_data}")
    return jsonify(formatted_data)

@app.route('/timeSeries')
def time_series():
    df = realPrice()
    # df['일'] = pd.to_datetime(df['일'], format='%d')
    # df_sorted = df.sort_values(by='일', ascending=True)
    # counts = df_sorted.groupby('일')['년'].count()
    # dates = df_sorted['일'].dt.strftime('%Y-%m-%d').unique().tolist()
    # data = [['x'] + dates, ['Transactions'] + counts.tolist()]

    df['일'] = pd.to_datetime('2024-04-' + df['일'].astype(str), format='%Y-%m-%d')
    df_sorted = df.sort_values(by='일', ascending=True)
    counts = df_sorted.groupby(df_sorted['일'].dt.strftime('%Y-%m-%d'))['년'].count()
    dates = counts.index.tolist()
    data = [['x'] + dates, ['Transactions'] + counts.tolist()]
    print(data)
    return jsonify(data)

########################################################################################################################
# 강남구
def get_df1(lawd_cd, deal_ymd):
    global serviceKey
    base_url = "http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?serviceKey=" + serviceKey
    base_url += f'&LAWD_CD={lawd_cd}'
    base_url += f'&DEAL_YMD={deal_ymd}'

    res = requests.get(base_url)
    data = json.loads(json.dumps(xmltodict.parse(res.text)))
    df = pd.DataFrame(data['response']['body']['items']['item'])
    return df

def realPrice1():
    # base_date = "2024.04"  # 필요한 데이터의 연도 + 월
    # gu_code = '11680'  # 강남구 법정동코드
    df = get_df1(11680, 202404)  # 강남구 2024.04월 실거래가 조회
    return df

@app.route('/boxChart1')
def box_chart1():
    df = realPrice1()  # Ensure this function returns a DataFrame with a '거래금액' column
    df['거래금액'] = df['거래금액'].str.replace(',', '').astype(float)

    # Define bin edges
    bin_edges = [0, 50000, 100000, 150000, 200000]  # Modify as necessary for your data range

    # Bin the data
    bins = pd.cut(df['거래금액'], bins=bin_edges, right=False)  # right=False makes intervals left-inclusive
    bin_counts = bins.value_counts().sort_index()

    # Prepare response data with bin intervals as strings
    response_data = [{'bin': f"{int(bin.left)}-{int(bin.right)-1}", 'count': count} for bin, count in bin_counts.items()]
    return jsonify(response_data)

@app.route('/pieChart1')
def pie_chart1():
    df = realPrice1()
    df['법정동_카테고리'] = df['법정동'].astype('category')
    counts = df['법정동_카테고리'].value_counts()

    # 데이터 전달
    formatted_data = [[district, count] for district, count in zip(counts.index.tolist(), counts.values.tolist())]
    print(f"Formatted Data for C3: {formatted_data}")
    return jsonify(formatted_data)

@app.route('/timeSeries1')
def time_series1():
    df = realPrice1()
    # df['일'] = pd.to_datetime(df['일'], format='%d')
    # df_sorted = df.sort_values(by='일', ascending=True)
    # counts = df_sorted.groupby('일')['년'].count()
    # dates = df_sorted['일'].dt.strftime('%d').unique().tolist()
    # dates = "2024-04"+dates
    # dates.strfttime('%Y-%m-%d')
    # data = [['x'] + dates, ['Transactions'] + counts.tolist()]

    df['일'] = pd.to_datetime('2024-04-' + df['일'].astype(str), format='%Y-%m-%d')
    df_sorted = df.sort_values(by='일', ascending=True)
    counts = df_sorted.groupby(df_sorted['일'].dt.strftime('%Y-%m-%d'))['년'].count()
    dates = counts.index.tolist()
    data = [['x'] + dates, ['Transactions'] + counts.tolist()]
    print(data)
    return jsonify(data)
########################################################################################################################

if __name__ == '__main__':
    app.run()
