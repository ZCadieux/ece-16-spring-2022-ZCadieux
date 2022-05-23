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
const int BUTTON_PIN = 14;
int prevState = LOW;
String activity = "";

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  setupMotor();
  sending = false;
  writeDisplay("Sleep", 0, true);

  pinMode(BUTTON_PIN, INPUT);  
  pinMode(LED_BUILTIN, OUTPUT);
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
    writeDisplay("Boot up: ", 0, true);
  }
  

  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    sendMessage(response);
    if (command != ""){
      writeDisplayCSV(command, 3);
    }
  }
  if(prevState == LOW && digitalRead(BUTTON_PIN) == HIGH)
  {
    sendMessage("reset");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(10);
  }
  prevState = digitalRead(BUTTON_PIN);
  digitalWrite(LED_BUILTIN, LOW);

  if(activity == "inactive")
  {
    activateMotor(255);
  }
  else
  {
    deactivateMotor();
  }
}
