from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HandTracker import HandTracker
from matplotlib import pyplot as plt
from time import time
import numpy as np

if __name__ == "__main__":
    num_samples = 500              # 5 seconds of data @ 50Hz
    process_time = .5                # compute the step count every second
    
    tracker = HandTracker() # HandTracker using defaults of 2, .8, 0

    comms = Communication('COM6', 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data

    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (m1, m2, m3, m4) = message.split(',')
                except ValueError:        # if corrupted data, skip the sample
                    continue

            #Read in video
            fingCount = tracker.getHands()
            comms.send_message(str(fingCount))

            # # if enough time has elapsed, process the data and plot it
            # current_time = time()
            # if (current_time - previous_time > process_time):
            #     print("run stuff")

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()