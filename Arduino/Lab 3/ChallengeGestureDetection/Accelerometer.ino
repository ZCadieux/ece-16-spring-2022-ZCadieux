const int X_PIN = A2;
const int Y_PIN = A3;
const int Z_PIN = A4;

void setupAccelSensor()
{
  //define pins as inputs 
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

void readAccelSensor()
{
  //read in current values and set global vars
  ax = analogRead(X_PIN);
  ay = analogRead(Y_PIN);
  az = analogRead(Z_PIN);
}
