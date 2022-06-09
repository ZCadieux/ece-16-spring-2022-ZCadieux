from ECE16Lib.Communication import Communication
from ECE16Lib.HandTracker import HandTracker
from time import time
from time import sleep
import traceback

if __name__ == "__main__":
    num_samples = 40          
    process_time = .5          
    
    tracker = HandTracker(num_samples) # HandTracker using defaults of 2, .8, 0
    threshold = 100
    getFloor = False
    fingCount = 0
    moving = False

    comms = Communication('COM5', 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    sleep(1)
    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    if("Hand" in message):
                        if not getFloor:
                            getFloor = True
                            previous_time = current_time
                        else:
                            print("Cancelled")
                            comms.send_message("cancelled")
                            getFloor = False
                    if("Arrived" in message):
                        moving = False
                        print("Arrived!")
                    if("moving" in message and not moving):
                        print("Moving...")
                        moving = True
                        continue

                except ValueError:        # if corrupted data, skip the sample
                    continue

            if(moving):
                continue

            #Read in video
            tracker.getHands() #get data
            comms.send_message(str(fingCount))
            tracker.showHands()

            fingCount = tracker.processImage() #process image


            # if enough time has elapsed, process the data and plot it
            current_time = time()
            if (current_time - previous_time > process_time):
                previous_time = current_time
                if(getFloor):
                    print("Checking for Floor...")
                    #print(tracker.checkFinger())
                    if(tracker.checkFinger()):
                        comms.send_message("Floor " + str(fingCount))
                        getFloor = False
                        print("Sent floor!")

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
        print(traceback.format_exc())
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()

        tracker.camReset()