# library 불러오기
import shutil
import os
import mediapipe as mp
import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from torchvision.ops import nms
import torch
# drawing
from PIL import ImageFont, ImageDraw, Image
import math
#######################################################################################################################
# pushup
def findAngle(image, kpts, p1,p2,p3, draw= True):
    coord = []
    no_kpt = len(kpts)//2
    for i in range(no_kpt):
        cx,cy = kpts[2*i], kpts[2*i +1]
        coord.append([i, cx, cy])

    points = (p1,p2,p3)

    # =3.1=Get landmarks========
    x1,y1 = coord[p1][1:3]
    print(f"x1:{x1},y1:{y1}")
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]

    # =3.2=Calculate the Angle========
    angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2, x1-x2))

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
# filename = "How to do a Push-Up _ Proper Form & Technique _ NASM.mp4"
filename = "pushup2.mp4"
# filename = "pushup1.mp4"
# filename = "mp4/KakaoTalk_20240520_065611169.mp4"
cap = cv2.VideoCapture(filename)
subject = filename.split('.')[0]

# 비디오 파일의 속성 읽기
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# 출력 비디오 파일 설정
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(f"{subject}_output.mp4", fourcc, fps, (width, height))

# 카운트 변수 및 방향 변수 초기화
bcount = 0
bfail = 0
direction = 0
H_SIDE = 0
MIN_ANGLE = 70
MAX_ANGLE = 140
MIN_PERCENT = 10
MAX_PERCENT = 90
angle_list = []
direction_list = []
percent_list = []
initangle_list = []
init_angle = 180

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

    # frame 사이즈 확인
    im_pil = Image.fromarray(frame)
    fw, fh = im_pil.size

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
                # print(f"xy_values :{xy_values}")

                # 골격과 키포인트를 프레임에 그리기
                plot_skeleton_kpts(frame, xy_values.flatten(), steps=2)

                # 키포인트를 프레임에 그리기
                for point in xy_values[0]:  # xy_values[0]을 사용하여 각 프레임의 키포인트 배열에 접근
                    x, y = point
                    # print("xy_point:", point)

                    if x > 0 and y > 0:  # 유효한 좌표만 표시
                        cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 0), -1)  # 파란색 원 그리기

                # 주요 keypoint 각도 측정
                # 사람의 어느 측면이 잘보이는지 확인
                # left_foot_x = xy_values.flatten()[30]                   # 왼발 X좌표
                # right_foot_x = xy_values.flatten()[32]                  # 오른발 X좌표
                left_arm_x = xy_values.flatten()[18]                     # 왼손 X좌표
                right_arm_x = xy_values.flatten()[20]                    # 오른손 X좌표
                left_knee_x = xy_values.flatten()[26]                     # 왼쪽 무릎 X좌표
                right_knee_x = xy_values.flatten()[28]                    # 오른쪽 무릎 X좌표

                print(f"H_SIDE :{H_SIDE}")

                if H_SIDE == 0:
                    if left_arm_x < left_knee_x:
                        H_SIDE = 1
                    else:
                        H_SIDE = 2

                if H_SIDE == 1:
                    # 왼팔 각도 측정
                    angle_arm = findAngle(frame, xy_values.flatten(), 5, 7, 9, draw=False)
                    print(f'H_SIDE:{H_SIDE} angle_arm: {angle_arm}')
                    # angle_arm 보정
                    angle_arm = 360 - angle_arm
                    if angle_arm > 360:
                        angle_arm -= 360
                else:
                    # 오른팔 각도 측정
                    angle_arm = findAngle(frame, xy_values.flatten(), 6, 8, 10, draw=False)
                    print(f'H_SIDE:{H_SIDE} angle_arm: {angle_arm}')

                # percent 표기
                percentage = np.interp(angle_arm, (MIN_ANGLE, MAX_ANGLE), (100, 0))  # angle_arm의 각도로 퍼센트 측정
                bar = np.interp(angle_arm, (MIN_ANGLE, MAX_ANGLE), (200, fh - 300))
                print(f'angle_arm: {angle_arm}, percentage: {percentage}, bar: {bar}')

                # percentage 바 그리기
                percent_color = (64, 224, 208)  # Turquoise
                cv2.line(frame, (100, 200), (100, fh - 300), (255, 255, 255), 30)
                cv2.line(frame, (100, int(bar)), (100, fh - 300), percent_color, 30)

                percentage = round(percentage, 0)
                # 텍스트 추가 (percentage)
                text = f"{percentage}%"
                font_scale = 0.8
                font_thickness = 2
                text_color = (64, 224, 208)  # Turquoise
                bg_color = (204, 204, 255)  # Periwinkle
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

                # 카운트 박스 그리기 및 bcount 값을 중앙에 표시
                text = f"{int(bcount)}"
                font_scale = 0.8
                font_thickness = 2
                font_color = (64, 224, 208)  # Turquoise
                box_color = (204, 204, 255)  # Periwinkle
                font = cv2.FONT_HERSHEY_SIMPLEX

                # 텍스트 크기 계산
                (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)
                # box_x1, box_y1 = fw - 150, fh - 150
                # box_x2, box_y2 = fw - 50, fh - 50
                box_x1, box_y1 = 50, 50
                box_x2, box_y2 = 150, 150

                # 텍스트 배경 박스 그리기
                cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), box_color, cv2.FILLED)

                # 텍스트 위치 계산
                text_x = box_x1 + (box_x2 - box_x1 - text_width) // 2
                text_y = box_y1 + (box_y2 - box_y1 + text_height) // 2

                # 텍스트 그리기
                cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

                # 디버그 로그 데이터 기록
                angle_list.append(angle_arm)
                direction_list.append(direction)
                percent_list.append(percentage)
                initangle_list.append(init_angle)

                # 스쿼트 카운트 측정
                percentage = np.interp(angle_arm, (MIN_ANGLE, MAX_ANGLE), (100, 0))  # angle_arm의 각도로 퍼센트 측정

                if percentage >= MAX_PERCENT:
                    if direction == 0:
                        bcount += 0.5
                        direction = 1
                elif percentage <= MIN_PERCENT:
                    if direction == 1:
                        bcount += 0.5
                        direction = 0
                else:
                    print("")

                print(f'bcount: {bcount}, bfail: {bfail}, direction: {direction}')
                # 성공 및 실패 카운트 표기
                # 카운트 박스 그리기 및 bcount, bfail 값을 중앙에 표시
                box_color = (204, 204, 255)
                font_color = (0, 0, 255)
                font_scale = 1.0
                font_thickness = 2
                font = cv2.FONT_HERSHEY_SIMPLEX

                box_width = 200
                box_height = 100
                box_x1 = fw - box_width - 10
                box_y1 = fh - box_height - 10
                box_x2 = fw - 10
                box_y2 = fh - 10

                cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), box_color, cv2.FILLED)

                bcount_text = f"{int(bcount)}"
                (text_width, text_height), baseline = cv2.getTextSize(bcount_text, font, font_scale, font_thickness)
                text_x = box_x1 + (box_width - text_width) // 2
                text_y = box_y1 + text_height + 10

                cv2.putText(frame, bcount_text, (text_x, text_y), font, font_scale, font_color, font_thickness)

                bfail_text = f"{bfail}"
                (text_width, text_height), baseline = cv2.getTextSize(bfail_text, font, font_scale, font_thickness)
                text_x = box_x1 + (box_width - text_width) // 2
                text_y = box_y1 + text_height + 10 + 50

                cv2.putText(frame, bfail_text, (text_x, text_y), font, font_scale, font_color, font_thickness)
    # 결과 프레임을 출력 비디오에 쓰기
    out.write(frame)

# 리소스 해제
cap.release()
out.release()
cv2.destroyAllWindows()

# debug log
angle_df = pd.DataFrame({"direction": direction_list, "angle": angle_list, "percent_list":percent_list, "init_angle":initangle_list})
angle_df.to_csv("datalog.csv", encoding='cp949', index=False)