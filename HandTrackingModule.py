import cv2
import mediapipe as mp
import time
import math
class HandDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.fingerTips = [4,8,12,16,20]
    
    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, 
                        self.mpHands.HAND_CONNECTIONS)
        return img
    def findPosition(self, img, handNo=0, draw=True, fitPointsToWindow=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            selHand = self.results.multi_hand_landmarks[handNo]
            h, w, c = img.shape
            for idx, lm in enumerate(selHand.landmark):
                if fitPointsToWindow:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                else:
                    cx, cy = lm.x, lm.y
                self.lmList.append((idx, cx, cy))
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)
        return self.lmList
    def fingersUp(self):
        fingers = []
        if len(self.lmList)<=0:
            return [0]*5
        if self.lmList[self.fingerTips[0]][1] > self.lmList[self.fingerTips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for i in range(1,5):
            if self.lmList[self.fingerTips[i]][2] < self.lmList[self.fingerTips[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    def findDistance(self, p1, p2):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        dist = math.hypot(x2-x1, y2-y1)
        return dist
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        _, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img,draw=False)
        if len(lmList) > 0:
            print(lmList[8])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"{int(fps)}", (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
        cv2.imshow("Frame",img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()