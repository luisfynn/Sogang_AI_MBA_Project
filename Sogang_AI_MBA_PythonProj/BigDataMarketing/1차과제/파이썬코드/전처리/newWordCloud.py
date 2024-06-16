import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 엑셀 파일 경로
file_path = r'C:\Users\luisf\OneDrive\desktop\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\BigDataMarketing\1차과제\크롤링데이터\SNS_분석데이터_전처리후 - 복사본.xlsx'

# 엑셀 파일 로드
data = pd.read_excel(file_path)

# 데이터 값 변경
replacement_dict = {
    '챌린지': '챌린저스',
    '너무': '좋다',
    '좋아': '좋다',
    '좋아요': '좋다',
    '상금': '보상',
    '포인트': '보상',
    '습관': '자기관리',
    '기능': '동기부여'
}

data['단어'] = data['단어'].replace(replacement_dict)

# 같은 단어의 빈도수 합치기
data_grouped = data.groupby('단어', as_index=False).agg({'빈도수': 'sum'})

# '챌린저스' 단어 필터링
challengers_data = data_grouped[data_grouped['단어'] != '챌린저스']
challengers_data = challengers_data[challengers_data['단어'] != '좋다']
challengers_data = challengers_data[challengers_data['단어'] != '어플']

# 데이터 확인
print(challengers_data)

# 데이터 준비
word_freq = dict(zip(challengers_data['단어'], challengers_data['빈도수']))

# 워드클라우드 생성
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=r'C:\Users\luisf\OneDrive\desktop\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\BigDataMarketing\1차과제\MalgunGothic.ttf').generate_from_frequencies(word_freq)

# 워드클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()