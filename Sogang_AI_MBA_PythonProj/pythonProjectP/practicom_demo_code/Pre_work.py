# yolo 다운로드:터미널에서 실행
# git clone https://github.com/ultralytics/yolov5
# cd yolov5
# pip install -r requirements.txt

# 학습 데이터 준비: 데이터 좌표 형식 <class> <x_center> <y_center> <width> <height>
# 이미지라벨 후 생성된 JSON 파일을 YOLO 포맷으로 변환
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

import json
from PIL import Image

# JSON 파일과 이미지 파일이 저장된 디렉토리
json_dir = r'C:/Users/rush0/PycharmProjects/Foodlabel/data_sets'

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

        # 클래스 이름과 ID 매핑
        class_name_to_id = {
            'spoon': 0,
            'kimbab': 1,
            'ramen': 2,
            # 필요한 경우 더 많은 클래스 추가
        }

        # YOLO 포맷으로 변환 및 저장
        yolo_data = []
        for item in data['shapes']:
            # 각 객체 정보 추출 및 변환
            class_name = item['label']
            class_id = class_name_to_id.get(class_name, -1)
            if class_id == -1:
                print(f"Unknown class name: {class_name}")
                continue
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
train_dir = r'C:/Users/rush0/PycharmProjects/Foodlabel/data_sets/train'
val_dir = r'C:/Users/rush0/PycharmProjects/Foodlabel/data_sets/val'

yolo_labels_dir = json_dir
# images_dir = json_dir

# 레이블 파일 목록 생성
label_files = [f for f in os.listdir(yolo_labels_dir) if f.endswith('.txt')]
train_files, val_files = train_test_split(label_files, test_size=0.2, random_state=42)

# Train 및 Val 폴더 생성 및 데이터 이동
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# 파일 이동
def move_files(files, source, destination):
    for file in files:
        shutil.move(os.path.join(source, file), os.path.join(destination, file))  ## label files
        shutil.move(os.path.join(source, file.replace('.txt', '.jpg')), os.path.join(destination, file.replace('.txt', '.jpg')))  ## image files

move_files(train_files, yolo_labels_dir, train_dir)
move_files(val_files, yolo_labels_dir, val_dir)

# YOLO 학습 실행
# 경로 주의
# python yolov5/train.py --img 640 --batch 16 --epochs 50 --data "C:/Users/rush0/PycharmProjects/Foodlabel/yolov5/data/coco.yaml" --weights yolov5s.pt
# --> 완료시 runs/exp/weights 폴더 아래 best.pt, last.pt 파일 생성됨