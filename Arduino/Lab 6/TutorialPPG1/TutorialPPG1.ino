int sampleTime = 0; // Time of last sample (in Sampling tab)
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)

void setup() {
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
}

void loop() {
  if(sampleSensors()) {
    sendMessage(String(ppg));
  }
}
