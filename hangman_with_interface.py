import random
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#Initial variables
words = ["PYTHON","BANANA","ELEPHANT","SUNSHINE","RAINBOW","SHARK","OCEAN","COOKIE"]
guessed_letters = []
used_words = []

#START Function session
def get_rand_index(list): #Function to select a random index from a list
    while True:
        i = list[random.randint(0,(len(list)-1))]
        return i
    
def hide_word(word): #Function to hide the word using underscores
    global found_letters
    hidden_word = []
    for i in range(len(word)):
        if (word[i] == ' '):
            hidden_word.append(' ')
            found_letters +=1
        else:
            hidden_word.append('_')
    return hidden_word

def disable_button(buttons): #Function to disable one or more buttons
    for button in buttons:
        button.config(state='disabled')

def enable_button(buttons): #Function to enable one or more buttons
    for button in buttons:
        button.config(state='normal')

def check_letter(letter): #Function to check if the letter is in the hidden word and update the underscores if the letter is found
    global hidden_word,word,found_letters,guessed_letters,tries,found
    guess_entry.delete(0,END) #Clear guess entry
    if tries + 1 == max_tries and letter not in guessed_letters: #Check if the attempt will reach the maximum number of attempts and if the letter has not been guessed yet.
        disable_button([guess_button,hints_button])
    match letter:
        case letter if letter in guessed_letters: #Check if the letter is in the list of previously spoken words.
            alert_label.config(foreground='red')
            if len(letter)>1:
                alert_text.set('Word already guessed.')
            else:
                alert_text.set('Letter already guessed.')
        case letter if letter == word: #Check if the spoken 'letter' is the word to be guessed.
            tries = tries+1
            hidden_text.set(word)
            disable_button([guess_button,hints_button])
            alert_label.config(foreground='green')
            alert_text.set('Word found! Take another.')
        case letter if len(letter) > 1: #If the letter has more than one character, then it is a word that, as a result of the previous case, is incorrect.
            guessed_letters.append(letter)
            tries = tries+1
            alert_label.config(foreground='red')
            alert_text.set('That is not the word.')
        case letter if letter == '': #If the person doesn't input anything.
            guessed_letters.append(letter)
            alert_label.config(foreground='red')
            alert_text.set('That letter is incorrect.')
            tries = tries+1
        case letter if letter in word: #Check if the letter is in the word and update the hidden_word.
            for i in range(len(word)):
                if (letter == word[i]):
                    hidden_word[i] = letter
                    found_letters +=1
            tries = tries+1
            hidden_text.set(' '.join(hidden_word)) #Updating the displayed hidden_text.
            guessed_letters.append(letter)
            alert_label.config(foreground='green')
            alert_text.set('That letter is correct!')
        case _: #If it is anything else, it is incorrect.
            tries = tries+1
            guessed_letters.append(letter)
            alert_label.config(foreground='red')
            alert_text.set('That letter is incorrect.')
    tries_text.set("Remaing tries: " + str(max_tries-tries))
    if (found_letters == len(word)): #If the number of letters found is the same as the size of the word, then the word has been found.
        alert_label.config(foreground='green')
        alert_text.set('Word found! Take another.')
        disable_button([guess_button,hints_button])
    else:
        pass

def hint_word(word): #Function to get a random letter from the word and reveal it
    global guessed_letters,hints,found
    guess_entry.delete(0,END)
    if hints >= 1:
        while True:
            rand_letter = get_rand_index(word)
            if rand_letter in guessed_letters:
                continue
            else:
                check_letter(rand_letter)
                guessed_letters.append(rand_letter)
                hints = hints-1
                hint_text.set("Hints: "+ str(hints))
                if hints < 1: #If the last hint is used, disable the button.
                    disable_button([hints_button])
                break

def new_word(): #Function that chooses a word and resets the variables.
    global hints,found_letters,tries,max_tries,hidden_word,word,found
    while True:
        if (len(words) == len(used_words)): #Check if all the words have been used.
            alert_label.config(foreground='red')
            alert_text.set("There is no more words")
            disable_button([new_word_button])
            break
        word = get_rand_index(words)
        if word in used_words: #If the word is repeated
            continue
        else: #When the game starts some variable are set, reset and incremented
            hints = 1
            found_letters = 0
            tries = 0
            max_tries = len(word)+2
            guessed_letters.clear()
            guessed_letters.append('-')
            hidden_word = hide_word(word)
            used_words.append(word)
            hidden_text.set(' '.join(hidden_word))
            alert_text.set('')
            hint_text.set("Hints: "+ str(hints))
            tries_text.set("Remaing tries: " + str(max_tries-tries))
            guess_entry.delete(0,END)
            enable_button([guess_button,hints_button]) #Reactivate the buttons.
            break
#END Function session

#START Tkinter session
main_window = Tk()
main_window.title("Hangman Game")
paddings = {'padx': 5, 'pady': 5}
font = ('Arial', 8)

#Text variables
hidden_text = StringVar()
alert_text = StringVar()
hint_text = StringVar()
tries_text = StringVar()

#START Widgets
new_word_button = ttk.Button(main_window,text="New Word", command= new_word)
new_word_button.grid(row=1,column=2, **paddings)

guess_entry = ttk.Entry(main_window)
guess_entry.grid(row=1,column=0, **paddings)

guess_button = ttk.Button(main_window,text="Guess",command= lambda: check_letter(guess_entry.get().upper()))
guess_button.grid(row=1,column=1, **paddings)
def enter_pressed(event): #Function to press the guess button when the enter key is pressed.
    guess_button.invoke()
main_window.bind('<Return>', enter_pressed)

hints_button = ttk.Button(main_window,text="Take a Hint!", command= lambda: hint_word(word))
hints_button.grid(row=2,column=1, **paddings)

hidden_label = ttk.Label(main_window,font=(font),textvariable=hidden_text)
hidden_label.grid(row=0,column=0, **paddings)

tries_label = ttk.Label(main_window,textvariable=tries_text)
tries_label.grid(row=0,column=1,columnspan=2, **paddings)

hints_label = ttk.Label(main_window,textvariable=hint_text)
hints_label.grid(row=2,column=2, **paddings)

alert_label = ttk.Label(main_window,font=(font),textvariable=alert_text)
alert_label.grid(row=2,column=0, **paddings)
#END Widgets

new_word()

main_window.mainloop()
#END Tkinter session