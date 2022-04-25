const int accelX = A0;

void setup() {
  // put your setup code here, to run once:
  // Begin the Serial communication (you did this in the last lab!)
  Serial.begin(9600);
  // Define the analog pin as input
  pinMode(accelX, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int accel_val = analogRead(accelX);
  // Print the value (you did this in the last lab too)
  Serial.println(accel_val);

}
