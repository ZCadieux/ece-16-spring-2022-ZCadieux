/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
String text = "";
int hr = 0;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable: ", 0, true);
  }
  else if(isDigit(command.charAt(0)))
  {
    if (command.toInt() != hr)
      hr = command.toInt();
      text = "HeartRate: " + String(hr);
      writeDisplay(text.c_str(), 0, true);
  }
  

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
  }
}
