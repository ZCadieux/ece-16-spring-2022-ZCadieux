/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
String oldcontrolcommand = "";
String controlcommand = "";


/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
//  setupPhotoSensor();
  setupMotor();
  setupButton();
  sending = false;

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Calibrating...", 0, true);
    calibrateZero();
    writeDisplay("Controller: On", 0, true);
  }
  if(command == "buzz") {
    activateMotor(100);
    delay(500);
    deactivateMotor();
  }
  if(command[0] == 'S') {
    writeDisplay(command.c_str(), 0, true);
  }

  controlcommand = String(getChange() + getOrientation() + getShoot());
  // Send the orientation of the board
  if(sending && sampleSensors() && controlcommand != oldcontrolcommand) {
    sendMessage(String(controlcommand));
    oldcontrolcommand = controlcommand;
  }
}
