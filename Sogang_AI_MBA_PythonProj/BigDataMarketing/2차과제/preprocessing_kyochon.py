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
df = pd.read_csv("C:\\Users\\luisf\\OneDrive\\바탕 화면\\WorkSpace\\Sogang_AI_MBA_Project\\Sogang_AI_MBA_PythonProj\\BigDataMarketing\\2차과제\\분석\\1차 취합 및 분석\\마포구 브랜드별 비교\\브랜드비교_마포구_교촌.csv")
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
                 'order_세분화7','order_세분화7']].apply(lambda row: [item for item in row if pd.notna(item)], axis=1).sum()
).reset_index(name='CombinedData')


print(grouped_df['CombinedData'])
print(grouped_df['region'])
newlist = []
for value in grouped_df['CombinedData']:
    for data in value:
        newlist.append(data)

# print(set(newlist))
# {'레드윙', ' 허니사이드', ' 시그니처세트', ' 소이살살', '허니점보윙', ' 라이스세트', ' 반반점보윙', '시그니처순살세트',
# '블랙시크릿오리지날', '반반윙', ' 허니점보윙', '신화순살', '시그니처세트', '허니순살', '신화오리지날', '반반순살',
# '레블반반콤보', '윙', '블랙시크릿순살', '순살', ' 블랙시크릿콤보', ' 레드순살', ' 콤보', ' 순살', ' 오리지날',
# ' 통통치킨카츠', '리얼후라이드', ' 레드윙', ' 레드점보윙', '반반콤보', ' 허니순살', '치즈트러플순살',
# ' 리얼후라이드', '허니오리지날', ' 발사믹치킨', ' 레드사이드', '발사믹치킨', ' 반반순살', ' 윙', '오리지날',
# ' 신화순살', '순살후라이드', ' 레드오리지날', '블랙치밥세트', ' 레드콤보', ' 반반사이드', ' 살살후라이드', '점보윙',
# '통통치킨카츠', '#VALUE!', '사이드', '살살후라이드', '허니콤보', '레드점보윙', '레드순살', '방콕점보윙', '응원팩',
# ' 치즈트러플순살', ' 신화오리지날', ' 사이드', '살살치킨', ' 리얼치킨버거', '블랙시크릿콤보', '레드콤보', '반반점보윙',
# ' 반반콤보', ' 반반오리지날', ' 후라이드', ' 블랙시크릿순살', '콤보', ' 반반윙', ' 허니콤보', ' 블랙시크릿오리지날', '레드사이드',
# '반반오리지날', '레드오리지날', '반반사이드', '허니사이드', ' 살살치킨', '윙후라이드', '소이살살', '라이스세트', '후라이드', ' 레허반반순살',
# ' 레블반반콤보', ' 허니오리지날', '레허반반순살', ' 방콕점보윙'}

# # 공백 제거
cleaned_data = {item.strip() for item in newlist}
print(f"cleaned_data:{cleaned_data}")
# cleaned_data:{'살살후라이드', '라이스세트', '후라이드', '반반사이드', '레드순살', '윙', '콤보', '리얼치킨버거', '점보윙',
#               '블랙치밥세트', '레드윙', '반반순살', '허니순살', '순살후라이드', '반반윙', '반반오리지날', '허니사이드',
#               '허니점보윙', '반반콤보', '치즈트러플순살', '시그니처순살세트', '사이드', '리얼후라이드', '통통치킨카츠',
#               '신화순살', '레허반반순살', '레드콤보', '윙후라이드', '블랙시크릿순살', '블랙시크릿오리지날', '레블반반콤보',
#               '발사믹치킨', '순살', '블랙시크릿콤보', '시그니처세트', '허니오리지날', '레드사이드', '오리지날', '신화오리지날',
#               '소이살살', '반반점보윙', '방콕점보윙', '살살치킨', '응원팩', '#VALUE!', '허니콤보', '레드오리지날', '레드점보윙'}



# 맛별로 리스트 할당
# 임의로 할당
flavors = {
    'spicy': ['레드순살', '레드윙', '신화순살', '레드콤보', '블랙시크릿순살', '블랙시크릿오리지날', '블랙시크릿콤보', '레드사이드', '신화오리지날', '레드오리지날', '레드점보윙'],
    'sweet': ['허니순살', '허니점보윙', '치즈트러플순살', '발사믹치킨', '허니오리지날', '소이살살', '허니콤보'],
    'normal' :['살살후라이드', '후라이드', '순살후라이드', '리얼후라이드', '윙후라이드', '순살', '오리지날', '살살치킨'],
    'unique': ['윙', '콤보', '반반순살','반반윙', '반반오리지날', '반반콤보', '시그니처순살세트', '레허반반순살', '레블반반콤보','시그니처세트', '반반점보윙', '방콕점보윙'],
    'etc' : ['라이스세트', ' 반반사이드', '리얼치킨버거', '점보윙', '블랙치밥세트', '허니사이드', '사이드', '통통치킨카츠']
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
# 각 행의 맛 카테고리 카운트
for row in grouped_df['CombinedData']:
    count = {key: 0 for key in flavor_lists}
    for item in row:
        for flavor, items in flavor_lists.items():
            if item in items:
                count[flavor] += 1
                break

print(count)

labels = list(count.keys())
sizes = list(count.values())
print(labels)

plt.pie(sizes, labels=flavor_lists.keys(), autopct='%1.1f%%')
# plt.show()
plt.close()

def plot_grouped_pie_charts(dataframe, region_column, flavor_column):
    regions = dataframe[region_column].unique()
    results = []
    region_titles = []

    for region in regions:
        region_data = dataframe[dataframe[region_column] == region]
        flavor_counts = region_data[flavor_column].explode().value_counts()

        if not flavor_counts.empty:
            results.append(flavor_counts)
            region_titles.append(region)

    # 3개씩 그룹화하여 파이 차트 그리기
    for i in range(0, len(results), 3):
        fig, axs = plt.subplots(1, 3, figsize=(14, 14))  # 한 행에 3개의 차트
        for j, ax in enumerate(axs):
            if i + j < len(results):
                sizes = results[i + j]
                labels = sizes.index
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax.set_title(region_titles[i + j])
            else:
                ax.axis('off')  # 더 이상 표시할 데이터가 없으면 축 비활성화

        plt.tight_layout()
        plt.savefig(f'마포구 교촌 pie_charts_row_{i // 3 + 1}.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

plot_grouped_pie_charts(df, 'region', '순살 여부')