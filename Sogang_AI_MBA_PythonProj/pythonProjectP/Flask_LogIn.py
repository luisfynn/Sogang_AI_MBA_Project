from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from datetime import timedelta
from functools import wraps
import logging
from flask import jsonify
########################################################################################################################
# add library
import threading
import queue
import uuid
from yolo_pose_pushup import pushUpProcessVideo
from yolo_pose_squart import squartProcessVideo
from flask import send_file
# log
from datetime import datetime
# bert
from transformers import BertTokenizer, BertForSequenceClassification
from bert_sentences import bertPredict
########################################################################################################################
# Flask app configuration
app = Flask(__name__, static_folder='static')
app.secret_key = 'practicom'  # Secret key for session management
bcrypt = Bcrypt(app)

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
UPLOAD_FOLDER = f'upload/defaultUpload'
PUSHUP_UPLOAD_FOLDER = f'upload/pushUpUpLoad'
SQUART_UPLOAD_FOLDER = f'upload/squartUpLoad'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PUSHUP_UPLOAD_FOLDER'] = PUSHUP_UPLOAD_FOLDER
app.config['SQUART_UPLOAD_FOLDER'] = SQUART_UPLOAD_FOLDER
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
            return redirect(url_for('schedule_file'))
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
            {'name': '1회 푸쉬업', 'usage': '대회창업', 'period': '2024.06.30 ~ 2024.08.31', 'remarks': '푸쉬업 페이지 바로가기'}, # 수정
            {'name': '2회 스쿼트', 'usage': 'something new', 'period': '2024.07.30 ~ 2024.08.31', 'remarks': '스쿼트 페이지 바로가기'}, # 수정
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
                return render_template('upload.html')
            ###########################################################################################################

            return redirect(url_for('uploaded_files_list'))
    return render_template('upload.html')

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
                return render_template('uploadPushUp.html')
            ###########################################################################################################

            return redirect(url_for('pushup_uploaded_files_list'))
    return render_template('uploadPushUp.html')

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
                return render_template('uploadSquart.html')
            ###########################################################################################################

            return redirect(url_for('squart_uploaded_files_list'))
    return render_template('uploadSquart.html')

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
    return render_template('uploaded.html', files=video_urls)

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
    return render_template('uploadedPushUp.html', files=video_urls)

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
    return render_template('uploadedSquart.html', files=video_urls)



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
    # 여기에서 my page 페이지에 필요한 데이터를 처리
    return render_template('my_page.html')

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

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5002)
    app.run(debug=True)