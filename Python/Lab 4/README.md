[//]: <> (Titles)

# README Lab 3

[//]: <> (Name and ID)

## Name and ID

Zachary Cadieux A15912942

[//]: <> (Lab 1 Content)

## Tutorial 1 - Object-Oriented Python

### Part 1 - Puppy Talk (Dog Class)

#### Questions

> 1) The print(scout) statement gives the memory location of the Dog object within working memory, which is used to reference the object.
> 2) The code returns: AttributeError: 'Dog' object has no attribute '__breed', indicating that the variable is unable to be accessed directly, as we'd expect from the double underscore in front. This means that it must be accessed via helper functions, which is good for OOP because we can limit the cases in which specific variables are used or changed.
> 3) See code for solution

## Tutorial 2 - Analog Input (Accelerometer)

Here we learned how to interface the accelerometer with the Arduino, and set up another file called Accelerometer that we could use later in the lab. Overall this was straightforward, but I encountered some issues with wires being loose and giving messy data, which took some trial and error to resolve, with the solution just being to make sure all my connections were nice and solid.

## Tutorial 3 - Analog Output (PWM)

As with most of the tutorials in this lab, the final outcome was setting up a file we could use in the challenges, specifically the "Motor" file. In this tutorial, I realized that the PWM values on my motor were swapped, such that 0 was a full power PWM signal, and 255 was off, so I adjusted the provided code accordingly.

## Tutorial 4 - Sampling

In another one of my classes we are doing labs that extensively explore sampling methods, rates, and the artifacts that come from taking bad samples, so I felt I had more than sufficient background to understand what was happening in the provided code, and be able to use the "Sampling" file that we created effectively later on in the lab. Also, seeing the sampled graph data and adjusting the sampling rate was an interesting exercise, to see the differences in the accelerometer data.

## Tutorial 5 - Python Serial & BT Communication

Working across Python and Arduino via Bluetooth brings access to a lot of computing power, and gives me a number of ideas for future projects, such as Bluetooth controlled robots and other similar applications. The tutorial_pyserial.py file contains lots of useful example code of the basics of reading from and writing to the Arduino, and works elegantly over Serial and Bluetooth, with only small edits in the Arduino codebase.

## Challenge 1

The concept for this challenge was to measure the values on the accelerometer, and then increment a counter based on physically tapping the accelerometer. This uses simple logic, with the most complex part being the algorithm used to detect taps. I used a deadband, where if the accelerometer had a change in value, either up or down, of over a certain amount, then it registered as a tap. I also put a small non-blocking delay, to ensure it didn't count one tap twice (once on the up spike and once on the down, for example).

For this challenge, I encountered a few different issues with the accelerometer that made it take a bit longer than I expected. First, I encountered the issue mentioned in Tutorial 2, with my loose connections causing meaningless data. This was fixed by adjusting some of the connections, and verifying that each individual channel was reading properly. Second, I found that between instances of testing, either when I rebuilt the circuit or sometimes even just on a fresh download, the accelerometer sensitivity would change slightly, so my deadband would need to be adjusted each time, which is why in the gif below some of my taps don't register completely. With more time to tune the algorithm, I could make something more robust but for the purposes of this lab, it functions.

![Challenge 1](images/lab3challenge1.gif)

## Challenge 2

This challenge built on challenge 1, using the tap detection algorithm in conjuction with algorithms borrowed from the timer and stopwatch challenges from lab 2. Before writing code, I drew out my state machine, modelling the states as shown below. I used these states to keep my code organized, and make sure I didn't miss things when working with the increased complexity of this challenge.
![Challenge 2](images/statemachine.jpeg)

While actually implementing the code, I wrote it one state at a time, testing each state, and then testing the conditions to swap between states as I wrote them, to make troubleshooting easier, rather than writing a large codebase and then testing it all at once. This made it easier to isolate issues, and to keep my code clean. Note that as mentioned in Challenge 1, the tap detection is not perfect, because of variance in the deadband. Recording the functioning system took a few tries, since I needed one hand to push the button and tap the accelerometer, and another to hold the motor so that the wires would stay plugged in, because with how thin they are and how strong the motor vibrates, they were coming loose very easily. 
![Challenge 2](images/lab3challenge2.gif)

## Challenge 3

This lab required only minor edits applied to the code written in Tutorial 5. The Arduino code stayed essentially exactly the same, but the Python code changed to include the date, time, and weather information, as well as update more cleanly in a while loop, so that the screen would not fully refresh every second. I was familiar with the datetime library and class, and using the docs for that library I was able to easily generate a formatted date and time, and getting the weather information simply took using the provided code and then correctly indexing the generated dictionary. 

To determine how often Python should send data to the Arduino, I compared the value of the time variable on every iteration of the loop to the value previously, and if it had changed then it updated. This resulted in it being updated exactly as the second changed, since with time blocking and other similar ideas in python, it was possible to update between seconds, sometimes looking like time was not passing, or jumping two seconds at a time.

![Challenge 3](images/lab3challenge3.gif)
