#https://github.com/cvzone/cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
from ECE16Lib.CircularList import CircularList

"""
A class to use openCV and cvzone to detect a hand in the FOV of the camera, 
and count how many fingers are being held up.
"""
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

    # Takes in image from webcam
    def getHands(self):
        _, self.__rawimg = self.__video.read()
        self.__hands, self.__handimg = self.__detector.findHands(self.__rawimg, draw=True)

    # Checks image for fingers
    def processImage(self):
        fingerCount = 0
        for hand in self.__hands:
            if hand:
                lmlist = hand
                if lmlist:
                    fingerup = self.__detector.fingersUp(lmlist)
                    fingerCount = fingerCount + sum(fingerup)

        self.__fingerList.add(fingerCount)
        return fingerCount

    # Check if same count has been held up for 1 second
    def checkFinger(self):
        print(self.__fingerList)
        recentVal = self.__fingerList[-1]
        for item in self.__fingerList:
            if item != recentVal:
                #print("Not the same!")
                return False
        return True
    
    # Show image on the screen
    def showHands(self):
        cv2.imshow("Video", self.__rawimg)
        cv2.waitKey(1)
    
    # Release camera and close openCV
    def camReset(self):
        self.__video.release()
        cv2.destroyAllWindows()

    # zero out finger list
    def listReset(self):
        self.__fingerList.clear()