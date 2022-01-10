from cv2 import cv2
import numpy as np
import time
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640,480
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol=(255,0,0)

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector(detectionConf=0.7,maxHands=1)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumeRange = volume.GetVolumeRange()
minvol = volumeRange[0]
maxvol = volumeRange[1]

while True:
    success, img= cap.read()
    # Find Hand
    img = detector.findhands(img)
    lmlist = detector.handPosition(img,draw=True)
    if(len(lmlist) != 0):
        # print(lmlist[4], lmlist[8])
        area = (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        # print(area)

        if 250 < area < 1000:
            # Find Distance between index and thumb
            length, img, lineInfo = detector.findDistange(4,8,img)
            # Hand rangee = 50,300
            #check range = 55,65
            # volRange = -65, 0

            # Convert value
            vol= np.interp(length,[50,300],[minvol,maxvol])
            volBar=np.interp(length,[50,300],[400,150])
            volPer=np.interp(length,[50,300],[0,100])
            cv2.putText(img,f'{int(volPer)}%', (40,450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
            # print(vol)

            # Reduce Resolution to make is smoother
            smoothness = 10
            volPer = smoothness*round(volPer/smoothness)

            # Check fingers up
            fingers = detector.fingersup()

            if not fingers[4]:
                # volume.SetMasterVolumeLevel(vol, None)
                volume.SetMasterVolumeLevelScalar(volPer/100,None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (0, 0, 255), cv2.FILLED)
                colorVol=(0,255,255)

    cTime=time.time()
    fps = 1/(cTime-pTime)
    pTime= cTime

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,240,0),cv2.FILLED)
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, f'Vol Set: {cVol}',(400,30),cv2.FONT_HERSHEY_PLAIN,2,colorVol,3)
    cv2.putText(img,f'FPS: {int(fps)}',(10,70),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)


    cv2.imshow("Output",img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break