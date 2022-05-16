Tutorial 1 questions:

1. This works because the sensor is something that is read from, while the OLED is written to, so they should be able to use the same wires to communicate since all readings will be from the heartbeat sensor and all writing will be to the OLED.

2. The while(1) statement makes it such that if the device is not connected, the Arduino will not exit setup, looping continuously in that location with the error as the last thing printed. If the error is printed and the device connected, the code will not proceed until the Arduino is reset.

3. 

``` C++
//Setup to sense a nice looking saw tooth on the plotter
byte ledBrightness = 0x19; //Options: 0=Off to 255=50mA
byte sampleAverage = 8; //Options: 1, 2, 4, 8, 16, 32
byte ledMode = 2; //Options: 1 = Red only, 2 = Red+IR, 3 = Red+IR+Green
int sampleRate = 200; //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200
int pulseWidth = 411; //Options: 69, 118, 215, 411
int adcRange = 8192; //Options: 2048, 4096, 8192, 16384
```

4. Hz, a bigger pulse would result in a more intense measurement because it is interpreted by PWM as a larger command signal.

5. 14

6. Red: 670 nm, IR: 900 nm, Green: 545 nm
