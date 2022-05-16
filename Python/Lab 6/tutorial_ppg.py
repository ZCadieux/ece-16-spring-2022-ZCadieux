from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
import numpy as np

if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 1                # plot every second

  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)
  ppg = CircularList([], num_samples)

  comms = Communication("COM5", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = time()
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4, m5) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))
        ppg.add(int(m5))

        # if enough time has elapsed, clear the axes, and plot the 4 plots
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          plt.clf()
          plt.subplot(411)
          plt.plot(ax)
          plt.subplot(412)
          plt.plot(ay)
          plt.subplot(413)
          plt.plot(az)
          plt.subplot(414)
          plt.plot(ppg)
          plt.show(block=False)
          plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()