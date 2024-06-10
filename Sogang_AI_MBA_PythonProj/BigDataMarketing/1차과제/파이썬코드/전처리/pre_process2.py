import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 엑셀 파일 불러오기
directory_path = 'D:/06.AI MBA/01.수업자료/3학기/3-1-3.빅데이터마케팅/중간과제/Output3'
file_name = 'SNS_분석데이터_전처리후.xlsx'
file_path = os.path.join(directory_path, file_name)

data = pd.read_excel(file_path)
data['빈도수'] = data['빈도수'].astype('int64')
sorted_data = data.sort_values(by='빈도수', ascending=False)
# print(sorted_data)

# JLab Miner Library_2조 제출파일.xlsx 파일의 불용어 체크한 대상을 가져옴
stopword_file = pd.read_excel(directory_path + '/' + 'JLab Miner Library_2조 제출파일.xlsx')
stopwordList = stopword_file[['tag', 'Clean_Characters']]
stopword = stopwordList[stopwordList['Clean_Characters'] == 1]
# print(stopword)
print(stopword_file.columns)

# JLab Miner Library_2조 제출파일.xlsx 파일의 표제어 체크한 대상을 가져옴
lemmawordList = stopword_file[['tag', 'Lemmatization']]
lemmaword = lemmawordList[lemmawordList['Lemmatization'].notna()]
# print(lemmaword)

# stopword2의 tag(불용어)가  sorted_data['단어']에 있으면 해당 단어를 제거
condition1 = sorted_data['단어'].isin(stopword['tag'])
filtered_data = sorted_data[~condition1]
print(filtered_data)

# lemmaword의 tag(불용어)가  sorted_data['단어']에 있으면 해당 단어를 표제어로 변경
# 불용어인지 확인하여 lemmatization 열에 있는 단어로 변경하는 함수
# lemmaword_df와 sorted_df를 'tag' 열을 기준으로 조인
merged_df = pd.merge(filtered_data, lemmaword, how='left', left_on='단어', right_on='tag')
# 'lemmatization_y' 열의 결측치를 '단어' 열 값으로 대체
merged_df['Lemmatization'].fillna(merged_df['단어'], inplace=True)
# 필요한 열만 선택
merged_df2 = merged_df[['Lemmatization', '빈도수']]
# print(merged_df[merged_df['단어']=='클릭'])
# print(merged_df2)
# print(merged_df2.isna)

result_df = merged_df2.groupby('Lemmatization').sum().reset_index().sort_values(by = '빈도수', ascending=False)
# print(result_df)

# 빈도수로 정렬
result_df.to_excel(directory_path + '/' + "SNS_Googleplay_sorted.xlsx", index = False)


# 한글 폰트 경로 설정
font_path = 'C:/Windows/fonts/malgun.ttf'  # Windows 예시, 다른 OS의 경우 해당 폰트 경로로 변경
sns.set_context('paper', # notebook, talk, poster
                rc={'font.size':15,
                    'xtick.labelsize':15,
                    'ytick.labelsize':15,
                    'axes.labelsize':15})

# countplot 그래프 그리기
plt.figure(figsize=(15, 10))
plt.rcParams['font.family'] = 'Malgun Gothic'
sns.barplot(result_df.head(20), x = "Lemmatization", y = "빈도수")
plt.show()
plt.savefig(directory_path + '/' + 'SNS_Googleplay_wordfreq.jpg')

# word cloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# text
result_df['Lemmatization'] = result_df['Lemmatization'].astype(str)
text = ' '.join(result_df['Lemmatization'])

# WordCloud 객체 생성 및 한글 폰트 지정
wordcloud = WordCloud(font_path=font_path, background_color='white', width=800, height=600).generate(text)

# 워드클라우드 그리기
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # 축 제거
plt.show()
plt.savefig(directory_path + '/' + 'SNS_Googleplay_wordcloud.jpg')