# ECE 16 Grand Challenge - Space Invaders Controller
A socket-based controller for Space Invaders to controller the game wirelessly with the ESP32.

The game is a modified version of Space Invaders based off of this project: https://github.com/leerob/Space_Invaders

You must have Pygame installed before being able to run the game: https://www.pygame.org/

## Instructions

To use the Space Invaders controller first all the files need to be downloaded and the Arduino script needs to be uploaded to the microcontroller. Reset the microcontroller. Open up two terminal windows. In the first window navigate to the `SpaceInvaders` folder that holds `spaceinvaders.py`. In the second window navigate to the `controller/Python` folder that holds `space_invaders_controller.py`. Run `spaceinvaders.py` using python3. Once the game opens up (in the second terminal window) run `space_invaders_controller.py` using python3. Hold the controller level and press Enter when prompted. Bring the game window back to the front and press any button to start. Tilt the controller along the axis orthongonal to the computer screen to move left/right. To shoot press the button on the right. To change speed press the button on the left. This can be done while playing! Attempt to shoot all the aliens before they sucessfully invade or you use all your lives.

## Improvements

* The first improvement we made was decoupling the movement from the shooting. We did this by sending a single two digit command to communicate the necessary information. The accelerometer script sent a 0 (flat), 3 (left), or 4 (right) depending on what direction was receiving the particular change in acceleration. The button script sent a 0 or a 10 for whether the button was pressed. These orientation and shoot values were added then sent to the python controller script. Here, the move command was taken from the message using modulus 10. Then the shoot command was determined by subtracting `move` from `message`. So from this single message we can determine the orientation, shoot status, and speed (described later).

* The second improvement was being able to shoot using the button. This included adding the button script in Arduino then setting the button press to 10, no button press to 0. After this command is sent to Python (described above), the controller script tells the game to shoot through the socket.

* We spent a fair amount of time determining the zeros for the accelerometer, so we implemented a time when the game first starts up for the accelerometer to calibrate. It samples 10 times, then takes the average of these values. Since the sampling is so quick it is not noticable to the user. This allows the game to work on any accelerometer, not just the one it was programmed with.

* We implemented smoother control in a few ways: only considering acceleration in the x direction, including a “dead zone” where the controller is considered flat, and changing when and how fast data is communicated. On the Arduino side, we sampled data from all directions but only used ax. As mentioned before, we calculated the zeros from the first 10 samples. If the current value was within 50 of ax’s zero, the controller was considered flat. More than that was a turn left or right. Data was only send to Python if the message was different. The message consists of a change speed value, a shoot value, and an orientation value. Any time any of these changes a new message gets sent. A possible furthering of the project could be to establish a second delta acceleration threshold and change the ship speed. Once the message is communicated to Python, it sends the same message to the game script until a new one is received. It sends every 0.05 seconds to allow the game to process data coming in.

## Features

* When the ship gets hit, the motor buzzes. Before implementing this feature, the game socket was only receiving data. To implement the buzz the game had to also send data. We created a new definition that gets called when the ship is hit. It sends the `“buzz”` command to the controller Python script, which then sends it to the Arduino.

* There is a second button on the board that changes the ship speed. When it is pressed the speed increases, then after max speed goes to min speed. The change is done by sending different speed multipliers, either 1, 2, or 3, through the game socket.

* The speed (1 (slow), 2 (medium), 3 (fast)) is displayed on the OLED. When a multiplier is selected, it changes the variable `speed` that displays on the OLED.

Here is a video displaying controller functions.

[![Elevator Explanation and Demo](https://img.youtube.com/vi/dP79kfdSzHg/0.jpg)](https://youtu.be/dP79kfdSzHg)


# ECE 16 Grand Challenge - Contactless Elevator Controller

An OpenCV based controller for Space Invaders to control an elevator with a combination of the ESP32 and a camera.

The use case for this project is to input a desired floor to go to in an elevator without making physical contact with any parts of the controller.

This is an imporant issue to address because elevators are a very high traffic contact area, and one that is in an enclosed space that is a perfect place for bacteria to reside. This design allows us to avoid touching the surface, and minimize contact with potentially dangerous germs.

The intended users are anyone using an elevator, including people who may not be able to reach or press normal elevator buttons for whatever reason such as physical disabilities. Additionally anyone who wants to minimize their exposure to potentially hazardous contact surfaces.

Our solution addresses these issues by allowing a user to activate an elevator and choose a floor to go to without touching any surface, in a way that is very repeatable and scalable.

Here is an explanation of our system, as explained in text below, as well as a demonstration of it functioning.

[![Elevator Explanation and Demo](https://img.youtube.com/vi/6f-8La9IHtE/0.jpg)](https://youtu.be/6f-8La9IHtE)

## Dependencies

This controller uses the CVZone library https://github.com/cvzone/cvzone to recognize hands from a raw camera input. It does so using a combination of OpenCV and Mediapipe, an ML library built for image recognition.
> OpenCV-Python: https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html \
> CVZone: https://github.com/cvzone/cvzone \
> Mediapipe: https://github.com/google/mediapipe \
> NOTE: Mediapipe currently has import errors with  protobuf, make sure version 3.20.1 is installed (may require a downgrade) \
> ECE16Lib (HandTracker.py is contained here)

## Elevator Controller

The elevator control uses a combination of PPG and camera inputs to allow for completely contactless user inputs. While we did not build an elevator for it to move up and down, the controller represents the current floor on the LCD, and uses a timer to represent moving at a rate of 1 floor per second.

### Usage

After installing all necessary files, run elevator.py. This will initialize all necessary objects, including the HandTracker, which uses CVZone, and the serial communication over Bluetooth with the ESP32 board. Initially, the board will be in a resting state. Note that all states are indicated by a certain LED, as well as printed on the LCD.

#### LED Code

> green - arrived or idle\
> yellow - waiting for floor input \
> red - floor selection cancelled \
> blue - moving

Waving a hand over the PPG sensor will change the system into the “Waiting for Input” state, where it will wait until the same number of fingers have been held up for about a second. This gives the user time to choose their floor, and accounts for movement or time to ensure the right number of fingers are in frame. Waving a hand over the PPG sensor again while it is in this state will cancel the command, putting it back in an Idle state.

Once a floor number has been input, the ESP32 simulates elevator movement by moving one floor per second until the current floor matches the target floor. When the user has arrived, it is indicated by the green LED, at which point it can take in a new input (after waving at the PPG again).

### Potential Improvements

Currently, this controller can only take in inputs from floors 1-10, since it reads the number of fingers being held up from a maximum of two hands. This can be changed by changing the recognition algorithm to intake numbers in sign language rather than by the number of fingers being held up, since sign language allows all numbers to be expressed by one hand.

Additionally, currently there is no actual elevator mechanism attached to the system. Getting a motor and attaching it with a PWM signal in place of the timer countdown would be the next major step in moving this prototype into a true implementation.

# Division of work

### Controller

Zach thought of the single message and dividing with mod then started the implementation. He also came up with ideas on how to implement several of the improvements and features. Gillian did the implementation and worked out all the bugs. She also decided on which improvements/features to include and put together the majority of the code for them.

### Project

Zach and Gillian worked together for the idea and use case. Zach found and implemented the library that ended up being used and designed/implemented the hardware and software.

### Overall

The overall split was Gillian worked on the controller and Zach worked on the elevator project.