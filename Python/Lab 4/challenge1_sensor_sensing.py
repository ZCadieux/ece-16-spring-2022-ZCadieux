from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
import numpy as np
from time import time

if __name__ == "__main__":
  num_samples = 100        # 5 seconds of data @ 50Hz
  refresh_time = 0.01              # update the plot every 0.1s (10 FPS)

  # raw data lists
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  # modified data lists
  average_x = CircularList([], num_samples)
  delta_x = CircularList([], num_samples)
  L1 = CircularList([], num_samples)
  L2 = CircularList([], num_samples)
  transformed = CircularList([], num_samples)

  #initiate communication
  comms = Communication("COM6", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue


        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        # modified data lists
        #average_x
        n = 1 # num seconds to avg over
        vals2avg = np.array(ax[-50*n:])
        average_x.add(np.average(vals2avg))

        #delta_x
        delta_x.add(ax[-2]-ax[-1])

        #L2
        L2.add(np.sqrt(int(m2)**2 + int(m3)**2 + int(m4)**2))

        #L1
        L1.add(np.abs(int(m2)) + np.abs(int(m3)) + np.abs(int(m4)))

        #norm_x
        transformed.add(int(m2)/L2[-1])


        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          plt.clf()

          # plotting raw data
          #plt.subplot(311)
          plt.plot(ax)
          #plt.subplot(312)
          plt.plot(ay)
          #plt.subplot(313)
          plt.plot(az)

          # plotting transformed data
          """plt.subplot(814)
          plt.plot(average_x)
          plt.subplot(815)
          plt.plot(delta_x)
          plt.subplot(816)
          plt.plot(L2)
          plt.subplot(817)
          plt.plot(L1)
          plt.subplot(818)
          plt.plot(transformed)"""


          plt.show(block=False)
          plt.pause(0.001)
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()