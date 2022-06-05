#https://github.com/cvzone/cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector


class HandTracker:
    __detector = None
    __video = None
    __hands = None
    __handimg = None
    __rawimg = None
    __fingerCount = 0

    def __init__(self, maxHands=2, detectionCon=0.8, video=0):
        self.__detector = HandDetector(maxHands, detectionCon)
        self.__video = cv2.VideoCapture(video)

    def getHands(self):
        _, self.__rawimg = self.__video.read()
        self.__hands, self.__handimg = self.__detector.findHands(self.__rawimg, draw=True)

    def processImage(self):
        self.__fingerCount = 0
        for hand in self.__hands:
            if hand:
                lmlist = hand
                if lmlist:
                    fingerup = self.__detector.fingersUp(lmlist)
                    self.__fingerCount = self.__fingerCount + sum(fingerup)
        return self.__fingerCount
    
    def showHands(self):
        cv2.imshow("Video", self.__rawimg)
    
    def camReset(self):
        self.__video.release()
        cv2.destroyAllWindows()