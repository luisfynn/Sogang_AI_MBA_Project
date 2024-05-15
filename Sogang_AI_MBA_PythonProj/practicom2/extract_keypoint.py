import torch
from utils.general import non_max_suppression_kpt, output_to_keypoint

# 모델 로드
model = torch.load('trained_yolov8x-pose-p6.pt')

# 모델 설정 파일에서 nc와 nkpt 값 가져오기
nc = model['model'].yaml['nc']
nkpt = model['model'].yaml['nkpt']

# 입력 이미지 처리 (예: 'img'는 사전 처리된 이미지 텐서)
# 예시로서 더미 데이터를 사용합니다.
# 실제 이미지 데이터를 사용하는 경우 전처리 과정을 거친 텐서를 사용하세요.
img = torch.zeros((1, 3, 640, 640))  # 예시 이미지 텐서

# 모델 추론
with torch.no_grad():
    output = model(img)[0]

# 비최대 억제 수행
output = non_max_suppression_kpt(output, 0.5, 0.65, nc=nc, nkpt=nkpt, kpt_label=True)

# 키포인트 추출
keypoints = output_to_keypoint(output)

print(keypoints)
