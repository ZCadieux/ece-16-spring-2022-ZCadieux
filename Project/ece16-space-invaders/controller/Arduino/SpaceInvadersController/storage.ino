// SPACEINVADERSCONTROLLER
///*
// * Global variables
// */
//// Acceleration values recorded from the readAccelSensor() function
//int ax = 0; int ay = 0; int az = 0;
//int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
//int sampleTime = 0; // Time of last sample (in Sampling tab)
//bool sending;
//String oldcontrolcommand = "";
//String controlcommand = "";
//
//
///*
// * Initialize the various components of the wearable
// */
//void setup() {
//  setupAccelSensor();
//  setupCommunication();
//  setupDisplay();
//  setupPhotoSensor();
//  setupMotor();
//  setupButton();
//  sending = false;
//
//  writeDisplay("Ready...", 1, true);
//  writeDisplay("Set...", 2, false);
//  writeDisplay("Play!", 3, false);
//}
//
///*
// * The main processing loop
// */
//void loop() {
//  // Parse command coming from Python (either "stop" or "start")
//  String command = receiveMessage();
//  if(command == "stop") {
//    sending = false;
//    writeDisplay("Controller: Off", 0, true);
//  }
//  else if(command == "start") {
//    sending = true;
//    writeDisplay("Calibrating...", 0, true);
//    calibrateZero();
//    writeDisplay("Controller: On", 0, true);
//  }
//  if(command == "buzz") {
//    activateMotor(100);
//    delay(500);
//    deactivateMotor();
//  }
//
//  controlcommand = String(getOrientation() + getShoot());
//  // Send the orientation of the board
//  if(sending && sampleSensors() && controlcommand != oldcontrolcommand) {
//    sendMessage(String(controlcommand));
//    oldcontrolcommand = controlcommand;
//  }
//}


// BUTTON
//const int BUTTON_PIN1 = 14;
////const int BUTTON_PIN2 = 32;
//int prevState1 = LOW;
//int buttonTime1 = millis();
//int curTime1 = millis();
////int prevState2 = LOW;
////int buttonTime2 = millis();
////int curTime2 = millis();
//
//void setupButton()
//{
//  pinMode(BUTTON_PIN1, INPUT);
////  pinMode(BUTTON_PIN2, INPUT);
//}
//
//int getShoot()
//{
//  curTime1 = millis();
//   if(prevState1 == LOW && digitalRead(BUTTON_PIN1) == HIGH && curTime1-buttonTime1 >= 10)
//  {
//    return 10; //shoot command
//    buttonTime1 = curTime1;
//  }
//  prevState1 = digitalRead(BUTTON_PIN1);
//  return 0; //don't shoot
//}
//
////int getChange()
////{
////  curTime2 = millis();
////   if(prevState2 == LOW && digitalRead(BUTTON_PIN2) == HIGH && curTime2-buttonTime2 >= 10)
////  {
////    return 100; //change speed command
////    buttonTime2 = curTime2;
////  }
////  prevState2 = digitalRead(BUTTON_PIN2);
////  return 200; //don't change speed
////}
