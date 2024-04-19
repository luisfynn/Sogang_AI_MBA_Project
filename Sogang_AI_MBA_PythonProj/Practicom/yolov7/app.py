# default library
import os
import sys
import pandas as pd
import numpy as np
import time
from PIL import ImageFont, ImageDraw, Image
import copy
import shutil

# flask library
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import Flask, request, redirect, url_for, render_template

# opencv & torch, tensorflow
import cv2
import torch
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf

# pose estimation(library 상세 분석 할 것!!)
from models.experimental import attempt_load
from utils.torch_utils import select_device
from utils.torch_utils import select_device
from utils.datasets import letterbox
from utils.plots import output_to_keypoint, plot_skeleton_kpts
from utils.general import non_max_suppression_kpt, strip_optimizer
from torchvision import transforms
from trainer import findAngle
from trainer import findHeight

# face recognition
# mmod_human_face_detector.dat<---학습 모델
# dlib 설치 가이드
# pip install cmake
# git clone https://github.com/davisking/dlib.git
# cd dlib
# python setup.py install

# 학습된 모델 불러오기(참조코드)
# pip install keras h5py
# from keras.models import load_model
# # Replace 'path_to_your_model' with the actual path to your HDF5 file
# model_path = 'path_to_your_model/model1-aug-1000-batch-32.hdf5'
# network = load_model(model_path)
# # Print the model summary
# network.summary()
# # Check the type of the model
# print(type(network))
# 참조링크 : https://github.com/amineHorseman/facial-expression-recognition-using-cnn
# 참조링크: https://github.com/petercunha/Emotion/blob/master/emotions.py#L4
# 참조링크: https://github.com/BaekKyunShin/Computer-Vision-Basic/blob/main/Project3-Emotion_Classification/Emotion_Classification_in_Video.ipynb
import dlib
from keras.models import load_model
import cv2
import numpy as np
from statistics import mode
from keras.models import load_model
from Emotionutils.datasets import get_labels
from Emotionutils.inference import detect_faces
from Emotionutils.inference import draw_text
from Emotionutils.inference import draw_bounding_box
from Emotionutils.inference import apply_offsets
from Emotionutils.inference import load_detection_model
from Emotionutils.preprocessor import preprocess_input

# Flask app configuration
app = Flask(__name__)

app.secret_key = 'practicom'  # Secret key for session management

# Configuration for user data and upload paths
USERS_CSV = 'users.csv'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'jpg'}
POSE_TRAINED = "yolov7-w6-pose.pt"
USE_GPU = "cuda"

global users_df

# Initialize or load users data
if os.path.exists(USERS_CSV):
    users_df = pd.read_csv(USERS_CSV)
else:
    users_df = pd.DataFrame(columns=['username', 'password_hash'])

# Home page
@app.route('/')
def index():
    return render_template('mainPage.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    global users_df  # This should ideally be avoided; consider using a database or a different design pattern

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users_df['username'].values:
            flash('Username already exists.')
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        # Add a new row to DataFrame with the next index
        new_index = users_df.index.max() + 1 if not users_df.empty else 0
        users_df.loc[new_index] = [username, password_hash]

        users_df.to_csv(USERS_CSV, index=False)
        flash('User registered successfully.')
        return redirect(url_for('login'))

    return render_template('registerPage.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_row = users_df[users_df['username'] == username]
        if not user_row.empty and check_password_hash(user_row.iloc[0]['password_hash'], password):
            session['username'] = username
            flash('Logged in successfully.')
            return redirect(url_for('schedule_file'))
        flash('Invalid username or password.')
    return render_template('mainPage.html')

# User logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

# Schedule and file management
@app.route('/schedule', methods=['GET', 'POST'])
def schedule_file():
    schedule_data = {
        'important_dates': [
            {'name': '행사명', 'usage': '내용', 'period': '기간', 'remarks': '비고'},
            {'name': '1회 스페셜데이', 'usage': '대회창업', 'period': '2024.06.30 ~ 2024.08.31', 'remarks': '참여링크'},
            {'name': '2회 무엇가', 'usage': 'something new', 'period': '2024.07.30 ~ 2024.08.31', 'remarks': '참여링크'},
        ],
        'general_dates': [
            {'name': '일반일정', 'usage': '내용', 'period': '기간', 'remarks': '컬럼'},
            {'name': '어떤일정', 'usage': '일정 내용', 'period': '2024.04.30 ~ 2024.05.31', 'remarks': '순위확인'},
        ]
    }
    return render_template('schedule.html', data=schedule_data)

# File upload
@app.route('/uploadFiles', methods=['GET', 'POST'])
def upload_file():
    # 앱이 위치한 경로를 기준으로 작업 디렉토리 변경
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if request.method == 'POST':
        file = request.files.get('video', None)
        if file and file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Attempting to save file to {save_path}")  # 파일 저장 경로 로깅
            file.save(save_path)
            print(f"File saved to {save_path}")  # 파일 저장 경로 로깅
            yolo_pose_detection()
            return redirect(url_for('uploaded_files_list'))
    return render_template('upload.html')

@app.route('/uploads')
def uploaded_files_list():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
    # Generate the full URL for the files, including the filename
    files_urls = [url_for('uploaded_file', filename=file) for file in files]
    print(f"uploaded_files_list:{files_urls}")
    return render_template('uploaded.html', files=files_urls)

# Serve individual uploaded files
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # safe_path = safe_join(app.config['UPLOAD_FOLDER'], filename)
    # return send_from_directory(app.config['UPLOAD_FOLDER'], safe_path, as_attachment=False)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# run yolo pose detection
# @app.route('/upload-video', methods=['POST'])
def yolo_pose_detection():
    if 'video' not in request.files: # 요청에 'video'라는 이름의 파일이 포함되어 있는지 확인 후, 없으면 request.url로 리다이렉션
        print("video not in request")
        return redirect(request.url)
    video = request.files['video']
    print(f"run pose_detection: {video.filename}")
    if video.filename == '':
        return redirect(request.url)
    if video and allowed_file_mp4(video.filename):
        filename = secure_filename(video.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # video.save(video_path)
        # yolov9-c-converted.pt와 사용자 정의 함수를 호출
        process_video(video_path)
        return redirect(url_for('uploaded_files_list'))
    return 'File upload error'

# GPU 설정 가이드 : https://neulvo.tistory.com/466
# @torch.no_grad(): 해당 함수의 컨텍스트 내에서 모든 연산이 gradient 계산을 수행하지 않도록 설정
# 메모리 절약: 모델을 평가하거나 추론을 할 때는 그래디언트를 계산할 필요가 없습니다. 그래디언트를 저장하지 않음으로써 사용되는 메모리 양을 줄일 수 있습니다.
# 계산 효율 증가: 그래디언트 계산이 필요 없을 때는 연산 속도가 빨라집니다. 이는 특히 모델을 평가하거나 실제 운영 환경에서 모델을 사용할 때 중요합니다.
# 버그 방지: 모델 학습 단계가 아닌, 평가나 테스트 단계에서는 실수로라도 그래디언트가 업데이트 되는 것을 방지합니다.
# emotion 감지 기능 추가
@torch.no_grad()
def run(poseweights, source, drawskeleton=True, **kwargs):
    # 각 인자에 대한 기본값 설정
    pushuptracker = kwargs.get('pushuptracker', False)
    curltracker = kwargs.get('curltracker', False)

    path = source
    ext = path.split('/')[-1].split('.')[-1].strip().lower()

    input_path = int(path) if path.isnumeric() else path

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 모션 인식 모델 로딩
    model = attempt_load(poseweights, map_location=device)
    _ = model.eval()

    # 비디오 처리
    cap = cv2.VideoCapture(input_path)
    webcam = False

    if (cap.isOpened() == False):
        print('Error while trying to read video. Please check path again')

    fw, fh = int(cap.get(3)), int(cap.get(4))
    if ext.isnumeric():
        print(f"webcam run")
        webcam = True
        fw, fh = 1280, 768
    vid_write_image = letterbox(cap.read()[1], (fw), stride=64, auto=True)[0]
    resize_height, resize_width = vid_write_image.shape[:2]
    print(f"resize_height:{resize_height}")
    # resize_height = 720

    out_video_name = "output" if path.isnumeric() else f"{input_path.split('/')[-1].split('.')[0]}"
    out = cv2.VideoWriter(f"{out_video_name}_kpt.mp4", cv2.VideoWriter_fourcc(*'H264'), 29.97, (resize_width, resize_height))
    if webcam:
        out = cv2.VideoWriter(f"{out_video_name}_kpt.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (fw, fh))

    frame_count, total_fps = 0, 0
    bcount = 0
    direction = 0

    # Load custom font
    fontpath = "sfpro.ttf"
    font = ImageFont.truetype(fontpath, 32)
    font1 = ImageFont.truetype(fontpath, 170)

    while cap.isOpened:
        # print(f"Frame {frame_count} Processing")
        ret, frame = cap.read()

        if not ret:
            break

        # 모션 인식 이미지 처리
        orig_image = frame
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        if webcam:
            image = cv2.resize(image, (fw, fh), interpolation=cv2.INTER_LINEAR)
        image = letterbox(image, (fw),stride=64, auto=True)[0]
        image = transforms.ToTensor()(image)
        image = torch.tensor(np.array([image.numpy()]))

        image = image.to(device)
        image = image.float()
        start_time = time.time()

        with torch.no_grad():
            output, _ = model(image)

        output = non_max_suppression_kpt(output, 0.5, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)
        output = output_to_keypoint(output)
        img = image[0].permute(1, 2, 0) * 255
        img = img.cpu().numpy().astype(np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if curltracker == True:
            for idx in range(output.shape[0]):
                kpts = output[idx, 7:].T #output(keypoint)의 7번째 값부터 끝까지 kpts에 저장
                #print(f"kpts:{kpts}")
                # Right arm =(5,7,9), left arm = (6,8,10)
                # set draw=True to draw the arm keypoints.
                angle = findAngle(img, kpts, 5, 7, 9, draw=False) #from trainer import findAngle 함수 참조
                #print(f"angle: {angle}") #펼친 상태에서 360도, 굽히면 0
                percentage = np.interp(angle, (10, 150), (100, 0)) #팔을 굽히면(10도) 100%, 팔을 펴면(150도) 0% (검증 필요함)
                bar = np.interp(angle, (20, 150), (200, fh-100))

                color = (254, 118, 136)
                # check for the bicep curls
                if percentage == 100:
                    if direction == 0:
                        bcount += 0.5
                        direction = 1
                if percentage == 0:
                    if direction == 1:
                        bcount += 0.5
                        direction = 0

                # draw Bar and counter
                cv2.line(img, (100, 200), (100, fh-100),
                         (255, 255, 255), 30)
                cv2.line(img, (100, int(bar)),
                         (100, fh-100), color, 30)

                #시작점 (x,y)좌표와 종료점 (x,y) 좌표를 동일하게 수정
                # % 표시가 되는 직선
                if (int(percentage) < 10):
                    #cv2.line(img, (155, int(bar)), (190, int(bar)), (254, 118, 136), 40)
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                elif (int(percentage) >= 10 and (int(percentage) < 100)):
                    #cv2.line(img, (155, int(bar)), (200, int(bar)), (254, 118, 136), 40)
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                else:
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)

                im = Image.fromarray(img)
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle((fw-280, (fh//2)-100, fw-80, (fh//2)+100), fill=color,
                                       radius=40)

                draw.text(
                    (145, int(bar)-17), f"{int(percentage)}%", font=font, fill=(255, 255, 255))
                draw.text(
                    (fw-228, (fh//2)-101), f"{int(bcount)}", font=font1, fill=(255, 255, 255))
                img = np.array(im)

        if pushuptracker == True:
            # print(f"run pushup tracker")
            for idx in range(output.shape[0]):
                kpts = output[idx, 7:].T #output(keypoint)의 7번째 값부터 끝까지 kpts에 저장
                #print(f"kpts:{kpts}")

                # Right arm =(5,7,9), left arm = (6,8,10)
                # set draw=True to draw the arm keypoints.
                angle = findAngle(img, kpts, 5, 7, 9, draw=False) #from trainer import findAngle 함수 참조
                percentage = np.interp(angle, (100, 160), (100, 0)) #팔을 굽히면(100도 이하) 100%, 팔을 펴면(160도 이상) 0%
                bar = np.interp(angle, (100, 160), (200, fh-100))
                print(f"angle: {angle}, percent: {percentage}, bar: {bar}, fh: {fh}")

                color = (254, 118, 136)
                # check for the bicep curls
                if percentage >= 90:
                    if direction == 0:
                        bcount += 0.5
                        direction = 1
                if percentage <=  10:
                    if direction == 1:
                        bcount += 0.5
                        direction = 0

                # draw Bar and counter
                cv2.line(img, (100, 200), (100, fh-100),
                         (255, 255, 255), 30)
                cv2.line(img, (100, int(bar)),
                         (100, fh-100), color, 30)

                #시작점 (x,y)좌표와 종료점 (x,y) 좌표를 동일하게 수정
                # % 표시가 되는 직선
                if (int(percentage) < 10):
                    #cv2.line(img, (155, int(bar)), (190, int(bar)), (254, 118, 136), 40)
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                elif (int(percentage) >= 10 and (int(percentage) < 100)):
                    #cv2.line(img, (155, int(bar)), (200, int(bar)), (254, 118, 136), 40)
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                else:
                    cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)

                im = Image.fromarray(img)
                draw = ImageDraw.Draw(im)
                draw.rounded_rectangle((fw-280, (fh//2)-100, fw-80, (fh//2)+100), fill=color,
                                       radius=40)

                draw.text(
                    (145, int(bar)-17), f"{int(percentage)}%", font=font, fill=(255, 255, 255))
                draw.text(
                    (fw-228, (fh//2)-101), f"{int(bcount)}", font=font1, fill=(255, 255, 255))
                img = np.array(im)

        if drawskeleton:
            for idx in range(output.shape[0]):
                plot_skeleton_kpts(img, output[idx, 7:].T, 3)

        if webcam:
            cv2.imshow("Detection", img)
            key = cv2.waitKey(1)
            if key == ord('c'):
                break
        else:
            img_ = img.copy()
            img_ = cv2.resize(img_, (960, 540), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Detection", img_)
            cv2.waitKey(1)

        end_time = time.time()
        fps = 1 / (end_time - start_time)
        total_fps += fps
        frame_count += 1
        out .write(img)  # 이미지 데이터를  비디오 파일에 기록

    cap.release()
    out.release()
    avg_fps = total_fps / frame_count
    print(f"Average FPS: {avg_fps:.3f}")
    emotion_process_video(f"{out_video_name}_kpt.mp4")


def emotion_process_video(video_filename):
    print(f"video_filename: {video_filename}")

    # 업로드 폴더 경로 가져오기
    upload_folder = app.config['UPLOAD_FOLDER']

    # 업로드 폴더 확인 및 생성
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # 모델과 얼굴 감지기 로드
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    model_path = 'model1-aug-1000-batch-32.hdf5'
    network = load_model(model_path)

    # getting input model shapes for inference
    emotion_target_size = network.input_shape[1:3]

    # 모델 컴파일
    network.compile(optimizer='adam',
                  loss='categorical_crossentropy',  # 다중 클래스 분류 문제에 적합한 손실 함수
                  metrics=['accuracy'])  # 평가 지표로 정확도 사용
    cnn_face_detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')

    # 색상 및 감정 리스트
    green_color = (0, 255, 0)
    red_color = (0, 0, 255)
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # hyper-parameters for bounding boxes shape
    frame_window = 10
    emotion_offsets = (20, 40)

    # starting lists for calculating modes
    emotion_window = []

    # 원본 비디오를 복사하여 처리할 파일 생성
    video_filename_SPLIT = video_filename.split('\\')[1]
    print(f"emotion_process_video_video_filename:{video_filename_SPLIT}")
    temp_video_filename = f"temp_{video_filename_SPLIT}"
    print(f"temp_video_filename:{temp_video_filename}")
    temp_video_path = os.path.join(upload_folder, temp_video_filename)
    print(f"temp_video_path:{temp_video_path}")
    shutil.copy(video_filename, temp_video_path)

    # 비디오 파일 열기
    cap = cv2.VideoCapture(temp_video_path)
    fw = int(cap.get(3))
    fh = int(cap.get(4))
    out_video_filename = f"{video_filename.split('.')[0]}_emotions.mp4"
    out = cv2.VideoWriter(out_video_filename, cv2.VideoWriter_fourcc(*'H264'), 29.97, (fw, fh))

    try:
        # 비디오 프레임 처리
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5,
                                                  minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for face_coordinates in faces:
                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = network.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                emotion_text = emotions[emotion_label_arg]
                emotion_window.append(emotion_text)

                print(f"emotion_text: {emotion_text}")

                # 텍스트를 프레임에 추가
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, f'Emotion: {emotion_text}', (150, 150), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            out.write(frame)
    finally:
        cap.release()
        out.release()
        print(f"Processed video saved as {out_video_filename}")

        # 파일 이동
        # shutil.move(out_video_filename, os.path.join(app.config['UPLOAD_FOLDER'], out_video_filename))
        # print(f"Video moved to upload_folder")

        # 임시 복사 파일 삭제
        os.remove(temp_video_path)

        # blur 처리 추가
        blur_faces(out_video_filename)


def blur_faces(in_video_filename):
    print("run blur")
    # 캐스케이드 분류기 로드
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # 비디오 파일 읽기
    cap = cv2.VideoCapture(in_video_filename)
    if not cap.isOpened():
        print(f"Error opening video file {in_video_filename}")
        return

    # 출력 비디오 설정
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    out = cv2.VideoWriter(f"{in_video_filename.split('.')[0]}_blurred.mp4", fourcc, cap.get(cv2.CAP_PROP_FPS),
                          (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 흑백 이미지로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴 감지
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # 감지된 얼굴 블러 처리
        for (x, y, w, h) in faces:
            roi = frame[y:y + h, x:x + w]
            roi = cv2.GaussianBlur(roi, (23, 23), 30)
            frame[y:y + h, x:x + w] = roi

        # 변형된 프레임을 출력 비디오에 쓰기
        out.write(frame)

    # 자원 해제
    cap.release()
    out.release()

def process_video(video_path):
    # run 함수 호출
    run(POSE_TRAINED, video_path, drawskeleton=True, pushuptracker=True, curltracker=False)

def allowed_file_mp4(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)