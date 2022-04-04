#Part 1: Running Python Code
print("Hello, ECE 16 World!")

#Part 3: Python Lists
# Creating Lists
animals = ["dog", "squirrel", "monkey", "cat"] # list of strings
numbers = [10, 114, 567, 8, 9] # list of integers
float_numbers = [4.6, 7.889, 1.005, 2.0, 5.1] # list of floats
empty_list = [] # empty list
mixed_list = ["this is a string", 451, 12.79, "a"] # differing data types

# Accessing List Elements
print(numbers[0]) # prints 10
print(mixed_list[0]) # prints “this is a string”
print(len(numbers)) # prints 5
print(numbers[4]) # prints 9
print(numbers[len(numbers) - 2]) # prints 8
numbers[3] = 100
print(numbers) # prints [10, 114, 567, 100, 9]

# Modifying Lists
numbers.append(60)
print(numbers) # prints [10, 114, 567, 100, 9, 60]
del(numbers[4])
print(numbers) # prints [10, 114, 567, 100, 60]

# Slicing
numbers = [10,20,30,40,50,60,70]
print(numbers) # prints [10,20,30,40,50,60,70]

print(numbers[0:3]) # prints [10,20,30]: slice from 0 to 3 (exclusive)
print(numbers[:3]) # prints [10,20,30]: slice from 0 to 3 (exclusive)

print(numbers[4:7]) # prints [50,60,70]: slice from 4 to 7 (exclusive)
print(numbers[4:100]) # prints [50,60,70]: slice from 4 to end of the list
print(numbers[4:]) # prints [50,60,70]: slice from 4 to the end of the list

print(numbers[:]) # prints [10,20,30,40,50,60,70]: slice of the whole list

numbers[1:4] = [200,300,400]
print(numbers) # prints [10,200,300,400,50,60,70]: modified 3 elements!

# List Comprehensions
nums = [1,2,3,4,5]
nums_double = [x*2 for x in nums] # multiply element by 2 and store in a new list
nums_squared = [x**2 for x in nums] # square each element and store in a new list
nums_subtract = [x-2 for x in nums if x>3] # subtract 2 from each element if its values is greater than 3 and store in a new list

print(nums_double) # prints [2,4,6,8,10]
print(nums_squared) # prints [1,4,9,16,25]
print(nums_subtract) #prints [2,3]; Notice only 2 elements!!!

# Part 4: Python Strings
"""
Adding 2 strings
"""
string_1 = "hello"
string_1 = string_1 + " world" 
print(string_1) # prints "hello world"

"""
Accessing characters
"""
string_1 = "It is a sunny day"
print(string_1[0]) # prints "I"
print(string_1[2]) # prints " "

print(string_1[-1]) # prints "y"
print(string_1[-2]) # prints "a"

"""
Length of a string
"""
string_1 = "Good Morning" # string_1 contains 12 characters
print( len(string_1) ) # prints 12 

"""
Slicing a string
"""
string_1 = "Good Morning"
print( string_1[0:4] ) # prints ‘Good’
print( string_1[-7:] ) # prints ‘Morning’

"""
Splitting a string: Returns a list of strings
"""
string_1 = "Good-Morning-Have-A-Good-Day"
print( string_1.split("-") ) # ['Good','Morning','Have','A','Good','Day']

"""
Strings are immutable
"""
string_1 = "Good Morning" # Str1 contains 12 characters
#string_1[0] = "A" # The interpreter will throw an error on this line

# Part 5: Python Looping

colors = ["red", "blue", "green", "yellow", "orange"]
for color in colors:
	print(color)

# prints red, blue, green, yellow, orange; each in its own line

colors = ["red", "blue", "green", "yellow", "orange"]
for ind, color in enumerate(colors):
	print(ind, color)

# prints 0 red, 1 blue, 2 green, 3 yellow, 4 orange; each in its own line

# Part 6: Python Functions
def add_nums(a, b):
	return a+b

if __name__== "__main__":
	sum1 = add_nums(2, 3)
	sum2 = add_nums(10, 20)

	print(sum1) # prints 5
	print(sum2) # prints 30