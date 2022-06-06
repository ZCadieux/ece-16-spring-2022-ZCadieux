from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HandTracker import HandTracker
from matplotlib import pyplot as plt
import ECE16Lib.DSP as filt
from time import time
from time import sleep
import numpy as np
import traceback

if __name__ == "__main__":
    num_samples = 100              #5 seconds of data @ 50Hz
    process_time = .1            #check finger count 60 times a second
    
    tracker = HandTracker(num_samples) # HandTracker using defaults of 2, .8, 0
    rawRange = CircularList([], num_samples)
    rangeVals = CircularList([], num_samples)
    threshold = 100

    comms = Communication('COM3', 115200)
    comms.clear()                   # just in case any junk is in the pipes
    comms.send_message("wearable")  # begin sending data
    sleep(1)
    try:
        previous_time = time()
        while(True):
            message = comms.receive_message()
            if(message != None):
                try:
                    (ardTime, rawPPG) = message.split(',')
                    rawRange.add(int(rawPPG))
                    print(rawPPG)
                except ValueError:        # if corrupted data, skip the sample
                    continue

            #Read in video
            tracker.getHands() #get data

            ppg = np.array(rawRange)
            #rangeVals = filt.detrend(ppg)

            print(rawRange[-1])
            fingCount = tracker.processImage() #process image

            #print(str(fingCount))
            comms.send_message(str(fingCount))
            tracker.showHands()


            # if enough time has elapsed, process the data and plot it
            current_time = time()
            if (current_time - previous_time > process_time):
                previous_time = current_time

                plt.cla()
                plt.plot(ppg)
                plt.title("Range (PPG)")
                plt.show(block=False)
                plt.pause(0.001)

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
        print(traceback.format_exc())
    finally:
        print("Closing connection.")
        comms.send_message("sleep")  # stop sending data
        comms.close()

        tracker.camReset()