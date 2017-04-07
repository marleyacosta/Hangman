
from tkinter import *
import tkinter.messagebox

## letter guess section ##
def letterguess(guessfield, hiddenword, game, gamelabel1, man, e):
	global correctcounter
	global incorrectcounter
	global wordarray
	global guessedletters
	global word




	i = 0
	letterinword = False
	valid = True
	letter = guessfield.get()
	letter = letter.lower()
	guessfield.delete(0, END)

	## account for blank input ##
	if (len(letter) == 0):
		tkinter.messagebox.showinfo("Error", "Please enter a word or letter!")
		valid = False

	## check to see if letter is good ##
	while (i < len(word) and valid):
		if word[i] == letter[0]:

			letterinword = True
			wordarray.pop(2*i)
			wordarray.insert(2*i, letter[0])

			if guessedletters.count(letter[0]) == 0:
				correctcounter = correctcounter + word.count(letter[0])
				guessedletters.append(letter[0])
		i = i + 1

	## incorrect guess ##
	if (not letterinword and valid):

		if guessedletters.count(letter[0]) == 0:
			guessedletters.append(letter[0])
			incorrectcounter = incorrectcounter + 1

	## update label ##
	remainingguesses = 6 - incorrectcounter
	wordprint = ''.join(wordarray) + "\n"
	wordguessedprint = ''.join(guessedletters)
	wordprint = wordprint + "\nGuessed Letters: \n" + wordguessedprint + "\n"
	wordprint = wordprint + "\nIncorrect Guesses Remaining: " + str(remainingguesses) + "\n"
	hiddenword.set(wordprint)

	## update image ##
	showhangman(gamelabel1, remainingguesses)

	## win condition ##
	if correctcounter == len(word):
		win(game, word)

	## lose condition ##
	if incorrectcounter >= 6:
		lose(game, word)

## word guess section ##
def wordguess(guessfield, hiddenword, game, man):

	global word
	wordguess = guessfield.get()
	i = 0
	match = True

	if (len(wordguess) == 0):
		match = False

	while i < len(wordguess):
		if word[i] != wordguess[i]:
			match = False
		i = i + 1

	if len(word) != len(wordguess):
		match = False

	if match:
		win(game, word)
	else:
		lose(game, word)


## play the actual game ##
def startgame(e, top):

	global word
	word = e.get().lower()

	if len(word) < 1:
		tkinter.messagebox.showinfo("Error", "Please enter a word!")
		top.withdraw()
		playnow()

	## lots of variables for actual game ##
	global wordarray
	wordarray = []
	global guessedletters
	guessedletters = []

	i = 0
	while i < len(word):
		wordarray.append('_')
		wordarray.append(' ')
		i = i + 1

	global correctcounter
	correctcounter = 0
	global incorrectcounter
	incorrectcounter = 0
	## end variables ##

	## more gui below ##
	top.withdraw()

	game = Toplevel()
	game.wm_title("Movies Hangman")
	game.minsize(100,100)
	game.geometry("500x450")

	man = PhotoImage(file="hangman_pics/gallows.gif")
	hiddenword = StringVar()
	gamelabel1 = Label(game, image=man)
	gamelabel1.image = man
	gamelabel1.pack()

	gamelabel2 = Label(game, textvariable=hiddenword)
	gamelabel2.pack()

	guessfield = Entry(game)
	guessfield.pack()

	remainingguesses = 6 - incorrectcounter
	wordprint = ''.join(wordarray)
	wordguessedprint = ''.join(guessedletters)
	wordprint = wordprint + "\nGuessed Letters: " + wordguessedprint + "\n"
	wordprint = wordprint + "\nIncorrect Guesses Remaining: " + str(remainingguesses) + "\n"
	hiddenword.set(wordprint)

	bguessletter = Button(game, text="Guess Letter", width=15, command=lambda:
		letterguess(guessfield, hiddenword, game, gamelabel1, man, e))
	bguessletter.pack()

	bguessword = Button(game, text="Guess Word [ONE CHANCE]", width=25, command=lambda:wordguess(guessfield, hiddenword, game, man))
	bguessword.pack()

	game.mainloop()

## quit the game ##
def quitnow():
	tkinter.messagebox.showinfo("Movies Hangman", "Thanks for playing! See you soon!")
	exit()

def win(game, word):
	tkinter.messagebox.showinfo("Winnerx2-Chicken-Dinner", "You WIN! The movie was " + word + "!")
	game.withdraw()

def lose(game, word):
	tkinter.messagebox.showinfo("Loser-Shmooser", "You LOSE! The movie was " + word + "!")
	game.withdraw()

def showhangman(gamelabel1, remainingguesses):
	if remainingguesses == 6:
		img = PhotoImage(file="hangman_pics/gallows.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 5:
		img = PhotoImage(file="hangman_pics/head.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 4:
		img = PhotoImage(file="hangman_pics/noarms.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 3:
		img = PhotoImage(file="hangman_pics/rightarm.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 2:
		img = PhotoImage(file="hangman_pics/nolegs.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 1:
		img = PhotoImage(file="hangman_pics/almostdead.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img
	if remainingguesses == 0:
		img = PhotoImage(file="hangman_pics/dead.gif")
		gamelabel1.configure(image = img)
		gamelabel1.image = img

## enter the word to be guessed ##
def playnow():

	top = Toplevel()
	top.wm_title("Game Lobby")
	top.minsize(200,100)
	top.geometry("300x80")

	label = Label(top)
	label.pack()

	e = Entry(top, width=30)
	e.insert(0, "Enter the word to be guessed")
	e.pack()

	benter = Button(top, text="Submit", width=7, command= lambda:startgame(e, top))
	benter.pack()

	top.mainloop()

root = Tk()
root.wm_title("Hangman in Python, by jl")
root.minsize(380,380)
root.geometry("300x100")

title = PhotoImage(file="hangman_pics/title.gif")
titleLabel = Label(root, image=title)
titleLabel.image = title
titleLabel.pack()

bplay = Button(root, text="Play", width=10, command=playnow)
bplay.pack()

bquit = Button(root, text="Quit", width=10, command=quitnow)
bquit.pack()

mainloop()
