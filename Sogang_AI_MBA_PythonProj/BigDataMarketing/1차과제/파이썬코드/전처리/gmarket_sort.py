import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

FREQUENCY = 1000

# 엑셀 파일 불러오기
data = pd.read_csv("gmarket_filtered_token_frequency_sorted.csv")
data['Frequency'] = data['Frequency'].astype('int64')
sorted_data = data.sort_values(by='Frequency', ascending=False)
# print(sorted_data)

# JLab Miner Library_2조 제출파일.xlsx 파일의 불용어 체크한 단어들 제거 또는 변경
stopword = pd.read_excel('JLab Miner Library_2조 제출파일.xlsx')
stopwordList = stopword[['tag', 'Clean_Characters']]
stopword2 = stopwordList[stopwordList['Clean_Characters'] == 1]
# print(stopword2)

# stopword2의 tag(불용어)가  sorted_data['Token']에 있으면 해당 단어를 제거
condition = sorted_data['Token'].isin(stopword2['tag'])
filtered_data = sorted_data[~condition]
print(filtered_data)

# 08. gmarket_filtered_token_frequency_sorted_delete.csv에 d라고 입력된 단어를 제거
wy_stopword = pd.read_csv("08. gmarket_filtered_token_frequency_sorted_delete.csv")
wy_stopword2 = wy_stopword[wy_stopword['delete'] == 'd']
condition = filtered_data['Token'].isin(wy_stopword2['Token'])
filtered_data2 = filtered_data[~condition]
print(filtered_data2)


# 빈도수로 정렬
filtered_data2.to_csv("gmarket_sorted.csv", encoding='cp949')

# 한글 폰트 경로 설정
font_path = 'MalgunGothic.ttf'  # Windows 예시, 다른 OS의 경우 해당 폰트 경로로 변경

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.figure(figsize=(15, 10))
sns.barplot(filtered_data2.head(20), x = "Token", y = "Frequency")
# plt.show()
plt.savefig('gmarket_wordfreq.jpg')

# word cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# text
text = ' '.join(filtered_data2['Token'])

# WordCloud 객체 생성 및 한글 폰트 지정
wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=600).generate(text)

# 워드클라우드 그리기
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 축 제거
# plt.show()
plt.savefig('gmarket_wordcloud.jpg')
