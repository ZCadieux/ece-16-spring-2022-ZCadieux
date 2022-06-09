"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from time import sleep, time
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)
processTime = 0.05
speed_mult = 1.
speed = 1

class PygameController:
  comms = None
  

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")
    previousTime = time()

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    movecommand = None
    shootcommand = None
    processTime = 0.05
    speed_mult = 1.
    while True:
      message = self.comms.receive_message()
      # print(message)
      currentTime = time()
      try:
        buzz, _ = mySocket.recvfrom(1024)
        # print("buzz loop")
        buzz = buzz.decode('utf-8')
        self.comms.send_message("buzz")
      except BlockingIOError:
        # print("blocked")
        pass
      if(message != None):
        # print("NOT NONE!!!!!!!!!!!!!!!")
        # movecommand = None
        # shootcommand = None
        change = int(message[0])
        message = message[1:]
        message = int(message)
        print("change: ", change)
        print("message: ", message)
        move = message % 10
        print("move: ", move)
        shoot = message - move
        print("shoot: ", shoot)
        # if message == 0:
        #   command = "FLAT"
        # if message == 1:
        #   command = "UP"
        if shoot == 0:
          shootcommand = "FIRE"
        if shoot != 0:
          shootcommand = None
        if move == 3:
          movecommand = "LEFT"
        elif move == 4:
          movecommand = "RIGHT"
        if move == 0:
          movecommand = "FLAT"

        # if change == 2:
        #   speed_mult += 0.25
        #   if speed_mult == 1.75:
        #     speed_mult = 1.
        #   if speed_mult == 1:
        #     speed = 1
        #   if speed_mult == 1.25:
        #     speed = 2
        #   if processTime == 1.5:
        #     speed = 3
        #   mult2send = str(speed_mult)
        #   mySocket.send(mult2send.encode("UTF-8"))

        if change == 2:
          speed_mult += 1
          if speed_mult == 4:
            speed_mult = 1.
          if speed_mult == 1:
            speed = 1
          if speed_mult == 2:
            speed = 2
          if speed_mult == 3:
            speed = 3
          mult2send = str(speed_mult)
          mySocket.send(mult2send.encode("UTF-8"))
          message2display = "Speed: " + str(speed)
          self.comms.send_message(message2display)

        # print("speed: ", speed, " process time: ", processTime)

      if (abs(currentTime - previousTime)>processTime):
        if movecommand is not None:
          # print("movecommand: ", movecommand)
          mySocket.send(movecommand.encode("UTF-8"))
        if shootcommand is not None:
          # print("shootcommand: ", shootcommand)
          mySocket.send(shootcommand.encode("UTF-8"))
        previousTime = time()
        # sleep(0.01)


if __name__== "__main__":
  serial_name = "/dev/cu.gcmBT-ESP32SPP"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
