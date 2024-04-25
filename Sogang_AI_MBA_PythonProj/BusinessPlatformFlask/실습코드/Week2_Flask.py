#requests 라이브러리가 하기 항목을 가지고 있음
##URL : L=location. 문서의 위치를 저장
##URI : I=Identifier(식별자) URI 가 URL을 포함하고 있는 개념이다.
##post : ID, password 등 보안이 필요한 정보를 전달할 때 사용
##요즘은 서버의 보안절차로 인해 requests 를 사용하지 않는다.
##get, host 방식의 차이: get은 보안이 안됨. host는 보안

#https: html을 전송할 때 보안을 추가(s: security)
#requests를 캡슐화하여 하나의 패키지로 만든 것이 selenium

#HyperText 문서: 링크가 존재하는 문서
#HTML -> XML -> JSON 로 이동
##HTML: 보여주기가 강조되어, 정보가 등한시되었다.
##XML: 정보만 가지고 있는 문서를 만들기 위한 언어
##JSON : dictionary 구조

#브라우저 역할: 요청하여 받은 html을 parsing하는 역할
#tag: box model. 두가지 중 하나(Box, Item)
##Box: 화면을 꾸밀 때 사용, 화면에 보이지 않음
###p(구문), div(구역), form tag를 주로 사용
##Item: 화면에 보여줄 정보에 사용
###a(링크 생성), img, table, input tag를 주로 사용

#html5: 기본형식이지만, 규격을 반드시 지키진 않음

#모든 tag에는 class와 id가 들어감
##class: 모든 tag에서 중복이 가능하며, 같은 class인 경우 같은 형식(폰트, 색상)을 적용
##id: 모든 문서에서 유일한 이름을 가지게 함

#block & inline
#html은 기본적으로 block모드로 동작(한 줄에 한 tag)
#inline : 한 줄에 여러 개의 글을 올릴 수 있도록 한다.

#css : style sheet
#meta tag: 문서의 중요한 정보를 갖고 있다.
#검색시 meta tag를 검색하여 정보를 보여주는 것이다.

#ol :ordered list 순서있는 리스트
#ul :not ordered list
#li :

#id 의 css는 #이다.
#class의 css 는 . 이다.

#HTML과 CSS는 상호작용 하지않지만 Javascript는 HTML과 상호작용함
#Javascript
## 웹 페이지 내부에서 발생하는 일(Event)들을 감지
## 사용자가 입력하는 데이터에 대해 서버로 전송 전, 유효성 검사(잘못된 요청을 파악할 수 있음) 가능

#pycharm IDE
#venv:
#conda: python interpreter와 util을 갖고 있다.
#pycharm 프로젝트시 conda를 프로젝트 내부로 가져와서, 필요한 라이브러리만 로드하도록 만듬
##그렇지 않을 경우 conda에 여러 프로젝트의 lib가 설치되어 무거워진다.
from flask import Flask

app = Flask(__name__)

#@:decorator
#'/':root
#즉 root 요청이 들어오면 hello()를 실행하여 client에 전송함
@app.route('/')
def hello():
    return "hello world"

if __name__ == "__main__":
    app.run()