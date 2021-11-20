from cv2 import cv2
import time
import os
import HandTrackingModule as htm

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

path="Resources"
imglist = os.listdir(path)
# print(imglist)
overlayList=[]

for imgpath in imglist:
    image = cv2.imread(f'{path}/{imgpath}')
    image= cv2.resize(image,[150,150])
    overlayList.append(image)
print(len(overlayList))
pTime=0

detector = htm.handDetector(detectionConf=0.75)
fngtips = [4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmlist = detector.handPosition(img,draw=False)

    if len(lmlist) != 0:
        fngList=[]

        if lmlist[4][1] > lmlist[3][1]:
            fngList.append(1)
        else:
            fngList.append(0)

        for id in range(1,5):
            if lmlist[fngtips[id]][2] < lmlist[fngtips[id]-2][2]:
                fngList.append(1)
            else:
                fngList.append(0)
        # print(fngList)
        totalFingure= fngList.count(1)
        print(totalFingure)

        img[0:150, 0:150] = overlayList[totalFingure-1]

    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime


    cv2.putText(img,f'fps: {int(fps)}',(10,205),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)

    cv2.imshow("Image",img)

    cv2.waitKey(1)