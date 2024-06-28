import Calculation
import Visualization
import torch
import pandas as pd
import matplotlib.pyplot as plt
import cv2

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

if __name__ == "__main__":

    ## New 이미지 인식
    model = torch.hub.load('ultralytics/yolov5', 'custom', path= r'yolov5/runs/train/exp13/weights/best.pt')
    img = r'test/김밥_라면_스푼_test8.jpg'  # 예측할 이미지의 경로
    save_path = r'detection/detected.jpg'

    detections = Calculation.get_image(model, img)

    ## 인식한 이미지 출력

    Visualization.draw_and_save_image(model, img, save_path)

    ## 이미지 안 음식들의 사이즈 계산
    labels_and_sizes = Calculation.get_labels_and_sizes(detections)

    spoon_size = Calculation.get_size_by_label(labels_and_sizes, 'spoon')
    ramen_size = Calculation.get_size_by_label(labels_and_sizes, 'ramen')
    kimbab_size = Calculation.get_size_by_label(labels_and_sizes, 'kimbab')

    ## 음식의 이름 한글로 변환
    labelConverter = {'spoon': '스푼', 'kimbab':'김밥', 'ramen':'라면'}
    food_name_eng = detections[detections['name']!='spoon']['name']
    food_names = food_name_eng.apply(lambda x: labelConverter[x])

    size_ratios = dict()
    size_ratios['라면'] = ramen_size / spoon_size
    size_ratios['김밥'] = kimbab_size / spoon_size

    # 칼로리와 영양소 데이터 로드
    ref_filepath = r'C:/Practicom/02.음식사진인식/식품영양성분DB_음식_단순화_20240606.xlsx'
    df = pd.read_excel(ref_filepath)



    ## 음식별 칼로리와 영양소 계산
    nutritional_info = Calculation.get_nutritional_info(df, food_names, size_ratios)

    ## 이미지 안 음식의 총 칼로리와 영양소 계산
    total_nutrition = Calculation.get_total(nutritional_info)

    ## 음식의 총 칼로리와 영양소를 타입별로 변수에 저장
    total_calory = total_nutrition[0]
    total_carbon = total_nutrition[1]
    total_protein = total_nutrition[2]
    total_fat = total_nutrition[3]
    total_natrium = total_nutrition[4]

    ## 그래프 생성
    Visualization.draw_bar_chart(total_calory, total_carbon, total_protein, total_fat, total_natrium)




