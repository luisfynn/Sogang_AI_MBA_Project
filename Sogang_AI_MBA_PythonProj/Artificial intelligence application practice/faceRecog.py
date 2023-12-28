import matplotlib.pyplot as plt ; import cv2

#캐스케이드 얼굴요소 DB) 파일 지정해서 검출기 생성하기 아래 파일을 먼저 Colab 에 위치 시킴
filename = "haarcascade_frontalface_alt.xml"
cascade_file = filename
cascade= cv2.CascadeClassifier(cascade_file)

#이미지를 읽어 들이기 (jpg 는 RGB 인데 cv2 로 읽으면 BGR 이 됨
#target_image = "/content/girl.jpg" # girl.jpg 파일을 Colab 으로 먼저 위치 시켜야 함
target_image = "girls.jpg"
img = cv2.imread(target_image)
img.shape # (1209, 1000, 3): ( height , x=width, BGR(3
img[100,100] # [ 56, 93, 119] <--(y=100, x=100 위치의 BRG 값 : pixel 값 (0~255 사이 ))
img[100,100,0] # 56: BGR 의 blue 의 pixel 값
plt.imshow(img)

img
