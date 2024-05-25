import torch

def face_detector(img):
    # 모델 로드
    # filePath = r"C:\Users\luisf\OneDrive\desktop\WorkSpace\Sogang_AI_MBA_Project\Sogang_AI_MBA_PythonProj\pythonProjectP\face_best.pt"
    filePath = r"face_best.pt"
    model = torch.hub.load('ultralytics/yolov5', 'custom', path= filePath)

    results = model(img)
    print(f"results: {results}")
    return results