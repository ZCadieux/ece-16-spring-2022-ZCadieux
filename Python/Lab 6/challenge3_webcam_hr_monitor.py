# Imports
from multiprocessing.sharedctypes import Value
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from matplotlib import pyplot as plt
from time import sleep
import time
import numpy as np
from hashlib import new
import cv2
plt.style.use('seaborn-whitegrid')

# Collect num_samples from the MCU
fs = 10 # sampling rate hz
num_samples = 120 # 2 min of data @ 10Hz
process_time = 1

hrm = HRMonitor(num_samples, fs)

comms = Communication("COM5", 115200)
comms.clear()
comms.send_message("wearable")
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
sleep(1)
try:
    previous_time = time.time()
    while(True):
        _, frame = cap.read()
        new_sample = frame.mean(axis=0).mean(axis=0)
        new_sample = -new_sample[2] # replace the ? with index of the RED channel            
        hrm.add(time.time_ns()/1e9, int(new_sample))

        # if enough time has elapsed, process the data and plot it
        current_time = time.time()
        if (current_time - previous_time > process_time):
          print('Processing...')
          previous_time = current_time
          try:
            hr, peaks, filtered = hrm.process()
          except(ValueError) as e:
              print(e)
          if peaks == 0:
              continue
          print("Heart Rate: {:f}".format(hr))

          plt.cla()
          plt.plot(filtered)
          plt.title("Heart Rate: %d" % hr)
          plt.show(block=False)
          plt.pause(0.001)
          print(str(int(hr)))
          comms.send_message(str(int(hr)))

except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
finally:
    print("Sleep")
    comms.send_message("sleep") # stop sending data
    comms.close()
    cap.release()
    cv2.destroyAllWindows()