from pyowm import OWM
import serial # the PySerial library
import time   # for timing purposes
from datetime import datetime

class Weather:
    __old_time_string = ""
    __owm = None

    def __init__(self):
        self.__old_time_string = ""
        self.__owm = OWM('89ed4bc1970c49b798031613be83f0d8').weather_manager()


    # Sending data example
    def get_weather(self):
        # get weather and date info
        weather = self.__owm.weather_at_place('San Diego,CA,US').weather
        now = datetime.now()

        # dd/mm/YY H:M:S
        # set up time string
        time_string = now.strftime("%H:%M")

        # else, if time has changed, get date and weather
        date_string = now.strftime("%d/%m")
        weather_string = str(int(weather.temperature('fahrenheit')['temp'])) + ' F'
    
        # put all together in CSV
        message = date_string + "," + time_string + "," + weather_string + "\n"
        self.__old_time_string = time_string # save current time
        return message