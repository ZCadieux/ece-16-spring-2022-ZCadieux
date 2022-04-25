void setup() {
  // set up modules, using bluetooth
  setupCommunication();
  setupDisplay();
}

void loop() {
  // check for messages
  String message = receiveMessage();
  if(message != "") {
    // print messages from CSV
    writeDisplayCSV(message.c_str(), 2);
    sendMessage(message);
  }
}
