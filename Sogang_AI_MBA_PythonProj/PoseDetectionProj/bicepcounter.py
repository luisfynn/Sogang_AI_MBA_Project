#YOLOv7 Bicep Curl Counter Tutorial
#By Augmented Startups
#Visit www.augmentedstartups.com
import cv2
import time
import torch
import argparse
import numpy as np
from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.plots import output_to_keypoint, plot_skeleton_kpts
from utils.general import non_max_suppression_kpt, strip_optimizer
from torchvision import transforms
from trainer import findAngle
from trainer import findHeight
from PIL import ImageFont, ImageDraw, Image


@torch.no_grad()
def run(poseweights='yolov7-w6-pose.pt', source='pose.mp4', device='cpu', curltracker=False, drawskeleton=True, pushuptracker=False):

    path = source
    ext = path.split('/')[-1].split('.')[-1].strip().lower()
    if ext in ["mp4", "webm", "avi"] or ext not in ["mp4", "webm", "avi"] and ext.isnumeric():
        input_path = int(path) if path.isnumeric() else path
        device = select_device(opt.device)
        half = device.type != 'cpu'
        model = attempt_load(poseweights, map_location=device)
        _ = model.eval()

        cap = cv2.VideoCapture(input_path)
        webcam = False

        if (cap.isOpened() == False):
            print('Error while trying to read video. Please check path again')

        fw, fh = int(cap.get(3)), int(cap.get(4))
        if ext.isnumeric():
            print(f"webcam run")
            webcam = True
            fw, fh = 1280, 768
        vid_write_image = letterbox(
            cap.read()[1], (fw), stride=64, auto=True)[0]
        resize_height, resize_width = vid_write_image.shape[:2]
        out_video_name = "output" if path.isnumeric(
        ) else f"{input_path.split('/')[-1].split('.')[0]}"
        out = cv2.VideoWriter(f"{out_video_name}_kpt.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (resize_width, resize_height))
        if webcam:
            out = cv2.VideoWriter(f"{out_video_name}_kpt.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (fw, fh))

        frame_count, total_fps = 0, 0
        bcount = 0
        direction = 0

        # Load custom font
        fontpath = "sfpro.ttf"
        font = ImageFont.truetype(fontpath, 32)
        font1 = ImageFont.truetype(fontpath, 170)

        while cap.isOpened:

            print(f"Frame {frame_count} Processing")
            ret, frame = cap.read()
            if ret:
                orig_image = frame

                # preprocess image
                image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
                if webcam:
                    image = cv2.resize(
                        image, (fw, fh), interpolation=cv2.INTER_LINEAR)
                image = letterbox(image, (fw),
                                  stride=64, auto=True)[0]
                image_ = image.copy()
                image = transforms.ToTensor()(image)
                image = torch.tensor(np.array([image.numpy()]))

                image = image.to(device)
                image = image.float()
                start_time = time.time()

                with torch.no_grad():
                    output, _ = model(image)

                output = non_max_suppression_kpt(
                    output, 0.5, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'], kpt_label=True)
                output = output_to_keypoint(output)
                img = image[0].permute(1, 2, 0) * 255
                img = img.cpu().numpy().astype(np.uint8)

                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

                if curltracker:
                    for idx in range(output.shape[0]):
                        kpts = output[idx, 7:].T #output(keypoint)의 7번째 값부터 끝까지 kpts에 저장
                        #print(f"kpts:{kpts}")
                        # Right arm =(5,7,9), left arm = (6,8,10)
                        # set draw=True to draw the arm keypoints.
                        angle = findAngle(img, kpts, 5, 7, 9, draw=False) #from trainer import findAngle 함수 참조
                        #print(f"angle: {angle}") #펼친 상태에서 360도, 굽히면 0
                        percentage = np.interp(angle, (10, 150), (100, 0)) #팔을 굽히면(10도) 100%, 팔을 펴면(150도) 0% (검증 필요함)
                        bar = np.interp(angle, (20, 150), (200, fh-100))

                        color = (254, 118, 136)
                        # check for the bicep curls
                        if percentage == 100:
                            if direction == 0:
                                bcount += 0.5
                                direction = 1
                        if percentage == 0:
                            if direction == 1:
                                bcount += 0.5
                                direction = 0

                        # draw Bar and counter
                        cv2.line(img, (100, 200), (100, fh-100),
                                 (255, 255, 255), 30)
                        cv2.line(img, (100, int(bar)),
                                 (100, fh-100), color, 30)

                        #시작점 (x,y)좌표와 종료점 (x,y) 좌표를 동일하게 수정
                        # % 표시가 되는 직선
                        if (int(percentage) < 10):
                            #cv2.line(img, (155, int(bar)), (190, int(bar)), (254, 118, 136), 40)
                            cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                        elif (int(percentage) >= 10 and (int(percentage) < 100)):
                            #cv2.line(img, (155, int(bar)), (200, int(bar)), (254, 118, 136), 40)
                            cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)
                        else:
                            cv2.line(img, (155, int(bar)), (210, int(bar)), (254, 118, 136), 40)

                        im = Image.fromarray(img)
                        draw = ImageDraw.Draw(im)
                        draw.rounded_rectangle((fw-280, (fh//2)-100, fw-80, (fh//2)+100), fill=color,
                                               radius=40)

                        draw.text(
                            (145, int(bar)-17), f"{int(percentage)}%", font=font, fill=(255, 255, 255))
                        draw.text(
                            (fw-228, (fh//2)-101), f"{int(bcount)}", font=font1, fill=(255, 255, 255))
                        img = np.array(im)

                if pushuptracker:
                    #print(f"run pushup tracker")
                    for idx in range(output.shape[0]):
                        kpts = output[idx, 7:].T #output(keypoint)의 7번째 값부터 끝까지 kpts에 저장
                        #print(f"kpts:{kpts}")
                        # Right arm =(5,7,9), left arm = (6,8,10)
                        # set draw=True to draw the arm keypoints.
                        height = findHeight(img, kpts, 5, 9)
                        percentage = np.interp(height, (25, 40), (100, 0))
                        bar = np.interp(height, (25, 40), (200, fh-100))

                        print(f"height: {height} percentage: {percentage} bar: {bar}")

                        color = (0, 118, 136)
                        # check for the pushup
                        if percentage >= 90:
                            if direction == 0:
                                bcount += 0.5
                                direction = 1
                        if percentage <= 10:
                            if direction == 1:
                                bcount += 0.5
                                direction = 0

                        # draw Bar and counter
                        cv2.line(img, (100, 200), (100, fh-100),
                                 (255, 255, 255), 30)
                        cv2.line(img, (100, int(bar)),
                                 (100, fh-100), color, 30)

                        if (int(percentage) < 10):
                            cv2.line(img, (155, int(bar)),
                                     (190, int(bar)), (0, 118, 136), 40)
                        elif (int(percentage) >= 10 and (int(percentage) < 100)):
                            cv2.line(img, (155, int(bar)),
                                     (200, int(bar)), (0, 118, 136), 40)
                        else:
                            cv2.line(img, (155, int(bar)),
                                     (210, int(bar)), (0, 118, 136), 40)

                        im = Image.fromarray(img)
                        draw = ImageDraw.Draw(im)
                        draw.rounded_rectangle((fw-280, (fh//2)-100, fw-80, (fh//2)+100), fill=color,
                                               radius=40)

                        draw.text(
                            (145, int(bar)-17), f"{int(percentage)}%", font=font, fill=(255, 255, 255))
                        draw.text(
                            (fw-228, (fh//2)-101), f"{int(bcount)}", font=font1, fill=(255, 255, 255))
                        img = np.array(im)

                if drawskeleton:
                    for idx in range(output.shape[0]):
                        plot_skeleton_kpts(img, output[idx, 7:].T, 3)

                if webcam:
                    cv2.imshow("Detection", img)
                    key = cv2.waitKey(1)
                    if key == ord('c'):
                        break
                else:
                    img_ = img.copy()
                    img_ = cv2.resize(img_, (960, 540), interpolation=cv2.INTER_LINEAR)
                    #img_ = cv2.resize(img_, (480, 360), interpolation=cv2.INTER_LINEAR)
                    cv2.imshow("Detection", img_)
                    cv2.waitKey(1)

                end_time = time.time()
                fps = 1 / (end_time - start_time)
                total_fps += fps
                frame_count += 1
                #out.write(img)
            else:
                break

        cap.release()
        avg_fps = total_fps / frame_count
        print(f"Average FPS: {avg_fps:.3f}")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str,
                        default='yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--source', type=str,
                        help='path to video or 0 for webcam')
    parser.add_argument('--device', type=str, default='cpu',
                        help='cpu/0,1,2,3(gpu)')
    parser.add_argument('--curltracker', type=bool, default=False,
                        help='set as true to check count bicep curls')
    parser.add_argument('--pushuptracker', type=bool, default=False,
                        help='set as true to check count bicep curls')
    parser.add_argument('--drawskeleton', type=bool,
                        help='draw all keypoints')

    opt = parser.parse_args()
    return opt


def main(opt):
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device, opt.poseweights)
    main(opt)
