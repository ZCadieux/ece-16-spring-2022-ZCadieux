int sampleTime = 0; // Time of last sample (in Sampling tab)
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; 
int ay = 0;
int az = 0;

void setup () {
     setupAccelSensor();
     setupDisplay();
     Serial.begin(9600);
}

void loop() {
     // Note: we only print values when we have a new sample!!!
     // Also note that we added the second argument to the conditional to    
     // check if there is space in the buffer, otherwise it will stall when 
     // the buffer is full. Credit to Kyle for discovering the solution!
     if(sampleSensors() && Serial.availableForWrite()) {
          Serial.print(ax);
          Serial.print(",");
          Serial.print(ay);
          Serial.print(",");
          Serial.println(az);
     }
}
