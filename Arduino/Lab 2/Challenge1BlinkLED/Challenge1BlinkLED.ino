// Specify the LED pin
const int RLED_pin = 13;
const int BLED_pin = 14;
const int GLED_pin = 12;

// Initialize time for LED
unsigned long rbefore_time = millis();
unsigned long bbefore_time = millis();
unsigned long gbefore_time = millis();

// How long the LED stays on or off for each color
int rperiod;
int bperiod;
int gperiod;

// red times
int ron_period = 1000;
int roff_period = 100;

//blue times
int bon_period = 200;
int boff_period = 50;

//green times
int gon_period = 20;
int goff_period = 10;

// Start LED logic as “OFF”
int RLED = LOW;
int BLED = LOW;
int GLED = LOW;

void setup() {
  // Setup the LED for output
  pinMode(RLED_pin, OUTPUT);
  pinMode(BLED_pin, OUTPUT);
  pinMode(GLED_pin, OUTPUT);
}

void loop() {
  // Get the current time every time we loop
  unsigned long now_time = millis();

  // Check if enough time has elapsed and updates the LED logic state for each color
  // Also change the period for different durations of ON/OFF times
  if (now_time - rbefore_time >= rperiod){ //RED LED
    rbefore_time = millis(); //update before time

    if (RLED == LOW) {
      RLED = HIGH;
      rperiod = ron_period;
    }
    else {
      RLED = LOW;
      rperiod = roff_period;
    }
  }
  
  if (now_time - bbefore_time >= bperiod){ //Blue LED
    bbefore_time = millis(); //update before time
        if (BLED == LOW) {
      BLED = HIGH;
      bperiod = bon_period;
    }
    else {
      BLED = LOW;
      bperiod = boff_period;
    }
    }
    if (now_time - gbefore_time >= gperiod){ //Green LED
    gbefore_time = millis(); //update before time

      if (GLED == LOW) {
      GLED = HIGH;
      gperiod = gon_period;
    }
    else {
      GLED = LOW;
      gperiod = goff_period;
    }
  }
  //Set values of all LEDs
  digitalWrite(RLED_pin, RLED);
  digitalWrite(BLED_pin, BLED);
  digitalWrite(GLED_pin, GLED);
}
