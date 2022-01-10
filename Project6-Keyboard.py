from cv2 import cv2
import HandTrackingModule as htm
from time import sleep
from pynput.keyboard import Controller


cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = htm.handDetector(detectionConf=0.8)

keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
textList =""
keyboard = Controller()


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (100, 0, 0), cv2.FILLED)
        cv2.putText(img, button.txt, (x + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    return img


class Button:
    def __init__(self, pos, txt, size=(85, 85)):
        self.pos = pos
        self.txt = txt
        self.size = size


buttonList = []
for i in range(len(keys)):
    for x, k in enumerate(keys[i]):
        buttonList.append(Button([100 * x + 60, 100 * i + 60], k))


while True:
    success, img = cap.read()
    img = detector.findhands(img)
    lmlist = detector.handPosition(img)
    # print(lmlist)
    img = drawAll(img, buttonList)

    if lmlist:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            if x < lmlist[8][1] < x+w and y < lmlist[8][2] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 100, 0), cv2.FILLED)
                cv2.putText(img, button.txt, (x + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
                l, _, _ = detector.findDistance(8, 12, img)
                # print(l)
                if l<30:
                    keyboard.press(button.txt)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.txt, (x + 20, y + 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
                    # print("Button clicked")
                    textList += button.txt
                    sleep(0.15)

    cv2.rectangle(img, (50,400), (900,500), (0, 50, 0), cv2.FILLED)
    cv2.putText(img, textList, (60,475), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)


    cv2.imshow("Virtual Keyboard",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


