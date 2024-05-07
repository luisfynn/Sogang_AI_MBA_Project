# 파이참 찾아서 바꾸기 ctrl+r
# 패키지 설치
# pip install torch torchvision pandas scikit-learn openpyxl

# labelme 설치 및 이미지 라벨링//anaconda prompt 사전 설치 필요//파이참 종료후 할 것
# set PYTHONIOENCODING=utf-8
# conda create --name=labelme python=3
# conda activate labelme
# pip install labelme

# anaconda prompt 닫은 후, 다시 열었을 때
# conda activate labelme
# labelme 실행: labelme C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/korean_food_sample --autosave
# 이미지 라벨 작업
########################################################################################################################
# yolo 모델을 이용한 학습
# 패키지 설치
# pip install torch torchvision numpy matplotlib opencv-python

# yolo 다운로드:터미널에서 실행
# git clone https://github.com/ultralytics/yolov5
# cd yolov5
# pip install -r requirements.txt
# 학습 데이터 준비: 데이터 좌표 형식 <class> <x_center> <y_center> <width> <height>
# 이미지라벨 후 생성된 JSON 파일을 YOLO 포맷으로 변환
import os
import json
from PIL import Image

# JSON 파일과 이미지 파일이 저장된 디렉토리
json_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/korean_food_sample'

for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        image_file = json_file.replace('.json', '.jpg')  # JSON 파일과 동일한 이름의 이미지 파일 가정
        image_path = os.path.join(json_dir, image_file)
        json_path = os.path.join(json_dir, json_file)

        # 이미지의 너비와 높이 추출
        with Image.open(image_path) as img:
            width, height = img.size

        # JSON 파일 로드 및 파싱
        with open(json_path, 'r', encoding='utf-8') as file:  # 파일 읽을 때 UTF-8 인코딩 사용
            data = json.load(file)

        # YOLO 포맷으로 변환 및 저장
        yolo_data = []
        for item in data['shapes']:
            # 각 객체 정보 추출 및 변환
            class_id = 0  # 클래스 ID 설정 필요
            x_center = (item['points'][0][0] + item['points'][1][0]) / 2 / width
            y_center = (item['points'][0][1] + item['points'][1][1]) / 2 / height
            bbox_width = abs(item['points'][0][0] - item['points'][1][0]) / width
            bbox_height = abs(item['points'][0][1] - item['points'][1][1]) / height
            yolo_data.append(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}")

        # YOLO 포맷 데이터를 .txt 파일로 저장
        txt_path = image_path.replace('.jpg', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:  # 파일 쓸 때 UTF-8 인코딩 사용
            f.writelines('/n'.join(yolo_data))


# train,val 데이터 구분
import shutil
from sklearn.model_selection import train_test_split

# 폴더 정의
train_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/korean_food_sample/train'
val_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/korean_food_sample/val'
yolo_labels_dir = json_dir
images_dir = yolo_labels_dir

# 이미지 파일 목록 생성
image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
train_files, val_files = train_test_split(image_files, test_size=0.2, random_state=42)

# Train 및 Val 폴더 생성 및 데이터 이동
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 파일 이동
def move_files(files, source, destination):
    for file in files:
        shutil.move(os.path.join(source, file), os.path.join(destination, file))
        shutil.move(os.path.join(yolo_labels_dir, file.replace('.jpg', '.txt')), os.path.join(destination, file.replace('.jpg', '.txt')))

move_files(train_files, images_dir, train_dir)
move_files(val_files, images_dir, val_dir)
########################################################################################################################
# dataset 구성:dataset.yaml
# train, val: 데이터 경로, nc: 라벨 수, names: 라벨 이름
# train_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/korean_food_sample/train'
# val_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/korean_food_sample/val'
# nc: 3
# names: ['kimchi', 'bulgogi', 'bibimbab'] # names는 영어로 '김치', '불고기', '비빔밥'

# YOLO 학습 실행
# 경로 주의
# python yolov5/train.py --img 640 --batch 16 --epochs 50 --data "C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/dataset.yaml" --weights yolov5s.pt
# --> 완료시 runs/exp/weights 폴더 아래 best.pt, last.pt 파일 생성됨
########################################################################################################################
# 학습된 라벨 확인:class(label)이 한글로 정상 출력되는지 확인
import torch

model = torch.hub.load('ultralytics/yolov5', 'custom', path= r'yolov5/runs/train/exp5/weights/best.pt')
print(model.names)  # 클래스 이름 출력
########################################################################################################################
# 예측
# 모델 로드
import torch

# 모델 로드
# 'custom' 사용은 사용자 정의 모델 가중치를 로드할 때 필요합니다.
# 'best.pt'는 학습 과정에서 가장 좋은 성능을 보인 모델의 가중치 파일입니다.
model = torch.hub.load('ultralytics/yolov5', 'custom', path= r'yolov5/runs/train/exp5/weights/best.pt')

# 이미지 로드 및 예측
img = r'Food/korean_food_sample/val/Img_069_0005.jpg'  # 예측할 이미지의 경로
results = model(img)
print(f"results: {results}")

# 결과 출력
results.show()
results.save()

# 결과 출력 및 클래스 이름 검증
results.print()
for det in results.xyxy[0]:  # per image
    # det는 [x1, y1, x2, y2, confidence, class]
    class_id = int(det[5])
    class_name = model.names[class_id]
    print(f'Detected class: {class_name}')

# 라벨 변환
# names: ['kimchi', 'bulgogi', 'bibimbab'] # names는 영어로 '김치', '불고기', '비빔밥' 를 딕셔너리로 변환
labelConverter = {'kimchi':'김밥', 'bulgogi':'불고기', 'bibimbab':'비빔밥'}

# 칼로리 계산
# 칼로리 데이터 로드
import torch
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from PIL import Image
from torchvision import transforms

def load_calorie_data(filepath):
    df = pd.read_excel(filepath)
    return df.set_index('식품명')['에너지(kcal)'].to_dict()

# 칼로리 계산
def calculate_calories(food_labels, calorie_dict):
    return sum(calorie_dict.get(food, 0) for food in food_labels)

# 회귀분석 모델(예시)
def predict_weight_loss(calories, days=14):
    X = np.arange(1, days + 1).reshape(-1, 1)
    y = np.array([2000 - cal for cal in calories]) / 3500  # 3500kcal = 1 pound of fat
    model = LinearRegression()
    model.fit(X, y)
    return model.predict(X)

calorie_dict = load_calorie_data(r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/Food/식품영양성분DB_음식_20240416.xlsx')
# print("-------------------------")
# print(f"calorie_dict:{calorie_dict}")
# print("-------------------------")
# print(f"converted label:{labelConverter[class_name]}")

foodlist = [] #list 생성
foodlist.append(labelConverter[class_name])

total_calories = calculate_calories(foodlist, calorie_dict)
print(f"total_calories:{total_calories}")
print(f"[total_calories] * 14 -> {[total_calories] * 14}")
weight_loss_predictions = predict_weight_loss([total_calories] * 14)

print("예측 체중 감소:", weight_loss_predictions)
