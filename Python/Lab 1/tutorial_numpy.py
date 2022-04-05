import numpy as np #import numpy

# Solving question 1
def question1():
    array1 = np.array([0,10,4,12]) # Create array
    array1 = array1 - 20 # Perform operation
    return [array1, array1.shape] # Return answer

print('Question 1:')
q1 = question1() # Evaluate
print('Result is', q1[0], 'shape is', q1[1]) # print result

# Solving question 2
def question2():
    array2 = np.array([[0,10,4,12], [1,20,3,41]]) # Create array
    array2_new = np.resize(array2, (4,2)) # Restructure to isolate into 2 number segments
    array2_new = np.array([array2_new[1], array2_new[2]]) # Select relevant segments
    return(array2_new) # Return answer

print('Question 2:')
q2 = question2() # Evaluate
print(q2, 'is obtained by restructuring into a 4x2 and selecting elements 1 and 2 of the resulting numpy array.')

# Solving question 3
def question3():
    array1 = np.array([0,10,4,12]) # Create array
    array3 = np.hstack((array1, array1)) # Horizontal stack
    array3 = np.vstack((array3, array3, array3, array3)) # Vertical stack
    return array3 # Return answer

print('Question 3:')
print(question3())

# Solving question 4
def question4():
    array4a = np.arange(-3, 16, 6)
    array4b = np.arange(-7, -20, -2)
    return [array4a, array4b]

print('Question 4:')
print(question4())

# Solving question 5
def question5():
    array5 = np.linspace(0,100, 49)
    return array5

print('Question 5:')
print(question5())
print('This is different because it specifies a number of steps rather than the step size,\
so if you need something evenly distributed over a range you would use linspace, but if you knew the intervals you wanted then you would use arange.')

# Solving question 6
def question6():
    array6 = np.zeros((3, 4))
    # Assign values row by row
    array6[0] = [12, 3, 1 ,2]
    array6[1] = [0, 0, 1, 2]
    array6[2] = [4, 2, 3, 1]
    # Test print statements
    print(array6[0])     # [12 3 1 2]
    print(array6[1, 0])  # 0    
    print(array6[:, 1])  # [3 0 2]
    print(array6[2, :2]) # [4 2]
    print(array6[2, 2:]) # [3 1] 
    print(array6[:, 2])  # [1 1 3]
    print(array6[1, 3])  # 2
    return array6

print('Question 6:')
print(question6())

# Solving question 7
def question7():
    string7 = "1,2,3,4" # Define initial string
    array7 = np.array(string7) # Define first line of array
    for i in range(99): # Loop x99 since we already have the first row
        array7 = np.vstack((array7, string7)) # Add a new row in every loop
    #print(array7.size) # check size
    return array7 # return answer

print('Question 7:')
print(question7())

