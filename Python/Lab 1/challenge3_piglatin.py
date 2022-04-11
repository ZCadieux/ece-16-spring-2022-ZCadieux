import enchant as e
import string

dictionary = e.Dict("en_US")
vowels = ['a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y'] # create list of vowels, used in many places
def english_to_pig_latin(inputWord):
    [inputWord, punct, punctloc] = removePunct(inputWord) # remove punctuation
    case = 0 # tracks case for punctuation purposes
    outputWord = '' # initialize output
    if inputWord.find('-') != -1: # check for hyphens
        words = hyphenSlicer(inputWord) # cut out hyphens
        for word in words: # loop through and convert each word
            if outputWord == '':
                outputWord = english_to_pig_latin(word) # no hyphen for first word
            else:
                outputWord = outputWord + '-' + english_to_pig_latin(word) # add hyphen and word

    elif inputWord[0] == 'y' or inputWord[0] == 'Y': # if first letter is 'y'
        vowelIndex = first_vowel(inputWord[1:len(inputWord)]) # find first vowel
        if type(vowelIndex) == type(1): # if there is a vowel
            outputWord = inputWord[vowelIndex+1:len(inputWord)] + inputWord[0:vowelIndex+1] + 'ey' # move letters before first vowel to end, add 'ey'

    elif inputWord[0] in vowels: # if the first letter is a vowel
        outputWord = inputWord + 'yay' # append 'yay'
        case = 1 # tracks case for punctuation purposes

    else: # if first letter is a consonant (not y)
        vowelIndex = first_vowel(inputWord) # find first vowel
        if type(vowelIndex) == type(1): # if there is a vowel
            if inputWord[vowelIndex] == 'u' and (inputWord[vowelIndex-1] == 'q' or inputWord[vowelIndex-1] == 'Q'):
                outputWord = inputWord[vowelIndex+1:len(inputWord)] + inputWord[0:vowelIndex+1] + 'ay' # move letters before first vowel to end, add 'ey'
            else:
                outputWord = inputWord[vowelIndex:len(inputWord)] + inputWord[0:vowelIndex] + 'ay'

    outputWord = addPunct(outputWord, punct, punctloc, case) # add punctuation back in
    return outputWord

def pig_latin_to_english(inputWord):
    outputWord = ''
    case = 0 # tracks case for punctuation purposes
    [inputWord, punct, punctloc] = removePunct(inputWord) # remove punctuation

    if inputWord.find('-') != -1: # check for hyphens
        words = hyphenSlicer(inputWord) # cut up word
        for word in words:
            if outputWord == '':
                outputWord = pig_latin_to_english(word) # no hyphen for first word
            else:
                outputWord = outputWord + '-' +  pig_latin_to_english(word) # add hyphen and word

    elif inputWord[len(inputWord)-3:len(inputWord)] == 'yay': # first letter vowel case
        outputWord = inputWord[0:len(inputWord)-3]
        case = 1 # tracks case for punctuation purposes

    else: # first letter consonant or y
        outputWord = inputWord[0:len(inputWord)-2] # take off ending
        while dictionary.check(outputWord) == False: # move letters to the front until it is a real word
            outputWord = outputWord[len(outputWord)-1] + outputWord[0:len(outputWord)-1]
    
    outputWord = addPunct(outputWord, punct, punctloc, case) # add punctuation back in
    return outputWord

def first_vowel(word):
    for index, char in enumerate(word):
        if char in vowels:
            return index # returns location of first vowel in word
    return 'No vowels found'

def removePunct(inputWord):
    (punct, punctloc) = ([], [])
    for index, char in enumerate(inputWord):
        if char in string.punctuation and char != '-' and char != '\'': # hyphens and apostrophes must be handled differently
            punct.append(char) # save info about punctuation and its location
            punctloc.append(index)
            inputWord = inputWord[0:index]+inputWord[index+1:len(inputWord)] # remove punctuation from word
    return inputWord, punct, punctloc

def addPunct(inputWord, punct, punctloc, case = 0):
    while punct != []:
        if case == 0:
            index = punctloc.pop(0) + 2 # adjustment for pig latin endings
        elif case == 1:
            index = punctloc.pop(0) + 3 # adjustment for pig latin endings for words starting with vowels
        inputWord = inputWord[0:index] + punct.pop(0) + inputWord[index:len(inputWord)]
    return inputWord

def hyphenSlicer(inputWord):
    outputWords = []
    while inputWord.find('-') != -1: # while the word has hyphens
        index = inputWord.find('-') # locate hyphen
        outputWords.append(inputWord[0:index]) # save word, minus hyphen
        inputWord = inputWord[index+1:len(inputWord)] # subtract processed part from input
    outputWords.append(inputWord) # add part after last hyphen
    return outputWords



test_list = ['Quotient','Mustn\'t','Yellow', 'Honest', 'Thursday', 'Christmas', 
             'Alliteration', 'Information', 'Education', 'Fish', 'Numbers!', 
             'Toyota!', 'Mother-in-law', 'Laps', 'Slap', 'August', 'empty-handed',
             'Ice-cream', 'Years', 'Yankee', 'Yawn', 'Young', 'Yard', 'Quiet', 'Quack']

#print(hyphenSlicer('Mother-in-law'))

for i, word in enumerate(test_list):
    out1 = english_to_pig_latin(word)  
    out2 = pig_latin_to_english(out1)
    print(i+1, 'inputted word:', word)
    print(i+1, 'english -> p-latin:', out1)
    print(i+1, 'p-latin -> english:', out2)
