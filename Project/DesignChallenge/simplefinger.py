#https://github.com/cvzone/cvzone

import cv2
from cvzone.HandTrackingModule import HandDetector
 
detector = HandDetector(maxHands=2, detectionCon=0.8)
video = cv2.VideoCapture(0)
 
while True:
    _, img = video.read()
    hands, handimg = detector.findHands(img, draw=True)
    fing = 0

    for hand in hands:
        if hand:
            lmlist = hand
            if lmlist:
                fingerup = detector.fingersUp(lmlist)
                fing = fing + sum(fingerup)

    cv2.imshow("Video", img)
    print(fing)
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
         
video.release()
cv2.destroyAllWindows()