from cv2 import cv2
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self,mode=False, maxHands=2, model_complexity=1, detectionConf=0.5, trackingConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity= model_complexity
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionConf, self.trackingConf)
        self.mpdraw = mp.solutions.drawing_utils


    def findhands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        if self.result.multi_hand_landmarks:
            for handlmr in self.result.multi_hand_landmarks:
                if draw:
                    self.mpdraw.draw_landmarks(img,handlmr,self.mpHands.HAND_CONNECTIONS)
        return img

    def handPosition(self, img, handno=0, draw=True):
        xList=[]
        yList=[]
        bbx=[]
        self.lmlist=[]
        if self.result.multi_hand_landmarks:
            myhand = self.result.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbx = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img,(bbx[0]-20,bbx[1]-20), (bbx[2]+20,bbx[3]+20),(0,255,0),2)

        return self.lmlist

    def fingersup(self):
        fngList = []
        fngtips = [4, 8, 12, 16, 20]

        # For thumb
        if len(self.lmlist) != 0:
            if self.lmlist[4][1] < self.lmlist[3][1]:
                fngList.append(1)
            else:
                fngList.append(0)

            # For fingers
            for id in range(1, 5):
                if self.lmlist[fngtips[id]][2] < self.lmlist[fngtips[id] - 2][2]:
                    fngList.append(1)
                else:
                    fngList.append(0)
            # print(fngList)
            # totalFingure = fngList.count(1)
            # print(totalFingure)
        return fngList

    def findDistance(self,p1,p2,img,draw=True):
        x1, y1 = self.lmlist[p1][1], self.lmlist[p1][2]
        x2, y2 = self.lmlist[p2][1], self.lmlist[p2][2]
        x3, y3 = self.lmlist[12][1], self.lmlist[12][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # checkLen = math.hypot(x3 - x2, y3 - y2)

        return length,img,[x1,y1,x2,y2,cx,cy]


def main():
    cTime = 0
    pTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.handPosition(img)
        fingers = detector.fingersup()

        # if len(lmlist) != 0:
        #     print(lmlist[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 3)

        cv2.imshow("Orignal", img)
        cv2.waitKey(1)


if __name__ =="__main__":
    main()