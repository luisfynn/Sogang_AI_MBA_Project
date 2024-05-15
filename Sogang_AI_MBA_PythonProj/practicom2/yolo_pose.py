# 1. yolo v8 설치
# https://github.com/ultralytics/ultralytics.git
# 참고 사이트 : https://docs.ultralytics.com/datasets/pose/coco8-pose/#dataset-yaml
# 2. 환경 설정
# 설치할 패키지들
# pip install mediapipe opencv-python numpy torch torchvision torchaudio ultralytics matplotlib numpy

# 3. Keypoints 추출 (MediaPipe 사용)
# yolo pose label은 56개의 데이터로 구성되어 있다(class+box+keypoints(1+4+17*3=56)
# openpose나 yolo 모델로도 가능. openpose의 경우 실패. yolo는 가능하지만 이번 경우는 mediaPipe를 사용해봄
#######################################################################################################################
# library 불러오기
import shutil
import zipfile
import cv2
import mediapipe as mp
import os
import json
import numpy as np
import tarfile
import io
#######################################################################################################################
# dataSetA
# AI-HUB의 피트니스 자세 이미지(1 Tera 용량)
# train : 약  45.0GB, 151,755개 이미지 사용
# train & validation 이미지 이동

# dataSetB
# AI_HUB의 사람 동작 영상(2020)
# https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=61

# 폴더가 계층구조로 되어 있어서 최하단 폴더의 이미지를 최상단 폴더로 모두 이동시킴
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
import os
import cv2
import mediapipe as mp
import numpy as np

# Mediapipe 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

# 이미지 폴더 경로
image_folder = 'Pose_DataSet2'
output_folder = 'Pose_DataSet2'

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
from ultralytics import YOLO

# Load a pre-trained model
model = YOLO('yolov8x-pose-p6.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='dataset.yaml', epochs=10, imgsz=640)

# Optionally, you can save the model after training
model.save('trained_yolov8x-pose-p6.pt')