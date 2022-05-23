# Imports
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import sleep
from time import time
import numpy as np

# Collect num_samples from the MCU
fs = 50 # sampling rate hz
num_samples = 250 # 1 min of data @ 50Hz
process_time = 1

hrm = HRMonitor(num_samples, fs)
hrm.train(".\\data") #train the GMM

# Begin live data inputs
print("Starting Comms!")
comms = Communication("COM5", 115200)
comms.clear()
comms.send_message("wearable")
sleep(1)
try:
    previous_time = time()
    while(True):
        message = comms.receive_message()
        if(message!=None):
            try:
                (m1, _, _, _, m2) = message.split(',') # take in only necessary input data
                hrm.add(int(m1)/1e3, int(m2)) # adjust time scaling
            except ValueError:
                continue

        # if enough time has elapsed, process the data and plot it
        current_time = time()
        if (current_time - previous_time > process_time):
          previous_time = current_time
          hr, peaks, filtered = hrm.predict()
          
          print("Heart Rate: {:f}".format(hr))

          plt.cla()
          plt.plot(filtered)
          plt.title("Heart Rate: %d" % hr)
          plt.show(block=False)
          plt.pause(0.01)
          comms.send_message(str(int(hr)))

except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
    print("Error in main loop")
finally:
    comms.send_message("sleep") # stop sending data
    comms.close()