from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from ECE16Lib.Pedometer import Pedometer
from matplotlib import pyplot as plt
from time import time
import numpy as np

if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 500               # 5 seconds of data @ 50Hz
  process_time = .5                # compute the step count every second

  ped = Pedometer(num_samples, fs, [])

  comms = Communication("COM5", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = time()
    while(True):
      message = comms.receive_message()
      if(message != None):
        print(message)
        try:
          print(message)
          data = message.splitlines()
          print("Data:")
          print(data)
          print("Split Data:")
          for entry in data:
            print(entry.split(','))
            (m1, m2, m3, m4) = entry.split(',')
            ped.add(int(m2),int(m3),int(m4))
            #print("Added to ped")
          print("Data Added!")
        except ValueError as e:        # if corrupted data, skip the sample
          print(e)
          print("Bad Data")
          continue

        # # Collect data in the pedometer
        # ped.add(int(m2),int(m3),int(m4))

        # if enough time has elapsed, process the data and plot it
        current_time = time()
        if (current_time - previous_time > process_time):
          print("Processing...")
          previous_time = current_time
          steps, peaks_s, jumps, peaks_j, filtered = 0,0,0,0,0
          try:
            steps, peaks_s, jumps, peaks_j, filtered = ped.process()
          except(ValueError) as e:
            print("Bad Process")
            print(e)


          print("Step count: {:d}".format(steps))
          print("Jump count: {:d}".format(jumps))

          plt.cla()
          plt.plot(filtered)
          plt.axhline(y = 10)
          plt.axhline(y = 150)
          title_string = "Step Count: " + steps + " Jump Count: " + jumps
          plt.title(title_string)
          plt.show(block=False)
          plt.pause(0.001)
          comms.send_message("Steps: " + str(steps) + ",Jumps: " + str(jumps))

  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()