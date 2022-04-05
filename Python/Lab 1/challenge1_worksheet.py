# 0.3 Exercises
def exercise0():
    list_1 = list(range(1,11)) # ints 1-10
    list_2 = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0] # floats 11-20
    list_1[0], list_1[1], list_1[2] = 'one', 'two', 'three' # replace first 3 terms
    print('Part 3i:', list_1) # Part 3i

    tup = ('eleven', 'twelve', 'thirteen') # Make tuple
    (list_2[0], list_2[1], list_2[2]) = tup # Set list vals to tuple
    print('Part 4i:', list_2) # Part 4i

    joint_1 = list_1[:]
    joint_1.extend(list_2)
    joint_2 = list_1 + list_2
    print('Part 5iii:', 'joint_1:', joint_1, 'joint_2:', joint_2) # Part 4i

# Part 6
def list_shift(base_list, new_data):
    length = len(base_list) # find target length
    base_list.extend(new_data) # add new data to end
    while len(base_list) is not length:
        base_list.pop(0) # remove first value until at target length
    return base_list

#1.4 Exercises
def exercise1():
    commands = ["STATUS", "ADD", "COMMIT", "PUSH"] # part 1
    for command in commands:
        print(command) # part 2
    words = ["PUSH FAILED", "BANANAS", "PUSH SUCCESS", "APPLES"] # part 3
    text = "SUCCESS" # part 4
    # Part 5 Test cases
    print("SUCCESS" in "SUCCESS")
    print("SUCCESS" in "ijoisafjoijiojSUCCESS")
    print("SUCCESS" == "ijoisafjoijiojSUCCESS")
    print("SUCCESS" == text)
    print("The 'in' function compares character by character, seeing if the term is contained at all within the target string, while '==' compares the entire string.")

    # Part 6
    i = 0 # set counter
    while i < len(words):
        if text in words[i]:
            print("This worked!") # if text contained, print and exit loop
            break
        else:
            print(words[i]) # else, print word
        i=i+1 # increment counter

#2.2 Exercises
def exercise2():
    name = "zachary"
    byte_name = name.encode('utf-8') # encode name
    byte_name_bad = byte_name + b'\xef' # will cause decoding error
    try:
        print(byte_name.decode()) # should successfully decode name
    except UnicodeDecodeError:
        print('')
    try:
        print(byte_name_bad.decode()) # gives UnicodeDecodeError error
    except UnicodeDecodeError:
        print('')


# Function calls
exercise0()
fixed_length_list = [1,2,3,4]
new_data = [5,6,7]
print(list_shift(fixed_length_list, new_data))
exercise1()
exercise2()

