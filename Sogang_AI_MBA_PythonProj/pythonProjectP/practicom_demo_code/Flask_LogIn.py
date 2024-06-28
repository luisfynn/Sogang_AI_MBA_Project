from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
import pandas as pd
import os
import platform
from datetime import timedelta
from functools import wraps
import logging
from flask import jsonify
import torch
########################################################################################################################
# add library
import threading
import queue
import uuid

import Calculation
import Visualization
from yolo_pose_pushup import pushUpProcessVideo
from yolo_pose_squart import squartProcessVideo
from flask import send_file
# log
from datetime import datetime
# bert
from transformers import BertTokenizer, BertForSequenceClassification
from bert_sentences import bertPredict
#face
from face import face_detector
from PIL import Image
#food
from Calculation import get_image, get_labels_and_sizes, get_size_by_label, get_nutritional_info, get_total
from Visualization import draw_and_save_image, draw_bar_chart

import subprocess
import json
########################################################################################################################

# Flask app configuration
app = Flask(__name__, static_folder='static')
app.secret_key = 'practicom'  # Secret key for session management
bcrypt = Bcrypt(app)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_BINDS'] = {
    'user': 'sqlite:///user.db',
    'diary': 'sqlite:///diary.db',
    'challenges': 'sqlite:///challenges.db'
}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)

# Connect to the databases
db = SQLAlchemy(app)

# Configuration for user data and upload paths
#######################################################################################################################
# 수정

base_dir = '/home/ubuntu/uploads' if platform.system() == 'Linux' else 'C:/python/pythonProjectP/uploads'

UPLOAD_FOLDER = os.path.join(base_dir, 'defaultUpload')
PUSHUP_UPLOAD_FOLDER = os.path.join(base_dir, 'pushUpUpLoad')
SQUART_UPLOAD_FOLDER = os.path.join(base_dir, 'squartUpLoad')
FACE_UPLOAD_FOLDER = os.path.join(base_dir, 'faceUpLoad')
FOOD_UPLOAD_FOLDER = os.path.join(base_dir, 'foodUpLoad')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PUSHUP_UPLOAD_FOLDER'] = PUSHUP_UPLOAD_FOLDER
app.config['SQUART_UPLOAD_FOLDER'] = SQUART_UPLOAD_FOLDER
app.config['FACE_UPLOAD_FOLDER'] = FACE_UPLOAD_FOLDER
app.config['FOOD_UPLOAD_FOLDER'] = FOOD_UPLOAD_FOLDER

#######################################################################################################################
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'jpg'}

class User(db.Model):
    __bind_key__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(50), nullable=True)  # 새로운 필드 추가

# 추가
class FaceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(50), nullable=True)  # 새로운 필드 추가

class Challenge(db.Model):
    __bind_key__ = 'challenges'
    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, nullable=False)  # 도전자 ID
    opponent_id = db.Column(db.Integer, nullable=False)    # 상대방 ID
    status = db.Column(db.String(50), default='pending')   # 챌린지 상태: pending, accepted, rejected
    # 필요에 따라 다른 필드 추가 가능

# Create the databases
with app.app_context():
    db.create_all()

@app.before_request
def make_session_permanent():
    session.permanent = True

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Home page
@app.route('/')
def index():
    return render_template('mainPage.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists.')
                return redirect(url_for('register'))

            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password_hash=password_hash)
            db.session.add(new_user)
            db.session.commit()

            flash('User registered successfully.')
            return redirect(url_for('login'))

        return render_template('registerPage.html')

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = username
            flash('Logged in successfully.')
            return redirect(url_for('my_page'))
        flash('Invalid username or password.')
    return render_template('mainPage.html')

# User logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
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

# challenge_detail
@app.route('/challenge/<int:challenge_id>')
def challenge_detail(challenge_id):

    # 여기서는 challenge_id를 기반으로 데이터베이스에서 챌린지의 세부 정보를 가져와야 합니다.
    # 데이터베이스 쿼리 등을 사용하여 해당 챌린지에 대한 정보를 가져옵니다.
    # 이후 해당 정보를 템플릿으로 렌더링하여 보여줍니다.
    challenge_info = {}  # 데이터베이스 쿼리를 통해 가져온 챌린지 세부 정보
    return render_template('challenge_detail.html', challenge_info=challenge_info)


########################################################################################################################
# 추가
# 작업 큐 및 결과 저장소
task_queue = queue.Queue()
results = {}

def worker():
    while True:
        task_id, func, args = task_queue.get()
        result_df = func(*args, task_id)
        filename = f"pushup_datalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        result_df.to_csv(filename, encoding='cp949', index=False)
        task_queue.task_done()
        results[task_id] = filename

# 백그라운드에서 작업을 처리할 스레드 시작
threading.Thread(target=worker, daemon=True).start()

# 동작하지 않음
@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    if task_id in results:
        result = results[task_id]
        if result.endswith('.csv'):
            return send_file(result, mimetype='text/csv', attachment_filename=result, as_attachment=True)
        else:
            return jsonify({'error': result}), 500
    else:
        return jsonify({'error': 'Task ID not found or still processing'}), 404
# def get_result(task_id):
#     results.to_csv(f"pushup_datalog_{datetime.now()}.csv", encoding='cp949', index=False)
#     # else:
#     #     return jsonify({"status": "Processing"}), 202

@app.route('/uploadFiles', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file', None)
        if file and file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ###########################################################################################################
            # 수정 및 추가
            fname = filename.split('.')[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{fname}_{timestamp}.mp4")
            file_path = os.path.normpath(file_path)
            print(f"file_path:{file_path}")
            file_path = file_path.replace('\\', '/')
            file.save(file_path)

            # 파일 형식에 따라 처리 방법 선택
            task_id = str(uuid.uuid4())
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{fname}_{timestamp}_output.mp4")
            if file.content_type.startswith('image/'):
                task_queue.put((task_id, squartProcessVideo, [file_path])) #image 처리를 위한 함수 구현 후 변경 필요
            elif file.content_type.startswith('video/'):
                task_queue.put((task_id, squartProcessVideo, [file_path, output_path])) #pushUpProcess 함수
            else:
                return render_template('p_upload.html')
            ###########################################################################################################

            return redirect(url_for('uploaded_files_list'))
    return render_template('p_upload.html')

# File upload
@app.route('/uploadFilesPushUp', methods=['GET', 'POST'])
def upload_filePushUp():
    if request.method == 'POST':
        file = request.files.get('file', None)
        if file and file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ###########################################################################################################
            # 수정 및 추가
            fname = filename.split('.')[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            print(f"fname:{fname}")
            file_path =  os.path.join(app.config['PUSHUP_UPLOAD_FOLDER'], f"{fname}_{timestamp}.mp4")
            file_path = os.path.normpath(file_path)
            print(f"file_path:{file_path}")
            file_path = file_path.replace('\\', '/')
            file.save(file_path)

            # 파일 형식에 따라 처리 방법 선택
            task_id = str(uuid.uuid4())
            output_path =  os.path.join(app.config['PUSHUP_UPLOAD_FOLDER'], f"{fname}_{timestamp}_output.mp4")
            if file.content_type.startswith('image/'):
                task_queue.put((task_id, pushUpProcessVideo, [file_path])) #image 처리를 위한 함수 구현 후 변경 필요
            elif file.content_type.startswith('video/'):
                task_queue.put((task_id, pushUpProcessVideo, [file_path, output_path])) #pushUpProcess 함수
            else:
                return render_template('p_uploadPushUp.html')
            ###########################################################################################################

            return redirect(url_for('pushup_uploaded_files_list'))
    return render_template('p_uploadPushUp.html')

@app.route('/uploadFilesSquart', methods=['GET', 'POST'])
def upload_fileSquart():
    if request.method == 'POST':
        file = request.files.get('file', None)
        if file and file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ###########################################################################################################
            # 수정 및 추가
            fname = filename.split('.')[0]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_path = os.path.join(app.config['SQUART_UPLOAD_FOLDER'], f"{fname}_{timestamp}.mp4")
            file_path = os.path.normpath(file_path)
            file_path = file_path.replace('\\', '/')
            file.save(file_path)

            # 파일 형식에 따라 처리 방법 선택
            task_id = str(uuid.uuid4())
            output_path = os.path.join(app.config['SQUART_UPLOAD_FOLDER'], f"{fname}_{timestamp}_output.mp4")
            if file.content_type.startswith('image/'):
                task_queue.put((task_id, squartProcessVideo, [file_path])) #image 처리를 위한 함수 구현 후 변경 필요
            elif file.content_type.startswith('video/'):
                task_queue.put((task_id, squartProcessVideo, [file_path, output_path])) #pushUpProcess 함수
            else:
                return render_template('p_uploadSquart.html')
            ###########################################################################################################

            return redirect(url_for('squart_uploaded_files_list'))
    return render_template('p_uploadSquart.html')

@app.route('/upploads')
def uploaded_files_list():
    # files = os.listdir(app.config['UPLOAD_FOLDER'])
    # files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
    # # Generate the full URL for the files, including the filename
    # files_urls = [url_for('upload_file', filename=file) for file in files]
    video_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.mp4')]
    print(f"video_files:{video_files}")
    video_urls = [url_for('uploaded_file', filename=f) for f in video_files]
    print(f"video_urls:{video_urls}")
    return render_template('p_uploaded.html', files=video_urls)

@app.route('/pushUpUploads')
def pushup_uploaded_files_list():
    # files = os.listdir(app.config['PUSHUP_UPLOAD_FOLDER'])
    # files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['PUSHUP_UPLOAD_FOLDER'], x)))
    # # Generate the full URL for the files, including the filename
    # files_urls = [url_for('upload_filePushUp', filename=file) for file in files]
    video_files = [f for f in os.listdir(app.config['PUSHUP_UPLOAD_FOLDER']) if f.endswith('.mp4')]
    print(f"video_files:{video_files}")
    video_urls = [url_for('pushup_uploaded_file', filename=f) for f in video_files]
    print(f"video_urls:{video_urls}")
    return render_template('p_uploadedPushUp.html', files=video_urls)

@app.route('/squartUploads')
def squart_uploaded_files_list():
    # files = os.listdir(app.config['SQUART_UPLOAD_FOLDER'])
    # files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['SQUART_UPLOAD_FOLDER'], x)))
    # # Generate the full URL for the files, including the filename
    # files_urls = [url_for('upload_fileSquart', filename=file) for file in files]
    video_files = [f for f in os.listdir(app.config['SQUART_UPLOAD_FOLDER']) if f.endswith('.mp4')]
    print(f"video_files:{video_files}")
    video_urls = [url_for('squart_uploaded_file', filename=f) for f in video_files]
    print(f"video_urls:{video_urls}")
    return render_template('p_uploadedSquart.html', files=video_urls)



# Serve individual uploaded files
@app.route('/upload/defaultUpload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload/pushUpUpload/<filename>')
def pushup_uploaded_file(filename):
    return send_from_directory(app.config['PUSHUP_UPLOAD_FOLDER'], filename)

@app.route('/upload/squartUpLoad/<filename>')
def squart_uploaded_file(filename):
    return send_from_directory(app.config['SQUART_UPLOAD_FOLDER'], filename)
########################################################################################################################

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/mypage')
@login_required
def my_page():
    # 현재 로그인된 사용자의 이름 가져오기
    current_user = User.get_by_id(session['user_id'])
    current_username = current_user.username if current_user else 'Anonymous'

    # 여기에서 my page 페이지에 필요한 데이터를 처리
    return render_template('my_page.html', current_username=current_username)

@app.route('/challenge11')
@login_required
def challenge11():
    # 여기에서 11challenge.html 페이지에 필요한 데이터를 처리
    return render_template('11challenge.html')


@app.route('/diary', methods=['GET', 'POST'])
@login_required
def diary():
    if request.method == 'POST':
        diary_entry = request.form['diaryEntry']
        emotion = bertPredict(diary_entry)
        new_entry = DiaryEntry(content=diary_entry, emotion = emotion)
        db.session.add(new_entry)
        db.session.commit()
        flash('Diary entry added successfully.')
        return redirect(url_for('diary'))

    entries = DiaryEntry.query.all()
    return render_template('diary.html', entries=entries)

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = DiaryEntry.query.get(entry_id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('diary'))





# 챌린지 생성 기능
@app.route('/challenge11', methods=['GET', 'POST'])
@login_required
def create_challenge():
        if 'user_id' not in session:
            flash('You need to log in first.')
            return redirect(url_for('login'))

        # 11challenge 페이지에 처음 접속했을 때 모든 사용자를 추천 사용자 목록에 제공
        recommended_users = User.query.all()

        if request.method == 'POST':
            challenger_id = session['user_id']
            opponent_id = request.form.get('opponent_id')

            if not opponent_id:
                flash('Please select opponent.')
                return redirect(url_for('create_challenge'))

            if opponent_id == challenger_id:
                flash('You cannot challenge yourself.')
                return redirect(url_for('create_challenge'))

            opponent = User.get_by_id(opponent_id)  # 수정: ID로 사용자 검색
            if not opponent:
                flash('Invalid opponent.')
                return redirect(url_for('create_challenge'))

            new_challenge = Challenge(challenger_id=challenger_id, opponent_id=opponent_id)  # 수정: opponent_id로 설정
            db.session.add(new_challenge)
            db.session.commit()

            flash('Challenge created successfully.')
            return redirect(url_for('view_challenges'))

        return render_template('11challenge.html', recommended_users=recommended_users)

@app.route('/challenges')
@login_required
def view_challenges():
    user_id = session['user_id']  # 현재 로그인한 사용자의 ID를 가져옵니다.

    # 받은 챌린지
    received_challenges = Challenge.query.filter_by(opponent_id=user_id).all()
    # 신청한 챌린지
    submitted_challenges = Challenge.query.filter_by(challenger_id=user_id).all()
    # 거절한 챌린지
    rejected_challenges = Challenge.query.filter_by(challenger_id=user_id, status='rejected').all()
    return render_template('view_challenges.html', received_challenges=received_challenges,
                           submitted_challenges=submitted_challenges, rejected_challenges=rejected_challenges)
# 챌린지 수락 기능 추가
@app.route('/accept_challenge/<int:challenge_id>', methods=['POST'])
def accept_challenge(challenge_id):
    challenge = Challenge.query.get(challenge_id)
    if challenge:
        challenge.status = 'accepted'
        db.session.commit()
        flash('Challenge accepted successfully.')
    else:
        flash('Challenge not found.')
    return redirect(url_for('view_challenges'))

@app.route('/wakeup')
def wakeup():
    return render_template('wakeup.html')


# 추가
@app.route('/face', methods=['GET', 'POST'])
@login_required
def face_emotion():
    if request.method == 'POST':
        model2 = torch.hub.load('ultralytics/yolov5', 'custom', path=r'yolov5feeling/runs/train/exp4/weights/best.pt')

        if 'FaceEntry' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['FaceEntry']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename('upload_face' + os.path.splitext(file.filename)[1])
            filepath = os.path.join(app.config['FACE_UPLOAD_FOLDER'], filename)
            file.save(filepath)
            flash('File successfully uploaded')

            # Yolov5 모델을 사용하여 이미지에서 감정 예측
            results = model2(filepath)
            results.print()

            detected_classes = []
            for det in results.xyxy[0]:  # per image
                class_id = int(det[5])
                class_name = model2.names[class_id]
                detected_classes.append(class_name)
                print(f'Detected class: {class_name}')

            # 결과 이미지를 저장할 절대 경로 지정
            save_filename = 'detected_' + filename
            save_path = os.path.abspath(r'C:\python\pythonProjectP\uploads\faceUpLoad' + '\\' + save_filename)  # 여기에 저장 경로를 직접 지정해줍니다
            results.save(save_path)
            print(f'Saved detected image to: {save_path}')

            emotion = ', '.join(detected_classes)
            return render_template('wakeup.html', emotion=emotion, filename=filename)

    return render_template('wakeup.html')

@app.route('/meal', methods=['GET', 'POST'])
@login_required
def meal():
    if request.method == 'POST':
        # Load the model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=r'yolov5/runs/train/exp13/weights/best.pt')

        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['FOOD_UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # 이미지 인식 및 처리
            save_path = os.path.join(app.config['FOOD_UPLOAD_FOLDER'], 'detected.jpg')
            save_path2 = os.path.join(app.config['FOOD_UPLOAD_FOLDER'], 'graph.jpg')

            detections = Calculation.get_image(model, filepath)
            Visualization.draw_and_save_image(model, filepath, save_path)

            labels_and_sizes = Calculation.get_labels_and_sizes(detections)
            spoon_size = Calculation.get_size_by_label(labels_and_sizes, 'spoon')
            ramen_size = Calculation.get_size_by_label(labels_and_sizes, 'ramen')
            kimbab_size = Calculation.get_size_by_label(labels_and_sizes, 'kimbab')

            labelConverter = {'spoon': '스푼', 'kimbab': '김밥', 'ramen': '라면'}
            food_name_eng = detections[detections['name'] != 'spoon']['name']
            food_names = food_name_eng.apply(lambda x: labelConverter[x])

            size_ratios = dict()
            size_ratios['라면'] = ramen_size / spoon_size
            size_ratios['김밥'] = kimbab_size / spoon_size

            ref_filepath = r'C:\python\pythonProjectP\식품영양성분DB_음식_단순화_20240606.xlsx'
            df = pd.read_excel(ref_filepath)

            nutritional_info = Calculation.get_nutritional_info(df, food_names, size_ratios)
            total_nutrition = Calculation.get_total(nutritional_info)

            total_calory = total_nutrition[0]
            total_carbon = total_nutrition[1]
            total_protein = total_nutrition[2]
            total_fat = total_nutrition[3]
            total_natrium = total_nutrition[4]

            Visualization.draw_bar_chart(total_calory, total_carbon, total_protein, total_fat, total_natrium)
            # Generate bar chart
            fig = draw_bar_chart(total_calory, total_carbon, total_protein, total_fat, total_natrium)

            # Save the generated figure as an image
            bar_chart_image_path = os.path.join(app.config['FOOD_UPLOAD_FOLDER'], 'graph.jpg')
            fig.savefig(bar_chart_image_path)

            foodlist = food_names.tolist()
            weight_loss_predictions = []  # 이 부분은 계산 로직에 따라 수정해야 합니다.

            result = {
                'foodlist': foodlist,
                'total_calories': total_calory,
                'weight_loss_predictions': weight_loss_predictions,
                'image_path': r'C:\python\pythonProjectP/uploads\foodUpLoad\detected.jpg',
                'bar_chart_image_path': r'C:\python\pythonProjectP/uploads\foodUpLoad\graph.jpg' # Flask 경로 처리
            }
            result['total_calories'] = round(result['total_calories']) # 반올림



            return render_template('meal.html', result=result, total_calories=total_calory, weight_loss_predictions=weight_loss_predictions)

    return render_template('meal.html')

# 추가
@app.route('/uploads/<filename>')
def uploaded_face_file(filename):
    return send_from_directory(app.config['FACE_UPLOAD_FOLDER'], filename)
from flask import send_file

@app.route('/detected_image', methods=['GET'])
def get_detected_image():
    directory = r'C:\python\pythonProjectP\uploads\foodUpLoad'
    filename = 'detected.jpg'
    return send_from_directory(directory, filename)

@app.route('/bar_chart_image', methods=['GET'])
def get_barchart_image():
    directory = r'C:\python\pythonProjectP\uploads\foodUpLoad'
    filename = 'graph.jpg'
    return send_from_directory(directory, filename)

@app.route('/detected_faceimage', methods=['GET'])
def get_detected_faceimage():
    directory = r'C:\python\pythonProjectP\runs\detect\exp2'
    filename = 'upload_face.jpg'
    return send_from_directory(directory, filename)

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
