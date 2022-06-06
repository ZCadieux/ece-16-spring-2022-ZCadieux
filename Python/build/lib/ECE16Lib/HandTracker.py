#https://github.com/cvzone/cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
from ECE16Lib.CircularList import CircularList


class HandTracker:
    __detector = None
    __video = None
    __hands = None
    __handimg = None
    __rawimg = None
    __fingerCount = 0
    __fingerList = None

    def __init__(self, numSamples, maxHands=2, detectionCon=0.8, video=0):
        self.__detector = HandDetector(maxHands=maxHands, detectionCon=detectionCon)
        self.__video = cv2.VideoCapture(video)
        self.__fingerList = CircularList([], numSamples)

    def getHands(self):
        _, self.__rawimg = self.__video.read()
        self.__hands, self.__handimg = self.__detector.findHands(self.__rawimg, draw=True)

    def processImage(self):
        #output = []
        fingerCount = 0
        for hand in self.__hands:
            if hand:
                lmlist = hand
                if lmlist:
                    fingerup = self.__detector.fingersUp(lmlist)
                    fingerCount = fingerCount + sum(fingerup)
                    #whichHand = hand['type']
                    #handFingerCount = [whichHand, fingerup] # i.e. left, 1
                    #output.append(handFingerCount)
                    self.__fingerList.add(fingerCount)
            
        return fingerCount

    # def fingerCount(self, handFingerCount):
    #     count = 3
    #     for hand in handFingerCount:
    #         print('fix')


    # Check if same count has been held up for 1 second
    def checkFinger(self):
        recentVal = self.__fingerList[-1]
        for item in self.__fingerList:
            if item != recentVal:
                return False
            return True
    
    def showHands(self):
        cv2.imshow("Video", self.__rawimg)
        cv2.waitKey(1)
    
    def camReset(self):
        self.__video.release()
        cv2.destroyAllWindows()