from cv2 import cv2
from cvzone.HandTrackingModule import HandDetector
cap=cv2.VideoCapture(0)
cap.set(3,1260)
cap.set(4,720)

detector=HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    img1 = cv2.imread("Resources/fish.jpg")
    img1 = cv2.resize(img1,[250,250])
    img[10:260,10:260]=img1

    if len(hands):
        print("Zoom Gesture")

    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
