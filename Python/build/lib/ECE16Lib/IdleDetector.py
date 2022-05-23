from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
import numpy as np
from time import time

"""
A class to handle Idle detection based on accelerometer data
"""
class IdleDetector:
  '''
  Encapsulated class attributes (with default values)
  '''
  __comms = None
  __num_samples = 250        # 5 seconds of data @ 50Hz
  __refresh_time = 0.1              # update the plot every 0.1s (10 FPS)
  __idleCheckTime = 5 # check if idle for 5s
  __activeCheckTime = 1 # check if active for 1s
  __lastActive = time()
  __lastInactive = time()
  __cutoff = 50
  __current_time = time()

  # raw data lists
  times = CircularList([], __num_samples)
  ax = CircularList([], __num_samples)
  ay = CircularList([], __num_samples)
  az = CircularList([], __num_samples)

  # modified data lists
  average_x = CircularList([], __num_samples)
  average_y = CircularList([], __num_samples)
  average_z = CircularList([], __num_samples)
  L2 = CircularList([], __num_samples)
  L2_avg = CircularList([], __num_samples)

  '''
  Initialize the class instance
  '''
  def __init__(self, serial_name=None, baud_rate=None):
    if(serial_name != None):
      self.__comms = Communication(serial_name, baud_rate)
      self.__comms.clear()                   # just in case any junk is in the pipes
      self.__comms.send_message("wearable")  # begin sending data

  def __add_data(self, message):
    try: 
      (m1, m2, m3, m4) = message.split(',') # split up info
    except ValueError:        # if corrupted data, skip the sample
        return
    
    # add accelerometer data to lists
    self.times.add(int(m1))
    self.ax.add(int(m2))
    self.ay.add(int(m3))
    self.az.add(int(m4))

  def __modified_data(self, message):
    try: 
      (m1, m2, m3, m4) = message.split(',') # split up info
    except ValueError:        # if corrupted data, skip the sample
        return
    # modified data lists
    #average_x
    n = 3 # num seconds to avg over
    vals2avg = np.array(self.ax[-50*n:])
    self.average_x.add(np.average(vals2avg))
    vals2avg = np.array(self.ay[-50*n:])
    self.average_y.add(np.average(vals2avg))
    vals2avg = np.array(self.az[-50*n:])
    self.average_z.add(np.average(vals2avg))

    #L2
    self.L2.add(np.sqrt(int(m2)**2 + int(m3)**2 + int(m4)**2))

    #L2_avg
    self.L2_avg.add(np.sqrt(self.average_x[-1]**2 + self.average_y[-1]**2 + self.average_z[-1]**2))

  def __activity_check(self):
    #print('active')
    if(self.__lastInactive+self.__activeCheckTime < self.__current_time): # if active for a second
        if self.__comms != None:
          self.__comms.send_message("active") # send active
        #print('active 1 sec')
        self.__lastActive = self.__current_time # record time
        return True
    return False

  def __inactivity_check(self):
    if(self.__lastActive+self.__idleCheckTime < self.__current_time): # if inactive for 5 seconds
        print('inactive 5 sec')
        if self.__comms != None:
          self.__comms.send_message("inactive") # send inactive
        self.__lastInactive = self.__current_time # record time
        return True
    return False

  def __plot(self):
      plt.cla()
      plt.plot(self.ax)
      plt.plot(self.ay)
      plt.plot(self.az)
      plt.show(block=False)
      plt.pause(0.01)

  def detectIdle(self, message):
    try:
      previous_time = 0
      if(message != None):
          self.__add_data(message)
          self.__modified_data(message)
          self.__current_time = time()

          if (self.__current_time - previous_time > self.__refresh_time):
              previous_time = self.__current_time
              #self.__plot()
              #print("activity check")
              if abs(self.L2[-1]-self.L2_avg[-1]) > self.__cutoff: # condition for activity
                  if self.__activity_check():
                    return "active"

              else: #if doesnt meet condition for activity
                  if self.__inactivity_check():
                    return "inactive"
              return "idle"

    except(Exception, KeyboardInterrupt) as e:
        print(e)                     # Exiting the program due to exception
        print("Error in IdleDetector")

