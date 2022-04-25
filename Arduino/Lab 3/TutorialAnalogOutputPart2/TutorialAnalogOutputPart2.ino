void setup () {
     setupMotor();
      Serial.begin(115200);
}

void loop() {
     //test motor at different duty cycles
     deactivateMotor();
     Serial.println("Deactivate");
     delay(2000);
     activateMotor(127);
     Serial.println("127");
     delay(2000);
     activateMotor(255);
     Serial.println("255");
     delay(2000);
     activateMotor(90);
     Serial.println("90");
     delay(2000);
}
