import torch
import pandas as pd


def get_image(model, img):
    model = model
    img = img  # 예측할 이미지의 경로
    results = model(img)
    detections = results.pandas().xyxy[0]  # xyxy 포맷으로 결과 추출
    return detections


# 바운딩 박스 크기 계산 및 라벨과 크기 사전 반환 함수
def get_labels_and_sizes(detections):
    labels_and_sizes = []
    for index, row in detections.iterrows():
        x_min, y_min, x_max, y_max = row[['xmin', 'ymin', 'xmax', 'ymax']]
        box_width = x_max - x_min
        box_height = y_max - y_min

        box_area = box_width * box_height
        label = row['name']
        labels_and_sizes.append({'label': label, 'size': box_area})
    return labels_and_sizes

# 특정 라벨의 크기 추출 함수
def get_size_by_label(labels_and_sizes, target_label):
    for item in labels_and_sizes:
        if item['label'] == target_label:
            return item['size']
    return None

# 바운딩 박스 크기를 반영한 음식별 칼로리 계산 함수
def get_nutritional_info(df, food_names, size_ratios):
    nutritional_info = {}
    for food_name in food_names:
        if food_name in df['식품명'].values:
            info = df[df['식품명'] == food_name].iloc[0]
            size_ratio = size_ratios.get(food_name, 1)  # 기본값을 1로 설정

            if food_name == '김밥':
                nutritional_info[food_name] = {
                    '칼로리': info['에너지(kcal)'] * size_ratio / 1,
                    '탄수화물': info['탄수화물(g)'] * size_ratio / 1,
                    '단백질': info['단백질(g)'] * size_ratio / 1,
                    '지방': info['지방(g)'] * size_ratio / 1,
                    '나트륨': info['나트륨(mg)'] * size_ratio / 1
                }
            elif food_name == '라면':
                nutritional_info[food_name] = {
                    '칼로리': info['에너지(kcal)'] * size_ratio / 1.5,
                    '탄수화물': info['탄수화물(g)'] * size_ratio / 1.5,
                    '단백질': info['단백질(g)'] * size_ratio / 1.5,
                    '지방': info['지방(g)'] * size_ratio / 1.5,
                    '나트륨': info['나트륨(mg)'] * size_ratio / 1.5
                }
            else:
                nutritional_info[food_name] = {
                    '칼로리': info['에너지(kcal)'] * size_ratio,
                    '탄수화물': info['탄수화물(g)'] * size_ratio,
                    '단백질': info['단백질(g)'] * size_ratio,
                    '지방': info['지방(g)'] * size_ratio,
                    '나트륨': info['나트륨(mg)'] * size_ratio
                }
        else:
            nutritional_info[food_name] = None

    return nutritional_info

def get_total(nutritional_info):
    total_calory = sum(info['칼로리'] for info in nutritional_info.values() if info is not None)
    total_carbon = sum(info['탄수화물'] for info in nutritional_info.values() if info is not None)
    total_protein = sum(info['단백질'] for info in nutritional_info.values() if info is not None)
    total_fat = sum(info['지방'] for info in nutritional_info.values() if info is not None)
    total_natrium = sum(info['나트륨'] for info in nutritional_info.values() if info is not None)
    return total_calory, total_carbon, total_protein, total_fat, total_natrium

#
#
#
#
# #######################################################################
# spoon_size = get_size_by_label(labels_and_sizes, 'spoon')
# ramen_size = get_size_by_label(labels_and_sizes, 'ramen')
# kimbab_size = get_size_by_label(labels_and_sizes, 'kimbab')
#
# size_ratios = dict()
# size_ratios['라면'] = ramen_size / spoon_size
# size_ratios['김밥'] = kimbab_size / spoon_size
#
#
# # 라벨 변환
# labelConverter = {'spoon': '스푼', 'kimbab':'김밥', 'ramen':'라면'}
# food_name_eng = detections[detections['name']!='spoon']['name']
# food_names = food_name_eng.apply(lambda x: labelConverter[x])
# ##########################################################################
#
# ########################### 칼로리 계산 ################################
# # 칼로리와 영양소 데이터 로드
# ref_filepath = r'C:/Practicom/02.음식사진인식/식품영양성분DB_음식_단순화_20240606.xlsx'
# df = pd.read_excel(ref_filepath)
# nutritional_info = get_nutritional_info(df, food_names, size_ratios)
#
# print(nutritional_info)
#
# get_total(nutritional_info)
#
# ####################################################################################