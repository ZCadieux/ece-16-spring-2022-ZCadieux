int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; 
int ay = 0;
int az = 0;
int numTaps = 0;
int currentTime = millis();
int oldTime = currentTime;
int oldTapTime = currentTime;
int oldButtonTime = currentTime;
int prevState = HIGH;

//button GPIO pin
const int BUTTON_PIN = 14;

int watchState = 0;
/* watchStates
 *  0 = reset
 *  1 = increment
 *  2 = counting down
 */

void resetCount()
{
  // state 0, set numtaps to 0 and run buzzer
  numTaps = 0;
  activateMotor(0);
}

void detectButtonPush()
{
  //if button pushed, toggle counting on
  if(prevState == HIGH && digitalRead(BUTTON_PIN) == LOW)
  {
    oldButtonTime = currentTime;
  }
  //if button just released
  else if(prevState == LOW && digitalRead(BUTTON_PIN) == HIGH)
  {
    if(oldButtonTime+2000 <= currentTime)
    {
    watchState = 0;
    }
  }
  //if it has been 2 seconds of push & still held
  else if(digitalRead(BUTTON_PIN) == LOW && oldButtonTime+2000 <= currentTime)
  {
    watchState = 0;
  }
  prevState = digitalRead(BUTTON_PIN);
}

void tapTiming()
{
  if(currentTime-oldTapTime >= 4000 && numTaps > 0) // if 4 seconds have passed since last tap
  {
    watchState = 2;
  }
}

void countDown() 
{
  if(currentTime-oldTime >= 1000 && numTaps >0) // if a second has passed and we aren't at 0 yet
  {
    numTaps--; // decrease numTaps
    oldTime = currentTime; // update stored time
  }
  if(numTaps == 0)
  {
    watchState = 0;
  }
}

void printAccelVals()
{
  //Print vals for troubleshooting
  Serial.print("Current Values: ");
  Serial.print(ax); // average around 1955
  Serial.print(",");
  Serial.print(ay); // average around 1955
  Serial.print(",");
  Serial.println(az); // average around 2440
  Serial.println(numTaps);
}

void setup () {
     // run setup for all components, begin serial, and print initial statements on LCD
     setupAccelSensor();
     setupDisplay();
     pinMode(BUTTON_PIN, INPUT); //set up button
     setupMotor(); //setup motor
     Serial.begin(115200);
     
     String tapMessage = "Num Taps: "+String(numTaps);
     writeDisplay(tapMessage.c_str(), 0, false);
     String stateMessage = "Cur State: "+String(watchState);
     writeDisplay(stateMessage.c_str(), 1, false);
}

void loop() {
     // Note: we only print values when we have a new sample!!!
     // Also note that we added the second argument to the conditional to    
     // check if there is space in the buffer, otherwise it will stall when 
     // the buffer is full. Credit to Kyle for discovering the solution!
     if(sampleSensors() && Serial.availableForWrite()) {
          //print values to Serial
          //printAccelVals();

          //if new sample taken, and tap detected, increase number of taps
          numTaps = numTaps + detectTaps();

          //print tap count
          String tapMessage = "Num Taps: "+String(numTaps);
          writeDisplay(tapMessage.c_str(), 0, false);
          
          //print current state
          String stateMessage = "Cur State: "+String(watchState);
          writeDisplay(stateMessage.c_str(), 1, false);

          detectButtonPush(); // check for button push and hold
          tapTiming(); // check if 4 sec since last tap
          if(watchState == 0)
          {
            resetCount(); // reset if in reset state
            //activateMotor(0);
          }
          else
          {
            deactivateMotor(); // turn off motor if not in reset state
          }
          if(watchState == 2)
          {
            countDown(); // if in state 2, start counting down        
          }
     }
     currentTime = millis(); // record current time

     
}
