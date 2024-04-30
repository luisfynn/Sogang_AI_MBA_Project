import pandas as pd
import os
import re

# 합칠 파일들이 저장된 디렉토리 경로
directory_path = 'D:\\06.AI MBA\\01.수업자료\\3학기\\3-1-3.빅데이터마케팅\\기말과제\\브랜드별분석'

# 정규 표현식 패턴
pattern = r'-(.*?)_final_page\.html_reviews\.csv'

# 데이터프레임을 저장할 변수 초기화
# combined_df = pd.DataFrame(columns=['region', 'store', 'dates', 'order_items', 'reviews', 'taste_score', 'quantity_score', 'delivery_score'])
combined_df = pd.DataFrame()

# 디렉토리 내의 모든 파일에 대해 반복

for folder in os.listdir(directory_path):
    brand_path = directory_path + '\\' + folder
    for filename in os.listdir(brand_path):
        if filename.endswith('.csv'):  # CSV 파일만 처리하도록 제한
            file_path = os.path.join(brand_path, filename)
            # CSV 파일을 데이터프레임으로 읽어와 합침
            df = pd.read_csv(file_path)

            match = re.search(pattern, filename)
            branch = match.group(1)
            df.insert(loc=0, column='brand', value=folder)
            df.insert(loc=1, column='store', value=branch)
            # df['store'] = branch
            combined_df = pd.concat([combined_df, df], ignore_index=True)

print(combined_df.head())
print(combined_df.shape)
combined_df.to_csv("combined_df.csv", encoding='utf-8-sig')
# index=False

