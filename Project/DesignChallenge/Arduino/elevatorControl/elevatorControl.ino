/*
 * Global variables
 */
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

void setup() {
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupLEDs();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Boot up: ", 0, true);
  }
  else if (command != ""){
      writeDisplay(command.c_str(),1, false);
    }
  

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ppg);
    sendMessage(response);
    
    writeDisplay(String(ppg).c_str(),2, false);
  }
}
