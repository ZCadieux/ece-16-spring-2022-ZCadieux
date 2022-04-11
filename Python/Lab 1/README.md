[//]: <> (Titles)

# README Lab 1

[//]: <> (Name and ID)

## Name and ID

Zachary Cadieux A15912942

[//]: <> (Lab 1 Content)

## Tutorial 1

The first tutorial led me through setting up Python, which for me went quickly because I have used Python on my computer before. I am using VSCode, which lets me program in a familiar environment that has simple Github integration.

## Tutorial 2
This tutorial primarily consisted of copying and running example code. I used this as a quick reference throughout Tutorial 3 and the Challenges, to remind me of important Python syntax that I was a bit rusty with. The tutorial goes over running code, data types, lists, strings, loops, and functions.

## Tutorial 3
This tutorial served as a walkthrough and practice with Numpy, which I have some prior experience with. However, as with tutorial 2, it provides helpful quick reference for syntax, as well as a refresher on some of the specific abilities of Numpy. The questions at the bottom are simple practice problems, showing the capabilities of Numpy. My implementation solved each question as its own function, and also prints out answers to the written questions when run. 

## Challenge 1
The first challenge is a worksheet, implementing code to solve various exercises to practice the content covered in tutorial 2. Numpy was not necessary, as all problems could be solved with basic Python capabilities. I wrote my code in a similar format to my solution for Tutorial 3, writing the solution to each problem as a function that could be called independently and then calling each function at the end. This makes it very clear what code belongs to which problem, along with comments that specify the question number. 

## Challenge 2
Challenge 2 asked to build a stock simulator, to determine stock strategy based on recent historical data on stock prices. My implementation uses a single for loop, iterating over each day of stock data that is given, and applying a number of if statements to check how the average of the past 3 days compares to the price on the current day. This generates a strategy array, while dynamically tracking profits. I also implemented if statements to check that we would have enough money to buy more shares, or shares to sell, which was not a case in this example but could be if the context of the code changed (i.e. starting with less money or less shares). 

Below is a screenshot of the code output:
![Challenge 2 Output](./images/challenge2.jpg?raw=true "Challenge 2 Output")

## Challenge 3
This challenge has two primary functions, but I also wrote four functions of my own to support my code, making the primary translation functions neater. I started with english_to_pig_latin, and had a relatively easy time with the primary 3 cases, leaving hyphenated words for later. Moving on to pig_latin_to_english, I started with the "first letter vowel" case, since that was a very simple scenario to convert back from. Then I attempted to implement something specifically for the starting with a y case, but upon starting the general consonant case I realized that the generalized version I created would also work for the starting with y case, so I deleted the specific portion. Then I created my code to remove punctuation and re-add it, since punctuation was leading to errors in translating back to english. Finally, I did the hyphenated words last, using recursion to break up the words and independently translate each one before putting them back together.

Below is a screenshot of all 25 test cases:
![Challenge 3 Output](./images/challenge3.png?raw=true "Challenge 3 Output")