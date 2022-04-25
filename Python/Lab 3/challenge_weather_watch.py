from pyowm import OWM
import serial # the PySerial library
import time   # for timing purposes
from datetime import datetime

old_time_string = ""

def setup(serial_name, baud_rate):
    # initial setup
    ser = serial.Serial(serial_name, baudrate=baud_rate)
    return ser

def close(ser):
    ser.close()

def send_message(ser, message):
   if(message[-1] != '\n'):
       message = message + '\n'
   ser.write(message.encode('utf-8'))

# Sending data example
def main(ser):
    # get weather and date info
    owm = OWM('89ed4bc1970c49b798031613be83f0d8').weather_manager()
    weather = owm.weather_at_place('San Diego,CA,US').weather
    now = datetime.now()

    # using a global variable to save in between function calls
    global old_time_string

    # dd/mm/YY H:M:S
    # set up time string
    time_string = now.strftime("%H:%M:%S")
    if(time_string == old_time_string): # if time has not changed
        return # stop running

    # else, if time has changed, get date and weather
    date_string = now.strftime("%d/%m/%Y")
    weather_string = str(weather.temperature('fahrenheit')['temp']) + ' deg F'
    
    # put all together in CSV
    message = date_string + "," + time_string + "," + weather_string + "\n"
    send_message(ser, message) # send over bluetooth
    old_time_string = time_string # save current time

"""
Main entrypoint for the application
"""
if __name__== "__main__":
    ser = setup("COM6", 115200) # set up outside of loop to avoid autoclearing LCD
    while(True):
        main(ser) # run alg constantly