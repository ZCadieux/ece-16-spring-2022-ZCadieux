// Specify the LED pin
const int RLED_pin = 21;
const int YLED_pin = 17;
const int BLED_pin = 16;
const int GLED_pin = 19;

// Start LED logic as “OFF”
int RLED = LOW;
int BLED = LOW;
int YLED = LOW;
int GLED = LOW;

void setupLEDs()
{
  // Setup the LED for output
  pinMode(RLED_pin, OUTPUT);
  pinMode(BLED_pin, OUTPUT);
  pinMode(YLED_pin, OUTPUT);
  pinMode(GLED_pin, OUTPUT);
}

void RBYG_LED(bool red, bool blue, bool yellow, bool green)
{
  // input of True -> turn LED to high/on
  RLED = red ? HIGH : LOW;
  BLED = blue ? HIGH : LOW;
  YLED = yellow ? HIGH : LOW;
  GLED = green ? HIGH : LOW;

  //Set values of all LEDs
  digitalWrite(RLED_pin, RLED);
  digitalWrite(BLED_pin, BLED);
  digitalWrite(YLED_pin, YLED);
  digitalWrite(GLED_pin, GLED);
}
