const int BUTTON_PIN1 = 14;
const int BUTTON_PIN2 = 32;
int prevState1 = LOW;
int buttonTime1 = millis();
int curTime1 = millis();
int prevState2 = LOW;
int buttonTime2 = millis();
int curTime2 = millis();

void setupButton()
{
  pinMode(BUTTON_PIN1, INPUT);
  pinMode(BUTTON_PIN2, INPUT);
}

int getShoot()
{
  curTime1 = millis();
   if(prevState1 == LOW && digitalRead(BUTTON_PIN1) == HIGH && curTime1-buttonTime1 >= 10)
  {
    return 10; //shoot command
    buttonTime1 = curTime1;
  }
  prevState1 = digitalRead(BUTTON_PIN1);
  return 0; //don't shoot
}

int getChange()
{
  curTime2 = millis();
   if(prevState2 == LOW && digitalRead(BUTTON_PIN2) == HIGH && curTime2-buttonTime2 >= 10)
  {
    return 100; //change speed command
    buttonTime2 = curTime2;
  }
  prevState2 = digitalRead(BUTTON_PIN2);
  return 200; //don't change speed
}
