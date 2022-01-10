from cv2 import cv2
import HandTrackingModule as htm
import numpy as np
import  time
import autopy

cap = cv2.VideoCapture(0)
wcam, hcam = 640,480
frameR = 100  #Frame Reduction
smooth = 7

cap.set(3,wcam)
cap.set(4,hcam)

detector = htm.handDetector(maxHands=1)
pTime = 0
wSrc, hSrc = autopy.screen.size()
plocX, plocY = 0,0
clocX, clocY = 0,0
# print(wSrc,hSrc)

while True:
    success, img = cap.read()
    # TODO:Find hand landmarks
    img = detector.findhands(img)
    lmlist = detector.handPosition(img)

    # TODO: Get the tip of the index and middle finger
    if len(lmlist) != 0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]
        # print(x1,y1,x2,y2)

        # TODO:Check which fingers are up
        fingers = detector.fingersup()
        # print(fingers)
        cv2.rectangle(img, (frameR, frameR), (wcam - frameR, hcam - frameR), (255, 255, 255), 2)

        # TODO: Only Inder Finger: Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:

            #TODO: Convert coordinates
            x3 = np.interp(x1,(frameR,wcam-frameR),(0,wSrc))
            y3 = np.interp(y1,(frameR,hcam-frameR),(0,hSrc))

            # TODO: Smoothen Values
            clocX = plocX + (x3-plocX)/smooth
            clocY = plocY + (y3-plocY)/smooth

            # TODO: Move Mouse
            autopy.mouse.move(wSrc-clocX,clocY)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX, plocY = clocX,clocY

        # TODO: Both Index and Middle finger are up: Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # TODO: Find distance between fingers
            length,img,lineInfo = detector.findDistance(8,12,img)
            print(length)

            # TODO: click Mouse when distance is sort
            if length < 40:
                cv2.circle(img,(lineInfo[4],lineInfo[5]),13,(0,255,0),cv2.FILLED)
            autopy.mouse.click()

    # TODO: Frame Rate
    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img,f"fps:{fps}",(460,40),cv2.FONT_HERSHEY_SIMPLEX,1,(119,220,340),2)

    cv2.imshow("Mouse",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break