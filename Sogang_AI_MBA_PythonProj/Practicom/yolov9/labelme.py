# yolo v9 다운로드 후 하기 경로의 hyp.scratch-high.yaml을 그대로 복사해서 hyp.scratch-low.yaml 만들기
# C:\Users\luisf\OneDrive\바탕 화면\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\Practicom\yolov9\data\hyps\hyp.scratch-high.yaml
# AI-Hub에서 다운로드 받은 한국 음식 이미지를 labelme를 사용하여 라벨링
# labelme 설치 및 사용법 가이드 : https://www.anaconda.com/download/success

# 아나콘다 설치후
# 아나콘다 프롬프트 실행하여 하기 코드 입력
# conda create --name=labelme python=3
# conda activate labelme
# pip install labelme
# [주의]위 설치시 인코딩 에러 발생시 아나콘다 프롬프트에 set PYTHONUTF8=1 입력 후 pip install labelme 실행
# [주의]아나콘다 프롬프트 닫기 후 재실행시 conda activate labelme 입력 후 명령어 입력 필요
# # or install standalone executable/app from:
# # https://github.com/wkentaro/labelme/releases

#######################################################################################################################
# 라벨링된 파일을 yolo format으로 변환
# yolo format : <object-class> <x_center> <y_center> <width> <height>
import json
import os

def convert_json_to_yolo(json_file, output_dir):
    with open(json_file, 'r') as file:
        data = json.load(file)

    image_path = data['imagePath']
    image_name = os.path.splitext(os.path.basename(image_path))[0]
    image_width = data['imageWidth']
    image_height = data['imageHeight']

    yolo_file_path = os.path.join(output_dir, f'{image_name}.txt')

    with open(yolo_file_path, 'w') as file:
        for shape in data['shapes']:
            label = shape['label']
            # 각 라벨에 해당하는 class_id를 설정해야 함, 예시에서는 'mandu'를 0으로 가정
            class_id = 0 if label == 'mandu' else 1

            points = shape['points']
            x1, y1 = points[0]
            x2, y2 = points[1]

            # 좌표를 YOLO 포맷으로 변환
            x_center = ((x1 + x2) / 2) / image_width
            y_center = ((y1 + y2) / 2) / image_height
            width = abs(x2 - x1) / image_width
            height = abs(y2 - y1) / image_height

            file.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

def process_directory(json_dir, output_dir):
    json_files = [os.path.join(json_dir, f) for f in os.listdir(json_dir) if f.endswith('.json')]
    for json_file in json_files:
        convert_json_to_yolo(json_file, output_dir)
        print(f"Processed {json_file}")

# JSON 파일 디렉토리와 출력 디렉토리 지정
json_directory = r'C:\Users\luisf\OneDrive\바탕 화면\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\Practicom\yolov9\food_example'
output_directory = r'C:\Users\luisf\OneDrive\바탕 화면\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\Practicom\yolov9\food_example\yolo_format'

# 디렉토리 처리 실행
process_directory(json_directory, output_directory)


#######################################################################################################################
# 훈련 및 검증 데이터셋 준비
import os
import glob

def prepare_dataset(image_dir, output_dir):
    images = glob.glob(os.path.join(image_dir, '*.jpg'))
    train_file = os.path.join(output_dir, 'train.txt')
    valid_file = os.path.join(output_dir, 'valid.txt')

    with open(train_file, 'w') as tr, open(valid_file, 'w') as val:
        for i, image_path in enumerate(images):
            if i % 5 == 0:  # 간단한 예로, 5개 중 1개 파일을 검증 데이터로 사용
                val.write(image_path + '\n')
            else:
                tr.write(image_path + '\n')


# 예제 실행
prepare_dataset(json_directory, output_directory)

#######################################################################################################################
# yolo 학습
# terminal에서

# python yolov9/train.py --img 640 --batch 16 --epochs 50 --data "C:\Users\luisf\OneDrive\바탕 화면\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\Practicom\yolov9\food_dataset.yaml" --cfg "yolov9/models/detect/yolov9-e.yaml" --weights "yolov9-e-converted.pt"