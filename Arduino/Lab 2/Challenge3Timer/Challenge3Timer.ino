//var for num of seconds
int timer = 0;
//counting down or waiting
bool countDown = false;
//previous state of button
int prevState = LOW;
//button GPIO pin
const int BUTTON_PIN = 14;
//initial times
unsigned long before_print_time = millis();
unsigned long before_count_time = millis();
unsigned long push_time = millis();

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
    timer++; // use button to increment timer
    push_time = now_time;
    countDown = false;
    delay(150);
  }
  //record previous state of button
  delay(50);
  prevState = digitalRead(BUTTON_PIN);
  Serial.print(prevState);
  
  if(now_time-before_print_time >= 100)
  {
    // Print counter time and verify counting state
    Serial.print("Current timer is: ");
    Serial.print(timer);
    Serial.println(" seconds");
    Serial.print("Currently ");
    Serial.println(countDown); // 1 = counting, 0 = not countings
    before_print_time = now_time; // update old time
  }
  
  if(now_time-push_time >= 3000 && !countDown) //if 3 seconds have passed since button was pushed
  {
    countDown = true; // start counting down
    before_count_time = now_time; // update stored time
  }

  //if we're counting down
  if(countDown)
  {
    if(now_time-before_count_time >= 1000 && timer >0) // if a second has passed and we aren't at 0 yet
    {
      timer--; // decrease timer
      before_count_time = now_time; // update stored time
    }
  }
}
