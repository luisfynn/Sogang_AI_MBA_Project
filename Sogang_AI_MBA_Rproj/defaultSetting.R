#rtools 설치 확인
Sys.which("make")

#lib path 확인 및 추가
.libPaths()
my_paths <- .libPaths()
my_paths <- c(my_paths, "C:/Users/luisf/OneDrive/바탕 화면/WorkSpace/Sogang_AI_MBA_Proj/Sogang_AI_MBA_Rproj/Library")
.libPaths(my_paths)

#lib path 순서 변경
my_paths <- .libPaths()
my_paths <- c(my_paths[3],my_paths[1],my_paths[2])
.libPaths(my_paths)
.libPaths()

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




