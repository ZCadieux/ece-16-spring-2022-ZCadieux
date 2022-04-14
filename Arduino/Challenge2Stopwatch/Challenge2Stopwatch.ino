//var for num of seconds
int counter = 0;
//previous state of button
int prevState = LOW;
//is stopwatch paused or counting
bool counting = false;
//button GPIO pin
const int BUTTON_PIN = 14;
//initial times
unsigned long before_print_time = millis();
unsigned long before_count_time = millis();

void setup() {
  pinMode(BUTTON_PIN, INPUT); //set up button
  Serial.begin(9600); //begin serial stream
  pinMode(LED_BUILTIN, OUTPUT); //use built in LED to verify button presses
}

void loop() {
  //current time in loop
  unsigned long now_time = millis();
  //if button pushed, toggle counting on
  if(prevState = HIGH && digitalRead(BUTTON_PIN) == LOW)
  {
    counting = !counting; // use button to toggle counting
  }
  if(now_time-before_print_time >= 100)
  {
    // Print counter time and verify counting state
    Serial.print("Current count is: ");
    Serial.print(counter);
    Serial.println(" seconds");
    Serial.print("Currently ");
    Serial.println(counting); // 1 = counting, 0 = not countings
    before_print_time = now_time; // update old time
  }
  if(counting) // if stopwatch is running
  {
    if(now_time-before_count_time >= 1000) //if a second has passed
    {
      counter++; // increment the counter
      before_count_time = now_time; // update the old time
    }
  }
  
  //activate built in LED for troubleshooting (from tutorial 2)
  // if the button is pushed down, turn on the LED
     if (digitalRead(BUTTON_PIN) == LOW) {
          digitalWrite(LED_BUILTIN, HIGH);     
     }
     // if the button isn't pushed down, turn the LED off
     else {
          digitalWrite(LED_BUILTIN, LOW); // turn the LED off
     }

  //record previous state of button
  prevState = digitalRead(BUTTON_PIN);
}
