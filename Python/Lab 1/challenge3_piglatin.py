import enchant as e

vowels = ['a', 'e', 'i', 'o', 'u', 'y'] # create list of vowels, used in many places
def english_to_pig_latin(inputWord):
    outputWord = '' # initialize output
    if inputWord[0] == 'y': # if first letter is 'y'
        vowelIndex = first_vowel(inputWord[1:len(inputWord)]) # find first vowel
        if type(vowelIndex) == type(1): # if there is a vowel
            outputWord = inputWord[vowelIndex:len(inputWord)] + inputWord[0:vowelIndex] + 'ey' # move letters before first vowel to end, add 'ey'
    elif inputWord[0] in vowels: # if the first letter is a vowel
        outputWord = inputWord + 'yay' # append 'yay'
    else: # if first letter is a consonant (not y)
        vowelIndex = first_vowel(inputWord) # find first vowel
        if type(vowelIndex) == type(1): # if there is a vowel
            #print('vowelIndex', vowelIndex)
            #print('vowel', inputWord[vowelIndex])
            #print('letter before', inputWord[vowelIndex-1])
            if inputWord[vowelIndex] == 'u' and (inputWord[vowelIndex-1] == 'q' or inputWord[vowelIndex-1] == 'Q'):
                outputWord = inputWord[vowelIndex+1:len(inputWord)] + inputWord[0:vowelIndex+1] + 'ay' # move letters before first vowel to end, add 'ey'
            else:
                outputWord = inputWord[vowelIndex:len(inputWord)] + inputWord[0:vowelIndex] + 'ay'

    return outputWord

def pig_latin_to_english(inputWord):

    return ''

def first_vowel(word):
    for index, char in enumerate(word):
        #print(index)
        #print(char)
        if char in vowels:
            return index
    return 'No vowels found'


test_list = ['Quotient','Mustn\'t','Yellow', 'Honest', 'Thursday', 'Christmas', 
             'Alliteration', 'Information', 'Education', 'Fish', 'Numbers!', 
             'Toyota!', 'Mother-in-law', 'Laps', 'Slap', 'August', 'empty-handed',
             'Ice-cream', 'Years', 'Yankee', 'Yawn', 'Young', 'Yard', 'Quiet', 'Quack']

for i, word in enumerate(test_list):
    out1 = english_to_pig_latin(word)  
    out2 = pig_latin_to_english(out1)
    print(i+1, 'inputted word:', word)
    print(i+1, 'english -> p-latin:', out1)
    print(i+1, 'p-latin -> english:', out2)
