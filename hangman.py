import random
from tkinter import *
from tkinter import messagebox
#START Functioin section
def randindex(list): #Function to select a random index from a list
    while True:
        index = list[random.randint(0,(len(list)-1))]
        return index
    
def hideword(word): #Function to hide the word using underscores
    global foundletters
    hiddenword = []
    for i in range(len(word)):
        if (word[i] == ' '):
            hiddenword.append(' ')
            foundletters +=1
        else:
            hiddenword.append('_')
    return hiddenword

def printword(word): #Function to print the word with a space between each character
    print('')
    for i in range(len(word)):
            print(word[i],end=' ')
    print('')

def checkletter(letter): #Function to check if the letter is in the hidden word and update the underscores if the letter is found
    global hiddenword,word,foundletters
    if (len(letter) > 1):
        print('That is not the word!')
    elif letter in word:
        for i in range(len(word)):
            if (letter == word[i]):
                hiddenword[i] = letter
                foundletters +=1
        print('That letter is correct!')
    else:
        print('That letter is incorrect!')
    
def hintword(word): #Function to get a random letter from the word and reveal it
    global letters
    while True:
        randletter = randindex(word)
        if randletter in letters:
            continue
        else:
            checkletter(randletter)
            letters.append(randletter)
            break
#END Function section

#START Variable declaration
#If you want to use compound words, write "PYTHON PY" instead of "PYTHON-PY".
words = ["PYTHON","BANANA","ELEPHANT","SUNSHINE","RAINBOW","SHARK","OCEAN","COOKIE"]
letters = []
usedwords = []
tries = 0
#END Variable declaration

#START Main code
print("HANGMAN GAME - We will select a word for you.")
while True: #Main loop
    if (len(words) == len(usedwords)):
        print("We don't have any more word for you to find :(")
        break
    word = randindex(words)
    if word in usedwords: #If the word is repeated
        continue
    else: #When the game starts some variable are set, reset and incremented
        hints = 1
        foundletters = 0
        tries = 0
        maxtries = len(word)+4
        letters.clear()
        letters.append(' ')
        hiddenword = hideword(word)
        usedwords.append(word)
    while True: #Loop with the game logic
        printword(hiddenword)
        letter = input("Try to guess the word. {} Attemps remaining.\nFor a hint type: ! (Remaining hints: {}) >>".format(maxtries-tries,hints)).upper()
        match letter: #Match case with the player input letter
            case '!' if hints > 0: #Hint option if there are hints available
                hints -= 1
                hintword(word)
            case '!': #Hint option if there are no hints available
                print("You don't have any more hints.")
                continue
            case letter if letter in letters: #Check if the letter has already been entered
                print("You already guessed that letter.")
                continue
            case letter if letter == word: #Check if the player entered the word
                tries += 1
                printword(word)
                print("Congratulations! You found the word in {} of {} attemps!".format(tries, maxtries))
                break
            case _: #If a letter that hasn't been guessed yet is entered, check the letter and add it to the list of guessed letters
                letters.append(letter)
                checkletter(letter)
                tries += 1 
        if(foundletters == len(word)): #If the number of found letters equals the number of letter in the word, then you found the word
            printword(word)
            print("Congratulations! You found the word in {} of {} attemps!".format(tries, maxtries))
            break
        if(tries == maxtries): #If the number of tries reaches the maximum, you lose
            print("\nYour attemps are over:(\nThe word was: {}".format(word))
            break
    while True: #Loop to ask if you wnat to play again or not
        op = input("\nDo you want to play again?(Y/N)\n>>").upper()
        match op:
            case 'Y':
                print("Finding another word...")
                break
            case 'N':
                print("Thank you for playing :)")
                exit()
            case _:
                print("Enter a valid option!")
                continue
#END Main code