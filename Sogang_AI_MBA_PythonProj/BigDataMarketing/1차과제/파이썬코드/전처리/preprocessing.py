from wordcloud import WordCloud, STOPWORDS
import re
import nltk
from collections import Counter
import re
nltk.download('stopwords')
import matplotlib.pyplot as plt
import pandas as pd

# 파일 읽기
# 구글 드라이브 파일을 읽어오기
# URL은 변경하지 마세요.
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTLsO7-y873IaNRElLjdMme3Er2A17Kdzr4yVa_ttsw5Hje26J8-DwJX7hCu45cvA/pub?gid=718240835&single=true&output=csv"
origin = pd.read_csv(URL)

#  ID가 없는 항목은 제거(불필요한 항목. ID 가 없으면 글도 없음)
preDf = origin.contents[origin.ID != ""]
print(preDf)

# 내용 합쳐서 하나의 문장으로 만들기
combined_string = " ".join([str(item) for item in preDf])
print(combined_string)

# 빈도표 작성
# 한글 불용어 처리
# 추가하기 <------------------- 필수

# 영문, 숫자, 특수문자 제거
cleaned_string = re.sub(r'[a-zA-Z0-9]|[^\w\s]', '', combined_string)

# 공백을 기준으로 단어 분리 후 한글 단어의 빈도 계산
korean_words = cleaned_string.split()
korean_word_freq = Counter(korean_words)

# 빈도가 높은 순서로 정렬
korean_word_freq_sorted = korean_word_freq.most_common()

# 정렬된 빈도 리스트 출력
for word, freq in korean_word_freq_sorted:
    print(f"'{word}': {freq}번")

# 파일로 저장
# 단어와 빈도수를 각각의 리스트로 준비
words = [word_freq[0] for word_freq in korean_word_freq_sorted]
frequencies = [word_freq[1] for word_freq in korean_word_freq_sorted]

# 리스트를 사용하여 데이터 프레임 생성
WordFreq = pd.DataFrame({
    'word': words,
    'freq': frequencies
})

# 데이터 프레임을 CSV 파일로 저장
WordFreq.to_csv("WordFreq.csv", encoding='utf-8-sig', index=False)
