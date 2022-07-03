import cv2
import time
import mouse
import HandTrackingModule as htm
import pyautogui
import numpy as np

def rightClick():
    mouse.click("right")
def leftClick():
    mouse.click("left")
smooth = 3
pLocX, pLocY = 0, 0
cLocX, cLocY = 0, 0
pTime = 0
cTime = 0
wCam, hCam = 640, 480
frameR = 150
wScr, hScr = pyautogui.size()
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.HandDetector()
clicked=False
while True:
    _, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    
    if len(lmList)>0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        
    cv2.rectangle(img, (frameR, frameR), (wCam-frameR, hCam-frameR), (255,0,255), 2)
    
    fingers = detector.fingersUp()
    if fingers[1]==1 and sum(fingers)==1:
        x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
        y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
        cLocX, cLocY = pLocX + (x3 - pLocX)/smooth, pLocY + (y3 - pLocY)/smooth 
        mouse.move(cLocX,cLocY)
        pLocX, pLocY = cLocX, cLocY
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        clicked=False
    if fingers[1]==1 and fingers[2]==1 and sum(fingers)==2:
        dist = detector.findDistance(8,12)
        clicked = False
        if dist<=40:
            leftClick()
            clicked=True
    if fingers[1]==1 and fingers[4]==1 and sum(fingers)==2:
        rightClick()
        clicked=True
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"{int(fps)}", (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    cv2.imshow("Frame",img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()