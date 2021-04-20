import cv2 as cv
import HLMTmodule as htl
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import numpy as np

cap = cv.VideoCapture(0)

width, height = 420, 360

cap.set(3, width)
cap.set(4, height)

detector = htl.HandTracking()

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while 1:
    ret, img = cap.read()
    img = detector.FindHand(img)


    myList = detector.HandPosition(img)
    if len(myList) != 0:
        x1 , y1 = myList[8][1], myList[8][2]
        x2, y2 = myList[4][1], myList[4][2]
        cx, cy = (x1 + x2)// 2, (y1+ y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        cv.circle(img, (x1,y1), 10, (255,255,0), cv.FILLED)
        cv.circle(img, (x2, y2), 10, (255, 255, 0), cv.FILLED)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)

        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv.circle(img, (cx,cy), 10, (0,0,0), cv.FILLED)
        else:
            cv.circle(img, (cx, cy), 10, (0, 255, 0), cv.FILLED)

        cv.line(img, (x1,y1), (x2, y2), (255,255,0), 2)
    cv.imshow("img", img)
    cv.waitKey(1)