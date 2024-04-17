from flask import Flask, request, render_template_string, session, render_template
from flask_session import Session  # Flask-Session 확장을 사용
import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = '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'

client = OpenAI()

# Set the OpenAI API key from environment variables
client.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Flask app & session
app = Flask(__name__)
app.secret_key = 'test1'  # 애플리케이션의 비밀 키 설정
app.config['SESSION_TYPE'] = 'filesystem'  # 세션 데이터를 파일 시스템에 저장
Session(app)

# usage
global total_tokens_used
total_tokens_used = 0

@app.route('/', methods=['GET', 'POST'])
def home():
    # session.clear() #session 데이터 삭제

    if 'items' not in session:
        session['items'] = [] #세션에 items가 없다면 초기화
    # items = []  # This will store tuples of (text, image_url)

    if request.method == 'POST':
        user_input = request.form['user_input']

        # Generate an image from the initial user input
        initial_image = generate_image(user_input)
        session['items'].append((user_input, initial_image))

        # Generate additional text based on user input
        additional_text = generate_text(user_input)
        # session['items'].append((additional_text, None))  # Add text without an image

        # Generate another image from the additional text
        followup_image = generate_image(additional_text)
        session['items'].append((additional_text, followup_image))
        session.modified  = True # 세션 수정 표시

    return render_template_string(PAGE_TEMPLATE, items=session['items'])

def generate_text(prompt):
    try:
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",  # GPT-3.5-turbo 모델 사용
        #     prompt=prompt,  # 사용자로부터 받은 프롬프트
        #     max_tokens=50,  # 생성할 최대 토큰 수
        #     temperature=0.7,  # 창의성을 결정하는 요소, 0~1 사이의 값
        #     top_p=1.0,  # 누적 확률 분포에서 고려할 확률의 양
        #     frequency_penalty=0.0,  # 자주 나오는 단어에 대한 패널티
        #     presence_penalty=0.0  # 이미 나온 단어에 대한 패널티
        # )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # prompt = prompt,
            # 전달 메세지
            messages=[
                {"role": "system", "content": "Comportati come se fossi un SEO copywriter professionista."},
                {"role": "user", "content": f"{prompt}\n prompt 문장과 이어지는 다음 문장을 만들어줘"}
            ],
            max_tokens=50,
            temperature=0.8,
            top_p=1.0,
            frequency_penalty=2, #자주 나오는 단어에 대한 패널티, 반복되는 내용을 줄이는 데 도움이 됩니다.
            presence_penalty=0.5, # 이미 나온 단어에 대한 패널티, 새로운 내용을 도입하는 데 도움이 됩니다.
            n=1,
        )
        # Aggiungi il numero di token utilizzati per questa risposta al totale
        # global total_tokens_used = total_tokens_used + response['usage']['total_tokens']

        # 생성된 텍스트 가져오기
        # return response.choices[0].text.strip()
        full_text = response.choices[0].message.content
        tokens_used = response['usage']['total_tokens']
        print(tokens_used)

        # 첫 문장 추출
        first_sentence_end = min(
            full_text.find(end) for end in ['.', '?', '!'] if full_text.find(end) != -1
        )
        first_sentence = full_text[:first_sentence_end + 1] if first_sentence_end != -1 else full_text

        return first_sentence
    except Exception as e:
        print(f"Error generating text: {e}")
        return "Error generating text."

def generate_image(prompt):
    try:
        # DALL·E 3 모델을 사용하여 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{prompt}\n이솝우화 스타일 사용",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # 생성된 이미지의 URL을 반환합니다. 실제 URL 경로는 API 응답에 따라 다를 수 있습니다.
        # 아래는 응답 구조의 예시이며, 실제 응답 구조는 OpenAI 문서를 참조하세요.
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        # 이미지 생성에 실패한 경우, 대체 이미지 URL이나 에러 메시지를 반환할 수 있습니다.
        return "https://example.com/image_not_found.png"

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Story and Image Creator</title>
</head>
<body>
    <h1>Interactive Story and Image Creator</h1>
    <form method="post">
        <textarea name="user_input" rows="4" cols="50" placeholder="Enter your text here..."></textarea><br>
        <input type="submit" value="Generate">
    </form>
    {% for text, image_url in items %}
        <p>{{ text }}</p>
        {% if image_url %}
            <img src="{{ image_url }}" alt="Generated Image" style="max-width: 300px;"><br>
        {% endif %}
    {% endfor %}
</body>
</html>
"""

def record_usage(tokens_used):
    with open("usage_log.txt", "a") as file:
        file.write(f"{tokens_used}\n")

@app.route('/usage')
def get_total_usage():
    try:
        with open("usage_log.txt", "r") as file:
            total_usage = sum(int(line.strip()) for line in file if line.strip().isdigit())
        # 정수를 문자열로 변환하여 반환
        return str(total_usage)
    except FileNotFoundError:
        # 파일이 없는 경우 문자열 "0"을 반환
        return "0"

@app.route('/logout')
def logout():
    session.clear()  # 세션 데이터 전체 삭제
    return 'Logged out successfully!'

if __name__ == '__main__':
    app.run(debug=True)
