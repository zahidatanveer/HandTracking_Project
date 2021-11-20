from cv2 import cv2
import numpy as np
import time
import HandTrackingModule as htm
import os

folderPath = "Header"
imglist = os.listdir(folderPath)

headerList = []

for imgpath in imglist:
    image = cv2.imread(f"{folderPath}/{imgpath}")
    headerList.append(image)

print(len(headerList))
header = headerList[0]

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

drawcolor = (255,0,255)
brushThickness = 15
xp, yp = 0,0

imgCanvas = np.zeros((720,1280,3),np.uint8)

detector = htm.handDetector(detectionConf=0.85)

while True:
    isTrue, img = cap.read()
    img=cv2.flip(img,1)

    # Find hand landmarks
    img = detector.findhands(img)
    lmlist = detector.handPosition(img,draw=False)

    if len(lmlist) != 0:
        # print(lmlist)

    # Tip of the index and middle finger

        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        # Check which fingers are up
        fingers = detector.fingersup()
        # print(fingers)

        if fingers[1] and fingers[2]:
            xp, yp = 0,0
            print("Selection Mode")
        #  Checking for the click
            if y1<125:
                if 250<x1<450:
                    header = headerList[0]
                    drawcolor = (255,0,255)
                elif 550<x1<750:
                    header = headerList[1]
                    drawcolor = (255,0,0)
                elif 800<x1<900:
                    header = headerList[2]
                    drawcolor = (0,255,0)
                elif 1000<x1<1200:
                    header = headerList[3]
                    drawcolor = (0,0,0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 15), drawcolor, cv2.FILLED)

        if fingers[1] and fingers[2] == False:
            cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
            print("Drawing mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawcolor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, 75)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, 75)

            cv2.line(img,(xp,yp),(x1,y1),drawcolor,brushThickness)
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, brushThickness)

            xp, yp = x1,y1

    grayimg = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(grayimg, 50,255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    img[0:125,0:1280] = header
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Paint",img)
    # cv2.imshow("Canvas", imgCanvas)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

