#YOLOv7 Find Angle Function
#By Augmented Startups
#Visit www.augmentedstartups.com
import math
import cv2 #pip install cv or pip install opencv-python

# =3.0=Takes three points and returns the angle between them========
def findAngle(image, kpts, p1,p2,p3, draw= True):
    coord = []
    no_kpt = len(kpts)//3
    for i in range(no_kpt):
        cx,cy = kpts[3*i], kpts[3*i +1]
        conf = kpts[3*i +2]
        coord.append([i, cx,cy, conf])

    points = (p1,p2,p3)

    # =3.1=Get landmarks========
    x1,y1 = coord[p1][1:3]
    x2,y2 = coord[p2][1:3]
    x3,y3 = coord[p3][1:3]

    # =3.2=Calculate the Angle========
    angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2, x1-x2))

    if angle < 0:
        angle += 360

    # =3.3=Draw Coordinates========
    if draw:
        cv2.line(image, (int(x1),int(y1)),(int(x2), int(y2)),(255,255,255),3 )
        cv2.line(image, (int(x3),int(y3)),(int(x2), int(y2)),(255,255,255),3 )

        cv2.circle(image, (int(x1),int(y1)),  10, (255,255,255),cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)
        cv2.circle(image, (int(x1), int(y1)), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(image, (int(x1), int(y1)), 20, (235, 235, 235), 5)

    return int(angle)
# ===========================================

def findHeight(image, kpts, p1,p2):
    coord = []
    no_kpt = len(kpts)//3
    for i in range(no_kpt):
        cx,cy = kpts[3*i], kpts[3*i +1]
        conf = kpts[3*i +2]
        coord.append([i, cx,cy, conf])

    points = (p1,p2)

    # =3.1=Get landmarks========
    x1,y1 = coord[p1][1:3]
    x2,y2 = coord[p2][1:3]

    z1=[x1,y1]
    z2=[x2,y2]

    # =3.2=Calculate the Distance========
    dist = math.dist(z1, z2)
    dist = dist/10 #cm 로 변환
    return int(dist)