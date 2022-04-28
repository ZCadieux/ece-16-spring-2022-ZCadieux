from ECE16Lib.Communication import Communication
import time

if __name__ == "__main__":
  comms = comms = Communication("COM6", 115200) # COM6 is BT port
  comms.clear() # clear garbage data
  for t in range(30):
      t = t+1 # shift so it starts at 1 and ends at 30
      message = str(t) + " seconds" # generate message
      comms.send_message(message) # send message
      time.sleep(1) # wait 1 sec
      print(comms.receive_message()) # check for messages from arduino

  comms.close() # close communication
  print(comms)
