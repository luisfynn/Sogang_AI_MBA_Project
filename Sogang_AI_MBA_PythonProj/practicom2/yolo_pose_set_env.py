# 1. yolo v8 설치
# pip install ultralytics
# 참조 코드 및 사이트
# https://github.com/ultralytics/ultralytics.git
# https://docs.ultralytics.com/datasets/pose/coco8-pose/#dataset-yaml
# 2. 환경 설정
# 설치할 패키지들
# pip install mediapipe opencv-python numpy torch torchvision torchaudio matplotlib numpy pillow

# 3. Keypoints 추출 (MediaPipe 사용)
# yolo pose label은 56개의 데이터로 구성되어 있다(class+box+keypoints(1+4+17*3=56)
# openpose나 yolo 모델로도 가능. openpose의 경우 실패. yolo는 가능하지만 이번 경우는 mediaPipe를 사용해봄
#######################################################################################################################
# library 불러오기
import shutil
import os
import mediapipe as mp
import cv2
import numpy as np
from ultralytics import YOLO
from torchvision.ops import nms
import torch
# drawing
from PIL import ImageFont, ImageDraw, Image
import math
#######################################################################################################################
# dataSetA
# AI-HUB의 피트니스 자세 이미지(1 Tera 용량)
# train : 약  45.0GB, 151,755개 이미지 사용
# train & validation 이미지 이동

# dataSetB
# AI_HUB의 사람 동작 영상(2020)
# https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=61

# dataSetA,B 또는 다른 데이터셋을 구해서 라벨 생성 후 coco8-pose폴더로 복사 후 finetunning 진행

# 폴더가 계층구조로 되어 있는 경우 최하단 폴더의 이미지를 최상단 폴더로 모두 이동시키는 함수
def move_jpg_to_top_folder(top_folder):
    # Walk through all directories and subdirectories
    for root, dirs, files in os.walk(top_folder):
        for file in files:
            # Check if the file is a JPG
            if file.lower().endswith('.jpg'):
                # Construct full file path
                file_path = os.path.join(root, file)
                # Move the file to the top folder
                shutil.move(file_path, top_folder)
                print(f"Moved: {file_path} to {top_folder}")

# Example usage
top_folder = 'Pose_DataSet'
# top_folder = 'YOLOv8-pose/valid'
move_jpg_to_top_folder(top_folder)
#######################################################################################################################
# mediaPipe를 사용하여 이미지들로부터 keypoints 추출한 후 yolo train을 위한 좌표 데이터로 변환
# 한글명 파일인 경우 탐색기에서 해당 폴더로 이동 후 전체 선택 -> 이름 변경 -> 영문이름 하면 일괄 변경됨
# Mediapipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# 이미지 폴더 경로
image_folder = 'coco8-pose'
output_folder = 'coco8-pose'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 이미지 파일 목록 가져오기
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

def extract_keypoints(image_path):
    # 이미지 로드
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 관절 정보 추출
    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        return None

    keypoints = []
    for landmark in results.pose_landmarks.landmark:
        keypoints.append((landmark.x, landmark.y, landmark.z))

    return keypoints


def convert_to_yolo_format(image_shape, keypoints):
    height, width, _ = image_shape
    yolo_data = []

    for x, y, z in keypoints:
        yolo_x = x * width
        yolo_y = y * height
        yolo_z = z
        yolo_data.extend([yolo_x, yolo_y, yolo_z])

    return yolo_data

# 메인 루프
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    keypoints = extract_keypoints(image_path)

    if keypoints is None:
        continue

    image = cv2.imread(image_path)
    yolo_data = convert_to_yolo_format(image.shape, keypoints)

    # YOLO 형식: class (여기서는 0으로 가정) + bounding box (dummy 값) + keypoints
    class_id = 0
    bounding_box = [0, 0, 1, 1]  # 더미 값 사용
    yolo_format = [class_id] + bounding_box + yolo_data

    # 결과 저장
    output_file = os.path.join(output_folder, os.path.splitext(image_file)[0] + '.txt')
    with open(output_file, 'w') as f:
        f.write(' '.join(map(str, yolo_format)) + '\n')

print("Processing complete.")
#######################################################################################################################
# YOLO 모델 finetunning
# 직접 작성한 dataset.yaml 외에도 C:\Users\luisf\AppData\Roaming\Ultralytics의 settings.yaml도 확인해서 경로 일치시켜줘야 함
# Load a pre-trained model
model = YOLO('yolov8x-pose-p6.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='dataset.yaml', epochs=10, imgsz=640)

# Optionally, you can save the model after training
model.save('trained_yolov8x-pose-p6.pt')
#######################################################################################################################
# YOLO 모델 validation
# Load a model
model = YOLO('trained_yolov8x-pose-p6.pt')  # load a custom model

# Validate the model
metrics = model.val()  # no arguments needed, dataset and settings remembered
metrics.box.map    # map50-95
metrics.box.map50  # map50
metrics.box.map75  # map75
metrics.box.maps   # a list contains map50-95 of each category
#######################################################################################################################
# YOLO 모델 prediction
# Load a model
# model = YOLO('runs/pose/train4/weights/best.pt')  # load a custom model
# model = YOLO('yolov8x-pose-p6.pt')  # load a custom model
model = YOLO('trained_yolov8x-pose-p6.pt')  # load a custom model
# Predict with the model
results = model('coco8-pose/images/train/000000000036.jpg', save = False)  # predict on an image
# print(results)

# boxes = [result.boxes.xyxyn.cpu().numpy() for result in results]
# print(boxes)
#
# keypoint = [result.keypoints for result in results]
# print(keypoint)

# Non-Max Suppression 및 키포인트 추출
conf_thres = 0.5
iou_thres = 0.65

filtered_keypoints = []

# 결과에서 박스와 키포인트 추출
for result in results:
    # 각 결과에서 박스 및 키포인트 정보 추출
    boxes = result.boxes
    keypoints = result.keypoints

    # boxes 및 keypoints가 None이 아닌지 확인
    if boxes is not None and keypoints is not None:
        # 박스 좌표 및 점수 추출
        bboxes = boxes.xyxy
        scores = boxes.conf

        # Non-Max Suppression 수행
        nms_indices = nms(bboxes, scores, iou_thres)

        # NMS가 적용된 인덱스를 사용하여 키포인트 필터링 및 xy 값 추출
        for idx in nms_indices:
            kp = keypoints[idx]
            xy_values = kp.xy.cpu().numpy()
            filtered_keypoints.append(xy_values)

# 결과 출력
for kpt in filtered_keypoints:
    print(kpt)
#######################################################################################################################
# cuda 설치 및 확인
# 터미널에서  nvidia-smi 입력 #12.3
# 없는 경우
# NVIDIA 웹사이트에서 최신 CUDA Toolkit을 다운로드 및 설치
# NVIDIA 웹사이트에서 cuDNN 라이브러리를 다운로드 후 인터넷 검색하여 진행

# torch version 확인
import torch
print(torch.__version__) #2.3.0+cpu

# pytorch 없는 경우 설치
# pip install torch torchvision torchaudio
# pytorch 가 cpu 버전인 경우 삭제 후 재설치
# pip uninstall torch torchvision torchaudio
# https://pytorch.org/ 공식 사이트 접속하여 하단 옵션 선택 후 명령어 복사하여 설치
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')