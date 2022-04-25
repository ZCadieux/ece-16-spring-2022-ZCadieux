int ax = 0;
int ay = 0;
int az = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  setupAccelSensor();

}

void loop() {
  // put your main code here, to run repeatedly:
  readAccelSensor();
  //print values
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.println(az);

}
