#rtools 설치 확인
Sys.which("make")

#lib path 확인 및 추가
# 키보드로 "고급 시스템 설정 보기"라고 입력
# "환경 변수" 클릭
# 사용자 변수 쪽에 "새로 만들기" 클릭
#   이름: R_LIBS_USER
#   값: 사용자의 user 폴더 안에 R_LIBS_USER라는 이름의 폴더를 만들고 이 경로를 입력함, 저 같은 경우는 C:\Users\masan\R_LIBS_USER
#   사용자 변수 쪽에 "새로 만들기" 클릭
# 
#   이름: R_LIBS_SITE
#   값: 사용자의 user 폴더 안에 R_LIBS_SITE라는 이름의 폴더를 만들고 이 경로를 입력함
#   이제 사용자가 설치한 library는 모두 R_LIBS_USER 안에 저장됩니다. R을 업데이트하면 새로 라이브러리를 매번 설치할 필요가 없어집니다

#변경된 lib path에 패키지 설치
install.packages("tidyverse")

#다음은 콘솔창에서 실행
#remotes::install_github("anthonynorth/rscodeio")

#아래 코드는 실행해보고 에러 나면 
#직접 테마 설정
#Options -> Appearance -> Editor Theme and selecting "rscodeio".
#library(rscodeio)
#rscodeio::install_theme() 

#라스트
#다음의 사항들을 체크합시다.
#• Tools → Global Options → Code → Display
#– Highlight selected line
#– Highlight R function calls
#• Tools → Global Options → Console
#Show syntax highlighting in console input 체크




