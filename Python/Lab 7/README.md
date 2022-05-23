[//]: <> (Titles)

# README Lab 7

[//]: <> (Name and ID)

## Name and ID

Zachary Cadieux A15912942

[//]: <> (Lab Content)

## Tutorial 1 - ML Data Preparation

This tutorial goes over using the files with the heartbeat data from the other people in the class, and verifying that all the files are filled with usable data as well as getting familiar with the glob utility. This took some time to go through each, but I was able to match my results to what other people in the Slack were noting about issues with people's files.

## Tutorial 2 - GMM HR Monitor

This tutorial goes over the does and don'ts with using the GMM, and sets up the initial code for using it to estimate heart rate using leave one subject out validation to validate the results. This goes with the idea of making sure not to validate on the same data that was used to train it.

## Challenge 1 - GMM Performance

For this challenge we used the LOSOV method from Tutorial 2 to estimate the heart rates from the given data for every file in the class drive, as well as computing statistics to verify the accuracy of the data. Below is the graph of the data, as well as the values of the root mean square error, correlation, and bias.

![Challenge 1](images/challenge1.png)

RMSE is valuable because it gives a standard metric for error that accounts purely for deviation from the true value, rather than possibly being offset by directional error, and by taking the square root it provides it on a scale that is directly applicable to the actual values, telling us that in this case our standard error is about 4 off from the ground truth. Correlation is also an important factor because it gives an idea of how well our predictions and the real values have matching trends, and bias tells us if we're significantly offset either above or below the true values. I chose these to help me eliminate bad values and pick out which data points I needed to check, since I could see how including or excluding certain data could effect the correlation, and bias helped ensure we weren't systematically over or under estimating the real values.

## Challenge 2 - GMM HR Monitor

For this challenge, I implemented the train and predict methods in the HRMonitor class mostly by using tutorial 2 as a model for how it should run. I took the main part of tutorial_gmm_losov.py and broke it up into the section involved with training and the part that is used to actually run the model. I also reproduced some of the other functions in that tutorial file within the HRMonitor class as helper functions, to make sure I was able to get all the functionality while keeping it clean and readable. The code in the actual challenge file essentially follows the same format as the online HRM from Lab 6, just with a call to the training function at the beginning. Preserving non ML usage was a bit tricky, but it just involved carefully reusing the process function that already existed. 

[![Lab 7 Challenge 2](https://youtu.be/-rf_7ZuZu1k/0.jpg)](https://youtu.be/-rf_7ZuZu1k "Lab 7 Challenge 2")

## Challenge 3 - Complete Wearable

This challenge involved incorporating parts from all of the previous labs. The Pedometer and Heart Monitor classes were easy to incorporate, as they were already built for the same kind of standardized usage loop. However, the IdleDetector and Weather modules required a bit more work to incorporate, as each of these were built in such a way as to work well independently, but not as parts of a larger program. With some minor refactoring to make them rely heavier on OOP and taking data inputs through add functions rather than directly having their own communicator objects, I was able to incorporate all the pieces together, including the motor to indicate inactivity, and the button to reset the step counter. Note that in the video, my step count is less accurate than in Lab 5, as a result of a slightly different environment and not taking the time to recalibrate the thresholds or algorithm. Eventually, this could be done with a GMM similar to the Heart Monitor!

[![Lab 7 Challenge 3](https://youtube.com/shorts/wB4Yxw8FJo4?feature=share/0.jpg)](https://youtube.com/shorts/wB4Yxw8FJo4?feature=share "Lab 7 Challenge 3")
