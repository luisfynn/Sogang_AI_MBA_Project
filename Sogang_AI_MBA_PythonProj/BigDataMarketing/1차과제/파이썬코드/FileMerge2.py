import pandas as pd
import os

# 파일 불러오기
data1 = pd.read_excel("gmarket_products_습관관리_11페이지.xlsx", sheet_name = 'Sheet1')
data2 = pd.read_excel("gmarket_products_자기관리_50페이지.xlsx", sheet_name = 'Sheet1')
data3 = pd.read_excel("gmarket_products_홈트레이닝_50페이지.xlsx", sheet_name = 'Sheet1')
# print(data1)

# 파일 합치기
combined = list()
combined.append(data1)
combined.append(data2)
combined.append(data3)
print(len(combined))

# xlsx파일로 저장하기 위해 데이터프레임 생성
combinedDf = pd.DataFrame()
combinedDf['contents'] = combined

# 파일 저장하기
combinedDf.to_excel("분석 데이터.xlsx")
