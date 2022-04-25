// previous sample values, used for detectTaps
int old_ax = 0; 
int old_ay = 0;
int old_az = 0;

int deadband = 40;

// tap detection timing
int timeDelay = 200;
int lastTime = currentTime;

int detectTaps(){
  // variable to be returned
  int tapVal = 0;
  //if all accelerations experience a large delta, then it has been tapped
  //time delay prevents counting the up and down from one tap as two different taps
  if (abs(ax-old_ax) > deadband && abs(ay-old_ay) > deadband && abs(az-old_az) > deadband && currentTime > lastTime + timeDelay)
  {
    tapVal = 1;
    lastTime = currentTime;
    watchState = 1;
    oldTapTime = currentTime;
  }
  //record old accel values
  old_ax = ax;
  old_ay = ay;
  old_az = az;

  // return 1 if tapped, 0 if not
  return tapVal; 
}
