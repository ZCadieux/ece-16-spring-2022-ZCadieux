from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
import numpy as np
from time import time

if __name__ == "__main__":
  num_samples = 250        # 5 seconds of data @ 50Hz
  refresh_time = 0.1              # update the plot every 0.1s (10 FPS)
  idleCheckTime = 5 # check if idle for 5s
  activeCheckTime = 1 # check if active for 1s
  lastActive = time()
  lastInactive = time()
  cutoff = 40

  # raw data lists
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  # modified data lists
  average_x = CircularList([], num_samples)
  average_y = CircularList([], num_samples)
  average_z = CircularList([], num_samples)
  L2 = CircularList([], num_samples)
  L2_avg = CircularList([], num_samples)

  #initiate communication
  comms = Communication("COM4", 115200)
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
        n = 3 # num seconds to avg over
        vals2avg = np.array(ax[-50*n:])
        average_x.add(np.average(vals2avg))
        vals2avg = np.array(ay[-50*n:])
        average_y.add(np.average(vals2avg))
        vals2avg = np.array(az[-50*n:])
        average_z.add(np.average(vals2avg))
        
        #L2
        L2.add(np.sqrt(int(m2)**2 + int(m3)**2 + int(m4)**2))

        #L2_avg
        L2_avg.add(np.sqrt(average_x[-1]**2 + average_y[-1]**2 + average_z[-1]**2))

        # if enough time has elapsed, determine activity
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          """plt.cla()
          plt.plot(ax)
          plt.show(block=False)
          plt.pause(0.01)"""

          #print(L2[-1])
          #print(L2_avg[-1])
          # determine if there is a change in state
          if abs(L2[-1]-L2_avg[-1]) > cutoff: # condition for activity
            print('active')
            if(lastInactive+activeCheckTime < current_time): # if active for a second
              comms.send_message("active") # send active
              print('active 1 sec')
              lastActive = current_time # record time

          else: #if doesnt meet condition for activity
            if(lastActive+idleCheckTime < current_time): # if inactive for 5 seconds
              print('inactive 5 sec')
              comms.send_message("inactive") # send inactive
              lastInactive = current_time # record time

    
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()