# Imports
from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Pedometer import Pedometer
from ECE16Lib.IdleDetector import IdleDetector
from ECE16Lib.Weather import Weather
from matplotlib import pyplot as plt
from time import sleep
from time import time
import numpy as np

# Collect num_samples from the MCU
fs = 50 # sampling rate hz
num_samples = 250 # 1 min of data @ 50Hz
process_time = 1

# Initialize objects
weth = Weather()
ped = Pedometer(num_samples, fs, [])
det = IdleDetector()
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
            #print(message)
            if "reset" in message:
                ped.reset()
                hrm.reset()
                continue
            try:
                (m1, ax, ay, az, m2) = message.split(',') # take in all necessary input data
                hrm.add(int(m1)/1e3, int(m2)) # adjust time scaling
                ped.add(int(ax),int(ay),int(az))
            except ValueError:
                continue

        # if enough time has elapsed, process the data and plot it
        current_time = time()
        if (current_time - previous_time > process_time):
          previous_time = current_time

          #print("Weather")
          weather = weth.get_weather()
          #print("HRMonitor")
          try:
            hr, peaks, filtered_hrm = hrm.predict()
          except:
              print("HRM error")
              continue
          #print("Pedometer")
          try:
            steps, peaks, jumps, jumpPeaks, filtered_ped = ped.process()
          except ValueError as e:
            print("Pedometer Error")
            print(e)
            continue
          #print("Idle Detector")
          status = det.detectIdle(str(m1) + ',' + str(ax) + ',' + str(ay) + ',' + str(az))
          
          print("Heart Rate: {:f}".format(hr))
          print("Step Count: {:f}".format(steps))
          print("Status:", status)
          print("Weather:", weather)

          """
          plt.cla()
          plt.subplot(211)
          plt.plot(filtered_hrm)
          plt.title("Heart Rate: %d" % hr)

          plt.subplot(212)
          plt.plot(filtered_ped)
          plt.title("Step Count: %d" % steps)

          plt.show(block=False)
          plt.pause(0.001)"""
          comms.send_message("HR:" + str(int(hr)) + " Steps:" + str(int(steps)) + ",Status: " + status + "," + weather)
          print("HR: " + str(int(hr)) + ",Steps: " + str(int(steps)) + ",Status: " + status + "," + weather)

except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
    print("Error in main loop")
finally:
    comms.send_message("sleep") # stop sending data
    comms.close()