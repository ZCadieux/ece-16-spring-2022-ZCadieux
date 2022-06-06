/*
   Global variables
*/
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
int targetFloor = 1;
int currentFloor = 1;
bool movingFloor = false;
int lastFloorMove = millis();

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
  if (command == "sleep") {
    RBYG_LED(false, false, false, false);
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if (command == "wearable") {
    sending = true;
    writeDisplay("Boot up: ", 0, true);
    RBYG_LED(false, false, false, true);
  }
  else if (command == "cancelled")
  {
    writeDisplay("Cancelled", 3, true);
  }
  else if (command.indexOf("Floor") >= 0)
  {
    movingFloor = true;
    targetFloor = command.substring(command.indexOf(" ") + 1).toInt();
    if(targetFloor == 0 || targetFloor == currentFloor)
    {
      writeDisplay("Invalid Floor", 1, true);
      movingFloor = false;
    }
    String targetFloorString = "Target:" + String(targetFloor);
    writeDisplay(targetFloorString.c_str(), 1, true);
    RBYG_LED(true, false, false, false);
  }
  //if (command != "") {
    //writeDisplay(command.c_str(), 1, false);
  //}

  if (movingFloor && lastFloorMove + 1000 < millis())
  {
    RBYG_LED(false, true, false, false);
    lastFloorMove = millis();
    if (targetFloor - currentFloor > 0) //going up
    {
      currentFloor = currentFloor + 1;
    }
    else if (targetFloor - currentFloor < 0)
    {
      currentFloor = currentFloor - 1;
    }
    else if (targetFloor == currentFloor)
    {
      movingFloor = false;
      sendMessage("Arrived");
      writeDisplay("Arrived!", 3, true);
    }
  }

  if (sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ppg);
    RBYG_LED(false, false, true, true);
    if (movingFloor) {
      sendMessage("moving");
      writeDisplay("Moving...", 3, true);
    }
    if (checkForHand())
    {
      RBYG_LED(true, true, false, false);
      sendMessage("Hand");
      writeDisplay("Which Floor?", 3, true);
    }
    String curFloorString = "Cur Floor:" + String(currentFloor);
    writeDisplay(curFloorString.c_str(), 0, false);
    //writeDisplay(String(ppg).c_str(), 2, false);
  }
}
