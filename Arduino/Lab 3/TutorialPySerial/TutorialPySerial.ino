void setup() {
  setupCommunication();
  setupDisplay();
}

void loop() {
  String message = receiveMessage();
  if(message != "") {
    writeDisplay(message.c_str(), 0, true);
    sendMessage(message);
  }
}
