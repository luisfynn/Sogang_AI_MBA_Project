# 파이참 찾아서 바꾸기 ctrl+r
# 패키지 설치
# pip install torch torchvision pandas scikit-learn openpyxl

# # labelme 설치 및 이미지 라벨링//anaconda prompt 사전 설치 필요//파이참 종료후 할 것
# set PYTHONIOENCODING=utf-8
# conda create --name=labelme python=3
# pip install labelme
# conda activate labelme
# pip install labelme
# 이래도 안되면 시스템 환경변수 추가 환경변수명 PYTHONUTF8 값 1

# # anaconda prompt 닫은 후, 다시 열었을 때
# conda activate labelme
# labelme 실행: labelme C:/Users/medit/Desktop/WorkSpace/pythonProject/Practicom/korean_food_sample --autosave
# # 이미지 라벨 작업

########################################################################################################################
# yolo 모델을 이용한 학습
# 패키지 설치
# pip install torch torchvision numpy matplotlib opencv-python