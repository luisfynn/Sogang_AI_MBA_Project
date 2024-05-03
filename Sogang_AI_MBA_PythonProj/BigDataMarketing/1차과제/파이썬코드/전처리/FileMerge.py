import pandas as pd
import os

# 합칠 파일들이 저장된 디렉토리 경로
directory_path = 'G:/내 드라이브/TaeHwan/1. SOGANG AI-MBA/24 1st semester/빅데이타 마케팅/프로젝트'

# 데이터프레임을 저장할 변수 초기화
combined_df = pd.DataFrame(columns=['ID', 'sentences', 'datetime', 'score'])
df_s = pd.DataFrame(columns=['ID', 'sentences', 'datetime', 'score'])

# 디렉토리 내의 모든 파일에 대해 반복
for filename in os.listdir(directory_path):
    if filename.endswith('.csv'):  # CSV 파일만 처리하도록 제한
        file_path = os.path.join(directory_path, filename)
        # CSV 파일을 데이터프레임으로 읽어와 합침
        df = pd.read_csv(file_path)

        df_s['ID'] = df.iloc[:, 1]
        df_s['sentences'] = df.iloc[:, 2]

        combined_df = pd.concat([combined_df, df_s], ignore_index=True)

print(combined_df.head())
print(combined_df.shape)
combined_df.to_csv("combined_df.csv", encoding='utf-8-sig')
