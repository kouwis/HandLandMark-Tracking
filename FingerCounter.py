import cv2 as cv
import HLMTmodule as htl
import os

fingers_dir = "fingers"
fingers_list = os.listdir(fingers_dir)
images = []

for finger in os.listdir(fingers_dir):
    img = cv.imread(f"{fingers_dir}/{finger}")
    img = cv.resize(img, (200,200))
    images.append(img)

cap = cv.VideoCapture(0)

width, height = 420, 360

cap.set(3, width)
cap.set(4, height)

detector = htl.HandTracking()


while 1:
    ret, img = cap.read()

    img = detector.FindHand(img)
    myList = detector.HandPosition(img)

    if len(myList) != 0:
        fingerList = []
        for tip in range(4, 21, 4):
            if tip != 4:
                if myList[tip][2] < myList[tip - 2][2]:
                    fingerList.append(1)
                else:
                    fingerList.append(0)
            else:
                if myList[tip][1] > myList[tip - 1][1]:
                    fingerList.append(1)
                else:
                    fingerList.append(0)

        fingerTotal = fingerList.count(1)

        h, w, c = images[fingerTotal].shape

        img[0:h, 0:w] = images[fingerTotal]

        cv.putText(img, str(fingerTotal), (45, 375), cv.FONT_HERSHEY_PLAIN,
                    5, (255, 0, 0), 20)
    cv.imshow("HandLandMark", img)
    cv.waitKey(1)