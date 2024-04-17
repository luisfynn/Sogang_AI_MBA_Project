#pip install roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="KlUSsAio79PTtj3A26Uh")
project = rf.workspace("test-a2btg").project("usb-labeler")
version = project.version(1)
dataset = version.download("yolov9")

#사전학습된 모델을 다운로드받아 학습하진 않음
#학습할 경우 yoloV9을 다운로드받아서 다음과 같은 방법으로 학습 필요
# !python usbModelTrain.py --batch 32 -conf configs/yolov6s.py --epochs 30 ---img-size 416 --data USB-LABELER-1/data.yaml --device 0
# yolov6 대신 configs 폴더 안의 다른 모델 이용 가능
# https://github.com/WongKinYiu/yolov9.git

# inference converted yolov9 models
# 터미널에서 실행
# python yolov9-main/detect.py --source 'USB-LABELER-1/test/images/L_5_jpg.rf.77a4b18ee5286ee072c5159e02639b20.jpg' --img 640 --device 0 --weights 'yolov9-main/yolov9-e-converted.pt' --name yolov9_c_c_640_detect
# Results saved to yolov9-main\runs\detect\yolov9_c_c_640_detect2


# inference yolov9 models
# python detect_dual.py --source './data/images/horses.jpg' --img 640 --device 0 --weights './yolov9-c.pt' --name yolov9_c_640_detect

# inference gelan models
# python detect.py --source './data/images/horses.jpg' --img 640 --device 0 --weights './gelan-c.pt' --name gelan_c_c_640_detect