int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;
// State -1 = idle, 0 = inactive, 1 = active
int state = -1; //start idle until data collected

void inactiveState()
{ 
  activateMotor(255); //activate buzzer
}

void activeState()
{
  activateMotor(0); //turn off buzzer
} 

void stateAction() // perform action based on current state
{
  if(state == 0)
  {
    inactiveState();
  }
  else if(state == 1)
  {
    activeState();
  }
}


void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
  setupMotor(); //setup motor
}

void loop() {
  String command = receiveMessage();
  //writeDisplay(command.c_str(), 1, false);
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  if(sending && sampleSensors()) {
    //writeDisplay("Test2", 2, false);
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);
        
  }
  if(command=="active" && state != 1)
    {
      state = 1;
      writeDisplay("Active!", 0, true);
    }
    else if(command=="inactive" && state != 0)
    {
      state = 0;
      writeDisplay("Inactive!", 0, true); 
    }
  stateAction();
}
