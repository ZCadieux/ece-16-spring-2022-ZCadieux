int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;
String text = "";
int arrayLength = 500;
String accelData[500];
int accelIndex = 0;
const int BUTTON_PIN = 14;
int prevState = LOW;
int currentTime = millis();
int sendTime = millis();
String message2Send = "";

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
  pinMode(BUTTON_PIN, INPUT); //set up button
  //initialize digital pin LED_BUILTIN as an output
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if(command.length() > 0)
  {
    //display step and jump count
    writeDisplay("", 0, true);
    writeDisplayCSV(command.c_str(), 1);
  }
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    //sendMessage(response);  
    accelData[accelIndex] = response;
    accelIndex = accelIndex + 1;

    //display current index being collected
    String indexString = "Index: " + String(accelIndex);
    writeDisplay(indexString.c_str(),2, false);
    if(accelIndex >= arrayLength)
    {
      accelIndex = 0;
    }
  }
  //if button pushed, send data (with small debounce)
  if(prevState = HIGH && digitalRead(BUTTON_PIN) == LOW && currentTime-sendTime > 100)
  {
    //writeDisplay("Sending Data", 0, true);
    sendTime = currentTime;
    //create many messages to send back with data
    for(int i = 0; i<arrayLength; i = i+1)
    {
      message2Send = accelData[i];
      sendMessage(message2Send.c_str());
    }
  }
  //record previous state of button
  prevState = digitalRead(BUTTON_PIN);
       if (digitalRead(BUTTON_PIN) == LOW) {
          digitalWrite(LED_BUILTIN, HIGH);     
     }
     // if the button isn't pushed down, turn the LED off
     else {
          digitalWrite(LED_BUILTIN, LOW); // turn the LED off
     }
     currentTime = millis();
}
