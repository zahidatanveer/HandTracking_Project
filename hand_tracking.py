from cv2 import cv2
import mediapipe as mp
import time

cap= cv2.VideoCapture(0)
mpHands= mp.solutions.hands
hands=mpHands.Hands()
mpdraw=mp.solutions.drawing_utils

cTime=0
pTime=0

while True:
    success, img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(imgRGB)
    # print(result.multi_hand_landmarks)
    if result.multi_hand_landmarks:
        for handlmr in result.multi_hand_landmarks:
            for id,lm in enumerate(handlmr.landmark):
                h, w, c = img.shape
                cx,cy= int(lm.x*w), int(lm.y*h)
                print(id,cx,cy)
                cv2.circle(img,(cx,cy),10,(255,0,0),3,cv2.FILLED)


            mpdraw.draw_landmarks(img,handlmr,mpHands.HAND_CONNECTIONS)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),3)

    cv2.imshow("Orignal",img)
    cv2.waitKey(1)