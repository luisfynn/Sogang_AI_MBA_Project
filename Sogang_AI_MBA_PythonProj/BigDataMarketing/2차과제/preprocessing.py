import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 처리
from matplotlib import font_manager, rc
font_path = "c:/windows/Fonts/malgun.ttf" #한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family = font_name)

# load data
df = pd.read_csv("C:\\Users\\luisf\\OneDrive\\바탕 화면\\WorkSpace\\Sogang_AI_MBA_Project\\Sogang_AI_MBA_PythonProj\\BigDataMarketing\\2차과제\\분석\\1차 취합 및 분석\\combined_df_date수정.csv")
# print(df.head())
# data column 확인
print(df.columns)

# order list 종류 및 개수 확인
# for items in df['order_items'].unique():
#     print(items)

# 'region' 열을 기준으로 그룹화하고, 특정 열들의 NaN을 제외한 값을 하나의 리스트로 묶기
grouped_df = df.groupby('region').apply(
    lambda x: x[['order_세분화1', 'order_세분화2', 'order_세분화3',
                 'order_세분화4', 'order_세분화5', 'order_세분화6',
                 'order_세분화7']].apply(lambda row: [item for item in row if pd.notna(item)], axis=1).sum()
).reset_index(name='CombinedData')


print(grouped_df['CombinedData'])
print(grouped_df['region'])
newlist = []
for value in grouped_df['CombinedData']:
    for data in value:
        newlist.append(data)

print(set(newlist))
# {'크리스피', ' 콤보', '빠삭', '크크크', ' 육육', '짜장', '후라이드', '골뱅이무침', ' 고추', ' 더매운고추', ' 장스', ' 크리스피', '고추', ' 양념',
# '장스', '호랑이', ' 사이드', '크랑이', '간지', '6초', ' 푸하핫', ' 크크크', ' 짜장', '양념', ' 골뱅이무침', ' 크랑이',
# ' 6초', ' 호랑이', '사이드', '하하핫', '육육', ' 하하핫', ' ', ' 간지', ' 빠삭', '반마리 + 반마리'}

# 공백 제거
cleaned_data = {item.strip() for item in newlist}
print(f"cleaned_data:{cleaned_data}")

# 맛별로 리스트 할당
# 임의로 할당
flavors = {
    'spicy': ['고추', '더매운고추', '크랑이', ' 크랑이', '하하핫', ' 하하핫', '호랑이', ' 호랑이', ' 고추', ' 더매운고추', '푸하핫', ' 양념', '6초', ' 6초', '육육', ' 육육'],
    'sweet': ['양념', '장스', ' 장스', '짜장', ' 짜장'],
    'normal' :['후라이드'],
    'crispy': ['크리스피', '빠삭', ' 빠삭', '크크크'],
    'unique': ['간지', ' 간지', '반마리 + 반마리', '콤보', ' 콤보'],
    'etc' : ['골뱅이무침', ' 골뱅이무침', '사이드', ' 사이드']
}

# 각 맛별로 할당된 아이템을 리스트에 저장
flavor_lists = {key: [] for key in flavors}  # 각 맛별로 빈 리스트 생성

for item in cleaned_data:
    for flavor, items in flavors.items():
        if item in items:
            flavor_lists[flavor].append(item)

print(f"flavor_lists:{flavor_lists}")

#######################################################################################################################
# 각 맛별로 매칭되는 아이템을 검색하여 맛 리스트를 생성
# 지역명 데이터
regions = [
    "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구", "도봉구",
    "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구", "양천구", "영등포구",
    "용산구", "은평구", "종로구", "중구", "중랑구"
]

# 맛 분류
flavor_lists = {
    'spicy': ['더매운고추', '하하핫', '크랑이', '호랑이', '육육', '푸하핫', '고추', '6초'],
    'sweet': ['양념', '장스', '짜장'],
    'normal': ['후라이드'],
    'crispy': ['빠삭', '크크크', '크리스피'],
    'unique': ['간지', '콤보', '반마리 + 반마리'],
    'etc': ['사이드', '골뱅이무침']
}

# 각 행의 맛 카테고리 카운트
results = []
for row in grouped_df['CombinedData']:
    count = {key: 0 for key in flavor_lists}
    for item in row:
        for flavor, items in flavor_lists.items():
            if item in items:
                count[flavor] += 1
                break
    results.append(count)

import matplotlib.pyplot as plt
import numpy as np

# 지정된 맛 분류에 따라서 데이터의 각 행을 처리하고 파이 차트 그리기
for i in range(0, len(results), 3):  # 3개씩 건너뛰면서 반복
    fig, axs = plt.subplots(1, 3, figsize=(14, 14))  # 한 행에 3개의 차트를 배치
    for j, ax in enumerate(axs):
        if i + j < len(results):  # 결과 리스트의 범위를 벗어나지 않도록 체크
            result = results[i + j]
            labels = list(result.keys())
            sizes = list(result.values())
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.set_title(regions[i + j])  # 지역 이름으로 제목 설정
        else:
            ax.axis('off')  # 추가 차트 공간 비활성화

    plt.tight_layout()
    # 파일 이름 설정
    plt.savefig(f'pie_charts_row_{i // 3 + 1}.png', dpi=300, bbox_inches='tight')
    plt.close(fig)  # 저장 후 차트 닫기



# # 각 지역별로 맛의 분포를 파이 차트로 그리고 저장하는 함수
# def plot_pie_charts(dataframe, region_column, flavor_column):
#     regions = dataframe[region_column].unique()
#     for region in regions:
#         # 특정 지역에 대한 데이터 추출
#         region_data = dataframe[dataframe[region_column] == region]
#
#         # 맛 카테고리별 카운트
#         flavor_counts = region_data[flavor_column].explode().value_counts()
#
#         # 데이터가 없는 경우 스킵
#         if flavor_counts.empty:
#             continue
#
#         # 파이 차트 그리기
#         plt.figure(figsize=(8, 8))
#         plt.pie(flavor_counts, labels=flavor_counts.index, autopct='%1.1f%%', startangle=140)
#         plt.title(f'Pie Chart for {region}')
#
#         # 파일로 저장
#         plt.savefig(f'{region}_pie_chart.png')
#         plt.close()
#
# # 파이 차트 그리기 및 저장
# plot_pie_charts(df, 'region', '순살 여부')