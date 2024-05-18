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
# 동영상으로 테스트A
# YOLOv8 포즈 모델 로드
model = YOLO("trained_yolov8x-pose-p6.pt")

# 비디오 파일 열기
cap = cv2.VideoCapture("test02.mp4")

# 비디오 파일의 속성 읽기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 출력 비디오 파일 설정
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

# keypoint list 설정
filtered_keypoints = []

# 비디오 프레임 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모델을 사용하여 포즈 추정
    results = model(frame)

    for result in results:
        boxes = result.boxes
        keypoints = result.keypoints

        if boxes is not None and keypoints is not None:
            bboxes = boxes.xyxy
            scores = boxes.conf

            # Non-Max Suppression 수행
            nms_indices = nms(bboxes, scores, iou_threshold=0.65)

            # NMS가 적용된 인덱스를 사용하여 키포인트 필터링 및 xy 값 추출
            for idx in nms_indices:
                kp = keypoints[idx]
                xy_values = kp.xy.cpu().numpy()  # xy 좌표 추출

                # 디버깅을 위해 xy_values의 구조를 출력
                # print("xy_values structure:", xy_values)

                # 키포인트를 프레임에 그리기
                for point in xy_values[0]:  # xy_values[0]을 사용하여 각 프레임의 키포인트 배열에 접근
                    x, y = point
                    print("xy_point:", point)

                    if x > 0 and y > 0:  # 유효한 좌표만 표시
                        cv2.circle(frame, (int(x), int(y)), 10, (255, 0, 0), -1)  # 파란색 원 그리기

    # 결과 프레임을 출력 비디오에 쓰기
    out.write(frame)

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()
#######################################################################################################################
# 동영상으로 테스트B
# findAngle 함수 정의
def findAngle(image, kpts, p1,p2,p3, draw= True):
    coord = []
    no_kpt = len(kpts)//2
    for i in range(no_kpt):
        cx,cy = kpts[2*i], kpts[2*i +1]
        # conf = kpts[2*i +2]
        # coord.append([i, cx,cy, conf])
        coord.append([i, cx, cy])

    points = (p1,p2,p3)

    # =3.1=Get landmarks========
    x1,y1 = coord[p1][1:3]
    print(f"x1:{x1},y1:{y1}")
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]

    # =3.2=Calculate the Angle========
    angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle < 0:
        angle += 360

    # =3.3=Draw Coordinates========
    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2), int(y2)),(255,255,255),3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2), int(y2)),(255,255,255),3 )

        cv2.circle(image, (int(x1),int(y1)),  10, (255,255,255),cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)

    return int(angle)


# 각 keypoint와 keypoint간 연결선 그리기 추가
# YOLOv8 포즈 모델 로드
model = YOLO("trained_yolov8x-pose-p6.pt")

# 비디오 파일 열기 및 사이즈 확인
cap = cv2.VideoCapture("test03.mp4")

# 비디오 파일의 속성 읽기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 출력 비디오 파일 설정
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

# 카운트 변수 및 방향 변수 초기화
bcount = 0
direction = 0

def plot_skeleton_kpts(im, kpts, steps, orig_shape=None):
    # Plot the skeleton and keypoints for COCO dataset
    palette = np.array([[255, 128, 0], [255, 153, 51], [255, 178, 102],
                        [230, 230, 0], [255, 153, 255], [153, 204, 255],
                        [255, 102, 255], [255, 51, 255], [102, 178, 255],
                        [51, 153, 255], [255, 153, 153], [255, 102, 102],
                        [255, 51, 51], [153, 255, 153], [102, 255, 102],
                        [51, 255, 51], [0, 255, 0], [0, 0, 255], [255, 0, 0],
                        [255, 255, 255]])

    skeleton = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12],
                [7, 13], [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3],
                [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]

    pose_limb_color = palette[[9, 9, 9, 9, 7, 7, 7, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16]]
    pose_kpt_color = palette[[16, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9]]
    radius = 5
    num_kpts = len(kpts) // steps

    for kid in range(num_kpts):
        r, g, b = pose_kpt_color[kid]
        x_coord, y_coord = kpts[steps * kid], kpts[steps * kid + 1]
        if not (x_coord % 640 == 0 or y_coord % 640 == 0):
            if steps == 3:
                conf = kpts[steps * kid + 2]
                if conf < 0.5:
                    continue
            overlay = im.copy()
            alpha = 0.4
            cv2.circle(overlay, (int(x_coord), int(y_coord)), 8, (int(220), int(237), int(245)), 8)
            cv2.circle(im, (int(x_coord), int(y_coord)), 5, (int(255), int(255), int(255)), -1)
            # im = output
            cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0, im)

    for sk_id, sk in enumerate(skeleton):
        r, g, b = pose_limb_color[sk_id]
        pos1 = (int(kpts[(sk[0]-1)*steps]), int(kpts[(sk[0]-1)*steps+1]))
        pos2 = (int(kpts[(sk[1]-1)*steps]), int(kpts[(sk[1]-1)*steps+1]))
        if steps == 3:
            conf1 = kpts[(sk[0]-1)*steps+2]
            conf2 = kpts[(sk[1]-1)*steps+2]
            if conf1 < 0.5 or conf2 < 0.5:
                continue
        if pos1[0] % 640 == 0 or pos1[1] % 640 == 0 or pos1[0] < 0 or pos1[1] < 0:
            continue
        if pos2[0] % 640 == 0 or pos2[1] % 640 == 0 or pos2[0] < 0 or pos2[1] < 0:
            continue
        cv2.line(im, pos1, pos2, (int(255), int(255), int(255)), thickness=2)

# 비디오 프레임 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모델을 사용하여 포즈 추정
    results = model(frame)

    for result in results:
        boxes = result.boxes
        keypoints = result.keypoints

        if boxes is not None and keypoints is not None:
            bboxes = boxes.xyxy
            scores = boxes.conf

            # Non-Max Suppression 수행
            nms_indices = nms(bboxes, scores, iou_threshold=0.65)

            # NMS가 적용된 인덱스를 사용하여 키포인트 필터링 및 xy 값 추출
            for idx in nms_indices:
                kp = keypoints[idx]
                xy_values = kp.xy.cpu().numpy()

                # 골격과 키포인트를 프레임에 그리기
                plot_skeleton_kpts(frame, xy_values.flatten(), steps=2)

                # 키포인트를 프레임에 그리기
                for point in xy_values[0]:  # xy_values[0]을 사용하여 각 프레임의 키포인트 배열에 접근
                    x, y = point
                    # print("xy_point:", point)

                    if x > 0 and y > 0:  # 유효한 좌표만 표시
                        cv2.circle(frame, (int(x), int(y)), 10, (255, 0, 0), -1)  # 파란색 원 그리기

                # 카운트 박스 그리기
                im_pil = Image.fromarray(frame)
                # color = (254, 118, 136)
                color = (0, 118, 136)
                draw = ImageDraw.Draw(im_pil)
                fw, fh = im_pil.size  # 이미지 크기 가져오기
                draw.rounded_rectangle((fw - 280, (fh // 2) - 100, fw - 80, (fh // 2) + 100), fill=color, radius=40)

                # 주요 keypoint 각도 측정
                angle = findAngle(frame, xy_values.flatten(), 5, 7, 9, draw=False)
                percentage = np.interp(angle, (10, 150), (100, 0))  # 팔을 굽히면(10도) 100%, 팔을 펴면(150도) 0% (검증 필요함)
                bar = np.interp(angle, (20, 150), (200, fh - 100))

                # 퍼센트 측정 박스
                # percent_color = (254, 118, 136)
                percent_color = (118, 254, 136)

                # 퍼센트표시 직선
                if (int(percentage) < 40):
                    #cv2.line(img, (155, int(bar)), (190, int(bar)), (254, 118, 136), 40)
                    cv2.line(frame, (155, int(bar)), (210, int(bar)), percent_color, 40)
                elif (int(percentage) >= 40 and (int(percentage) < 70)):
                    #cv2.line(img, (155, int(bar)), (200, int(bar)), (254, 118, 136), 40)
                    cv2.line(frame, (155, int(bar)), (210, int(bar)), percent_color, 40)
                else:
                    cv2.line(frame, (155, int(bar)), (210, int(bar)), percent_color, 40)

                # 카운트 bar 그리기
                cv2.line(frame, (100, 200), (100, fh-100),
                         (255, 255, 255), 30)
                cv2.line(frame, (100, int(bar)),
                         (100, fh-100), percent_color, 30)

                # bicep curls 카운트 측정
                if percentage >= 70:
                    if direction == 0:
                        bcount += 0.5
                        direction = 1
                if percentage <= 40:
                    if direction == 1:
                        bcount += 0.5
                        direction = 0

                print(f"count :{bcount}")
                # 카운트 텍스트 및 퍼센트 표시
                font = ImageFont.load_default(size = 50)  # 기본 폰트 사용, size = 90
                draw.text((145, int(bar)-17), f"{int(percentage)}%", font=font, fill=(255, 255, 255))
                draw.text((fw - 230, (fh // 2) - 50), f"{int(bcount)}", font=font, fill=(255, 255, 255))

                # PIL 이미지를 다시 OpenCV 이미지로 변환
                frame = np.array(im_pil)

    # 결과 프레임을 출력 비디오에 쓰기
    out.write(frame)

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()
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

#######################################################################################################################
# 스쿼트
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
import math
from PIL import Image, ImageDraw, ImageFont

def findAngle(image, kpts, p1,p2,p3, draw= True):
    coord = []
    no_kpt = len(kpts)//2
    for i in range(no_kpt):
        cx,cy = kpts[2*i], kpts[2*i +1]
        # conf = kpts[2*i +2]
        # coord.append([i, cx,cy, conf])
        coord.append([i, cx, cy])

    points = (p1,p2,p3)

    # =3.1=Get landmarks========
    x1,y1 = coord[p1][1:3]
    print(f"x1:{x1},y1:{y1}")
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]

    # =3.2=Calculate the Angle========
    angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle > 0:
        angle = 360 - angle

    # =3.3=Draw Coordinates========
    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2), int(y2)),(255,255,255),3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2), int(y2)),(255,255,255),3 )

        cv2.circle(image, (int(x1),int(y1)),  10, (255,255,255),cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)

    return int(angle)

# 각 keypoint와 keypoint간 연결선 그리기 추가
# YOLOv8 포즈 모델 로드
model = YOLO("trained_yolov8x-pose-p6.pt")

# 비디오 파일 열기 및 사이즈 확인
cap = cv2.VideoCapture("squart.mp4")

# 비디오 파일의 속성 읽기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 출력 비디오 파일 설정
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, fps, (width, height))

# 카운트 변수 및 방향 변수 초기화
bcount = 0
direction = 0

def plot_skeleton_kpts(im, kpts, steps, orig_shape=None):
    # Plot the skeleton and keypoints for COCO dataset
    palette = np.array([[255, 128, 0], [255, 153, 51], [255, 178, 102],
                        [230, 230, 0], [255, 153, 255], [153, 204, 255],
                        [255, 102, 255], [255, 51, 255], [102, 178, 255],
                        [51, 153, 255], [255, 153, 153], [255, 102, 102],
                        [255, 51, 51], [153, 255, 153], [102, 255, 102],
                        [51, 255, 51], [0, 255, 0], [0, 0, 255], [255, 0, 0],
                        [255, 255, 255]])

    skeleton = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12],
                [7, 13], [6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3],
                [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]

    pose_limb_color = palette[[9, 9, 9, 9, 7, 7, 7, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16]]
    pose_kpt_color = palette[[16, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9]]
    radius = 5
    num_kpts = len(kpts) // steps

    for kid in range(num_kpts):
        r, g, b = pose_kpt_color[kid]
        x_coord, y_coord = kpts[steps * kid], kpts[steps * kid + 1]
        if not (x_coord % 640 == 0 or y_coord % 640 == 0):
            if steps == 3:
                conf = kpts[steps * kid + 2]
                if conf < 0.5:
                    continue
            overlay = im.copy()
            alpha = 0.4
            cv2.circle(overlay, (int(x_coord), int(y_coord)), 8, (int(220), int(237), int(245)), 8)
            cv2.circle(im, (int(x_coord), int(y_coord)), 5, (int(255), int(255), int(255)), -1)
            # im = output
            cv2.addWeighted(overlay, alpha, im, 1 - alpha, 0, im)

    for sk_id, sk in enumerate(skeleton):
        r, g, b = pose_limb_color[sk_id]
        pos1 = (int(kpts[(sk[0]-1)*steps]), int(kpts[(sk[0]-1)*steps+1]))
        pos2 = (int(kpts[(sk[1]-1)*steps]), int(kpts[(sk[1]-1)*steps+1]))
        if steps == 3:
            conf1 = kpts[(sk[0]-1)*steps+2]
            conf2 = kpts[(sk[1]-1)*steps+2]
            if conf1 < 0.5 or conf2 < 0.5:
                continue
        if pos1[0] % 640 == 0 or pos1[1] % 640 == 0 or pos1[0] < 0 or pos1[1] < 0:
            continue
        if pos2[0] % 640 == 0 or pos2[1] % 640 == 0 or pos2[0] < 0 or pos2[1] < 0:
            continue
        cv2.line(im, pos1, pos2, (int(255), int(255), int(255)), thickness=2)

# 비디오 프레임 처리
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 모델을 사용하여 포즈 추정
    results = model(frame)

    for result in results:
        boxes = result.boxes
        keypoints = result.keypoints

        if boxes is not None and keypoints is not None:
            bboxes = boxes.xyxy
            scores = boxes.conf

            # Non-Max Suppression 수행
            nms_indices = nms(bboxes, scores, iou_threshold=0.65)

            # NMS가 적용된 인덱스를 사용하여 키포인트 필터링 및 xy 값 추출
            for idx in nms_indices:
                kp = keypoints[idx]
                xy_values = kp.xy.cpu().numpy()

                # 골격과 키포인트를 프레임에 그리기
                plot_skeleton_kpts(frame, xy_values.flatten(), steps=2)

                # 키포인트를 프레임에 그리기
                for point in xy_values[0]:  # xy_values[0]을 사용하여 각 프레임의 키포인트 배열에 접근
                    x, y = point
                    # print("xy_point:", point)

                    if x > 0 and y > 0:  # 유효한 좌표만 표시
                        cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)  # 파란색 원 그리기

                # 주요 keypoint 각도 측정
                # 한쪽 다리만 굽혀지는 경우는 없으니 한쪽 다리각도만 측정해도 정확도 보장 가능
                angle = findAngle(frame, xy_values.flatten(), 12, 14, 16, draw=False)
                print(f'angle: {angle}')
                print(f'xy_values: {xy_values.flatten()}')
                percentage = np.interp(angle, (120, 170), (100, 0))  # 스쿼트 굽힌 자세 120도 미만 : 100%, 선 자세 170도 이상 : 0%
                bar = np.interp(angle, (120, 170), (200, fh - 100))
                print(f'percentage: {percentage}, bar: {bar}')

                # 카운트 바 그리기
                cv2.line(frame, (100, 200), (100, fh - 100), (255, 255, 255), 30)
                cv2.line(frame, (100, int(bar)), (100, fh - 100), color, 30)

                # 텍스트 추가 (percentage)
                text = f"{percentage}%"
                font_scale = 0.8
                font_thickness = 2
                text_color = (0, 0, 255)  # 빨간색 폰트
                bg_color = (254, 118, 136)  # 텍스트 배경색
                font = cv2.FONT_HERSHEY_SIMPLEX

                # 텍스트 크기 계산
                (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
                text_x = 160  # 텍스트의 x 좌표
                text_y = int(bar) - 10  # 텍스트의 y 좌표

                # 텍스트 배경 박스 그리기
                cv2.rectangle(frame, (text_x - 5, text_y - text_height - 5),
                              (text_x + text_width + 5, text_y + baseline + 5),
                              bg_color, cv2.FILLED)

                # 텍스트 그리기
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

                # 스쿼트 카운트 측정
                if percentage >= 95:
                    if direction == 0:
                        # 조건 1: 골반 X 좌표가 양발 X 좌표보다 일정 값 이상 작거나 커야 한다.
                        # 골반 X좌표 (왼쪽과 오른쪽 골반 평균)
                        pelvis_x = (xy_values.flatten()[22] + xy_values.flatten()[24]) / 2

                        # 왼발 X좌표
                        left_foot_x = xy_values.flatten()[30]

                        # 오른발 X좌표
                        right_foot_x = xy_values.flatten()[32]
                        print(f'pelvis_x: {pelvis_x}, left_foot_x: {left_foot_x}, right_foot_x: {right_foot_x}')

                        # 조건 확인
                        if left_foot_x > pelvis_x and right_foot_x > pelvis_x:
                            bcount += 0.5
                            direction = 1
                        else:
                            # 에러 이미지 저장
                            error_dir = "errors"
                            if not os.path.exists(error_dir):
                                os.makedirs(error_dir)
                            error_files = sorted(
                                [f for f in os.listdir(error_dir) if f.startswith("error") and f.endswith(".png")])
                            if error_files:
                                last_error_num = int(error_files[-1][5:-4])  # "error" 뒤와 ".png" 앞의 숫자 추출
                                error_filename = f"error{last_error_num + 1}.png"
                            else:
                                error_filename = "error0.png"
                            cv2.imwrite(os.path.join(error_dir, error_filename), frame)
                if percentage <= 5:
                    if direction == 1:
                        bcount += 0.5
                        direction = 0

                # 카운트 박스 그리기
                im_pil = Image.fromarray(frame)
                box_color = (204, 204, 255)  # Periwinkle
                draw = ImageDraw.Draw(im_pil)
                box_x1, box_y1 = fw - 150, fh - 150
                box_x2, box_y2 = fw - 50, fh - 50
                draw.rounded_rectangle((box_x1, box_y1, box_x2, box_y2), fill=box_color, radius=20)

                # bcount 값을 중앙에 표시
                font_size = 40
                font_color = (0, 0, 0)  # Black
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()

                text = str(int(bcount))
                # 텍스트 크기 계산
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                text_x = box_x1 + (box_x2 - box_x1 - text_width) // 2
                text_y = box_y1 + (box_y2 - box_y1 - text_height) // 2
                draw.text((text_x, text_y), text, font=font, fill=font_color)

                # PIL 이미지를 다시 OpenCV 이미지로 변환
                frame = np.array(im_pil)

    # 결과 프레임을 출력 비디오에 쓰기
    out.write(frame)

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()
#######################################################################################################################