from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
import numpy as np
if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 500               # 5 seconds of data @ 50Hz
  process_time = .001                # compute the step count every second
  ped = Pedometer(num_samples, fs, [], 25, 125, 125, 300)
  comms = Communication("COM5", 921600)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data
  samples = []
  newData = False
  steps, peaks_s, jumps, peaks_j, filtered = 0,0,0,0,0
  try:
    previous_time = time()
    while(True):
      message = comms.receive_message(288)
      newData = False
      # check if messages come through
      if(message != None):
        newData = True
        while(message != None):
          samples.append(message) # add to sample array
          message = comms.receive_message(288)
        try:
          for data in samples: # process sample array into data, add to pedometer
            if data != ['\r\n'] and len(data.split(",")) == 4:
              print(data.split(","))
              (m1, m2, m3, m4) = data.split(',')
              ped.add(int(m2),int(m3),int(m4))
        except ValueError as e:        # if corrupted data, skip the sample
          print(e)
          print("Bad Data")
          continue

        print("Processing...")
        steps, peaks_s, jumps, peaks_j, filtered = 0,0,0,0,0
        try: # try to process data, might go wrong if read in errors
          steps, peaks_s, jumps, peaks_j, filtered = ped.process()
        except(ValueError) as e:
            print("Bad Process")
            print(e)
        print("Step count: {:d}".format(steps))
        print("Jump count: {:d}".format(jumps))
        comms.send_message("Steps: " + str(steps) + ",Jumps: " + str(jumps)) # send results to Arduino

      current_time = time()
      if (current_time - previous_time > process_time or newData):
      # plot data locally
        previous_time = current_time
        plt.cla()
        plt.plot(filtered)
        plt.axhline(y = 25)
        plt.axhline(y = 125)
        plt.axhline(y = 300)
        title_string = "Step Count: " + str(steps) + " Jump Count: " + str(jumps)
        plt.title(title_string)
        plt.show(block=False)
        plt.pause(0.001)

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()