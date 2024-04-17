#All Flask applications must create an application instance
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world(): #view functions.
    return 'Hello, World!'

# The previous example registers the function index() as the handler for the application’s root URL.
# @app.route('/')
# def index(): #view functions.
#     return '<h1>Hello World!!!!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


# Python에서 스크립트를 직접 실행할 때, 즉 커맨드 라인에서 python xxx.py와 같이 해당 스크립트 파일을 실행시킬 때,
# 해당 스크립트 파일 내에서의 __name__ 변수의 값은 __main__이 됩니다. 이는 Python이 실행 중인 파일을 메인 프로그램으로 인식하기 때문입니다.

# 이 메커니즘은 Python이 스크립트를 직접 실행하는 경우와 모듈로 임포트해서 사용하는 경우를 구분하기 위해 사용됩니다.
# 만약 xxx.py가 다른 Python 파일에서 모듈로 임포트되어 사용되는 경우 (import xxx),
# xxx.py 내의 __name__ 변수는 __main__이 아닌 xxx로 설정됩니다.
# main.py에서 app.py를 임포트하여 확인할 수 있다.
print(f"The value of __name__ is: {__name__}") #결과 The value of __name__ is: __main__

# server startup
# Once the server starts up, it goes into a loop that waits for requests and services them.
# This loop continues until the application is stopped, for example by hitting Ctrl-C.
if __name__ == '__main__':
    app.run(debug=True)
