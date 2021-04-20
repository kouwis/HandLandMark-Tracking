import cv2 as cv
import mediapipe as mp


class HandTracking():
    def __init__(self, class_mode = False, maxHands = 2, detection_conf = 0.5, tracking_conf = 0.5):

        self.mpHand = mp.solutions.hands
        self.Hands = self.mpHand.Hands(class_mode, maxHands, detection_conf, tracking_conf)
        self.mpDraw = mp.solutions.drawing_utils

    def FindHand(self, img):

        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        self.res = self.Hands.process(imgRGB)

        if self.res.multi_hand_landmarks:
            for hand in self.res.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, hand, self.mpHand.HAND_CONNECTIONS)

        return img

    def HandPosition(self, img):

        myList = []
        if self.res.multi_hand_landmarks:
            myHand = self.res.multi_hand_landmarks[0]

            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                myList.append([id, cx, cy])

        return myList
def main():

    cap = cv.VideoCapture(0)

    width, height = 420, 360

    cap.set(3, width)
    cap.set(4, height)

    detector = HandTracking()

    while 1:
        ret, img = cap.read()

        img = detector.FindHand(img)
        myList = detector.HandPosition(img)

        if len(myList) != 0:
            print(myList)

        cv.imshow("HandLandMark", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()