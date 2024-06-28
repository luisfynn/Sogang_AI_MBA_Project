# 패키지 설치
# pip install torch torchvision pandas scikit-learn openpyxl

# labelme 설치 및 이미지 라벨링//anaconda prompt 사전 설치 필요//파이참 종료후 할 것
# set PYTHONIOENCODING=utf-8
# conda create --name=labelme python=3
# conda activate labelme
# pip install labelme

# anaconda prompt 닫은 후, 다시 열었을 때
# conda activate labelme
# labelme 실행: labelme C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/archive --autosave
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
json_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/face_recog_code/feelingdata'

# 클래스 매핑
label_mapping = {'angry': 0, 'disgust': 1, 'fear': 2, 'happy': 3, 'neutral': 4, 'sad': 5, 'surprise': 6}

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
            class_name = item['label']  # JSON 파일에서 클래스 이름 추출
            class_id = label_mapping.get(class_name, -1)  # 클래스 이름을 ID로 변환, 없는 경우 -1 반환
            if class_id == -1:
                continue  # 유효하지 않은 클래스 이름인 경우 스킵

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
train_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/face_recog_code/feelingdata/train'
val_dir = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/face_recog_code/feelingdata/test'
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

# dataset 구성:dataset.yaml
# train, val: 데이터 경로, nc: 라벨 수, names: 라벨 이름
# train: C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/archive/train
# val: C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/archive/test
# nc: 7
# names: ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

# YOLO 학습 실행
# 경로 주의
# python yolov5/train.py --img 640 --batch 16 --epochs 50 --data "C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/face_recog_code/face_dataset.yaml" --weights yolov5s.pt# --> 완료시 runs/exp/weights 폴더 아래 best.pt, last.pt 파일 생성됨
# 학습된 라벨 확인:class(label)이 한글로 정상 출력되는지 확인
import torch
filePath = r"C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/yolov5/runs/train/exp2/weights/best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path= filePath)
print(model.names)  # 클래스 이름 출력
# {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# 예측
# 모델 로드
import torch

# 모델 로드
# 'custom' 사용은 사용자 정의 모델 가중치를 로드할 때 필요합니다.
# 'best.pt'는 학습 과정에서 가장 좋은 성능을 보인 모델의 가중치 파일입니다.
filePath = r"C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/yolov5/runs/train/exp3/weights/best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path= filePath)

# 이미지 로드 및 예측
img = r'C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/test1.jpg'  # 예측할 이미지의 경로
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


# 평가
import torch
import os
import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# %matplotlib inline  # 주피터 노트북에서 그림을 인라인으로 표시하기 위해 필요합니다

# Load the YOLOv5 model
filePath = r"face_recog_code/face_best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', path=filePath, force_reload=True)

# Path to validation images and labels
val_path = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/face_recog_code/feelingdata/test'
label_mapping = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Get list of image files in the validation folder
image_files = [os.path.join(val_path, f) for f in os.listdir(val_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Placeholder for predictions (listA) and ground truths (listB)
listA = []
listB = []

# Function to get ground truth label from corresponding text file
def get_ground_truth_from_txt(file_path):
    with open(file_path, 'r') as file:
        label = int(file.readline().strip().split()[0])
    return label_mapping[label]

# Run inference on all validation images
results = model(image_files)

# Process each image and its corresponding ground truth
for img_path in image_files:
    # Get prediction for the current image
    pred = results.pandas().xyxy[image_files.index(img_path)]
    # Assuming the highest confidence prediction is the label (you can adjust based on your requirement)
    if len(pred) > 0:
        pred_class = int(pred.iloc[0]['class'])  # Get the predicted class
        print(f"Image: {img_path}, Predicted Class: {pred_class}")
        listA.append(pred_class)
    else:
        print(f"Image: {img_path}, No detection made.")
        listA.append(-1)  # Append -1 or any invalid class if no detection is made

    # Get the corresponding ground truth label
    txt_file_path = os.path.splitext(img_path)[0] + '.txt'
    if os.path.exists(txt_file_path):
        gt_class = get_ground_truth_from_txt(txt_file_path)
        print(f"Image: {img_path}, Ground Truth Class: {gt_class}")
        listB.append(gt_class)
    else:
        print(f"Image: {img_path}, Ground Truth File not found.")
        listB.append('unknown')  # Handle case where ground truth file doesn't exist

# Filter out invalid entries
valid_indices = [i for i in range(len(listA)) if listA[i] != -1 and listB[i] != 'unknown']
listA = [listA[i] for i in valid_indices]
listB = [listB[i] for i in valid_indices]

# Convert listB to indices to match the predictions
listB = [list(label_mapping.values()).index(label) for label in listB]

# Compute confusion matrix
cm = confusion_matrix(listB, listA, labels=list(label_mapping.keys()))

# Display the confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(label_mapping.values()))
disp.plot(cmap=plt.cm.Blues)
plt.show()

# Save the confusion matrix to a file
output_path = r'C:/Users/luisf/OneDrive/desktop/WorkSpace/Sogang_AI_MBA_Project/Sogang_AI_MBA_PythonProj/Practicom/confusion_matrix.png'
plt.savefig(output_path)
plt.close()  # Close the plot to avoid displaying it