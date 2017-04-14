#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *
import tkinter.messagebox
import sqlite3


## letter guess section ##

def letterguess(
    guessfield,
    hiddenmovie,
    game,
    gamelabel1,
    man,
    ):
    global correctcounter
    global incorrectcounter
    global moviearray
    global guessedletters
    global movie

    i = 0
    letterinmovie = False
    valid = True
    letter = guessfield.get()
    letter = letter.lower()
    guessfield.delete(0, END)

    # # account for blank input ##

    if len(letter) == 0:
        tkinter.messagebox.showinfo('Error',
                                    'Please enter a word or letter!')
        valid = False

    # # check to see if letter is good ##

    while i < len(movie) and valid:
        if movie[i] == letter[0]:

            letterinmovie = True
            moviearray.pop(2 * i)
            moviearray.insert(2 * i, letter[0])

            if guessedletters.count(letter[0]) == 0:
                correctcounter = correctcounter + movie.count(letter[0])
                guessedletters.append(letter[0])
        i = i + 1

    # # incorrect guess ##

    if not letterinmovie and valid:

        if guessedletters.count(letter[0]) == 0:
            guessedletters.append(letter[0])
            incorrectcounter = incorrectcounter + 1

    # # update label ##

    remainingguesses = 6 - incorrectcounter
    movieguessedprint = ''.join(guessedletters)
    movieprint = ''.join(moviearray) + '\n'

    movieprint = movieprint + '''
Guessed Letters:
''' \
        + movieguessedprint + '\n'
    movieprint = movieprint + '\nIncorrect Guesses Remaining: ' \
        + str(remainingguesses) + '\n'
    hiddenmovie.set(movieprint)

    # # update image ##

    showhangman(gamelabel1, remainingguesses)

    # # win condition ##

    if correctcounter == len(movie):
        win(game, movie)

    # # lose condition ##

    if incorrectcounter >= 6:
        lose(game, movie)

<<<<<<< Updated upstream
## letter guess section ##
def letterguess(guessfield, hiddenmovie, game, gamelabel1, man):
	global correctcounter
	global incorrectcounter
	global moviearray
	global guessedletters
	global movie

	i = 0
	letterinmovie = False
	valid = True
	letter = guessfield.get()
	letter = letter.lower()
	guessfield.delete(0, END)

	## account for blank input ##
	if (len(letter) == 0):
		tkinter.messagebox.showinfo("Error", "Please enter a word or letter!")
		valid = False

	## check to see if letter is good ##
	while (i < len(movie) and valid):
		if movie[i].lower() == letter[0]:

			letterinmovie = True
			moviearray.pop(2*i)
			moviearray.insert(2*i, letter[0])

			if guessedletters.count(letter[0]) == 0:
				correctcounter = correctcounter + movie.count(letter[0].lower()) + movie.count(letter[0].upper())
				guessedletters.append(letter[0])
		i = i + 1

	## incorrect guess ##
	if (not letterinmovie and valid):

		if guessedletters.count(letter[0]) == 0:
			guessedletters.append(letter[0])
			incorrectcounter = incorrectcounter + 1

	## update label ##
	remainingguesses = 6 - incorrectcounter
	movieguessedprint = ''.join(guessedletters)
	movieprint = ''.join(moviearray) + "\n"

	movieprint = movieprint + "\nGuessed Letters: \n" + movieguessedprint + "\n"
	movieprint = movieprint + "\nIncorrect Guesses Remaining: " + str(remainingguesses) + "\n"
	hiddenmovie.set(movieprint)

	## update image ##
	showhangman(gamelabel1, remainingguesses)

	## win condition ##
	if correctcounter == len(movie):
		win(game, movie)

	## lose condition ##
	if incorrectcounter >= 6:
		lose(game, movie)
=======
>>>>>>> Stashed changes

## movie guess section ##

def movieguess(
    guessfield,
    hiddenmovie,
    game,
    man,
    ):

    global movie

    movieguess = guessfield.get()
    i = 0
    match = True

    if len(movieguess) == 0:
        match = False

    while i < len(movieguess):
        if movie[i] != movieguess[i]:
            match = False
        i = i + 1

<<<<<<< Updated upstream
	while i < len(movieguess):
		if movie[i].lower() != movieguess[i].lower():
			match = False
		i = i + 1
=======
    if len(movie) != len(movieguess):
        match = False
>>>>>>> Stashed changes

    if match:
        win(game, movie)
    else:
        lose(game, movie)


def hint():
    hint = 'The movie was released in ' + title_year \
        + ' and directed by ' + director_name + '.\n' + 'Starring ' \
        + actor_1_name + ', ' + actor_2_name + ', and ' + actor_3_name \
        + '.'
    tkinter.messagebox.showinfo('Hint', hint)


## play the actual game ##

def startgame():

    global movie
    global director_name
    global actor_1_name
    global actor_2_name
    global actor_3_name
    global title_year

    # Get the movie

    cursor = movie_metadata_connection.cursor()

    # This generated a random row from the movie_metadata database

    cursor.execute('SELECT * ' + 'FROM movie_metadata '
                   + 'ORDER BY RANDOM() ' + 'LIMIT 1')

    results = cursor.fetchall()

    row = results[0]

    # Get the data from the row.

    director_name = row[1]
    actor_1_name = row[3]
    actor_2_name = row[2]
    actor_3_name = row[5]
    title_year = row[6]
    movie = row[4]

    # # lots of variables for actual game ##

    global moviearray
    moviearray = []
    global guessedletters
    guessedletters = []

    i = 0
    while i < len(movie):
        moviearray.append('_')
        moviearray.append(' ')
        i = i + 1

    global correctcounter
    correctcounter = 0
    global incorrectcounter
    incorrectcounter = 0

    # # end variables ##

    game = Toplevel()
    game.wm_title('Movies Hangman')
    game.minsize(380, 380)
    game.geometry('380x480')

    man = PhotoImage(file='hangman_pics/gallows.gif')
    hiddenmovie = StringVar()
    gamelabel1 = Label(game, image=man)
    gamelabel1.image = man
    gamelabel1.pack()

    gamelabel2 = Label(game, textvariable=hiddenmovie)
    gamelabel2.pack()

    guessfield = Entry(game)
    guessfield.pack()

    remainingguesses = 6 - incorrectcounter
    movieprint = ''.join(moviearray)
    movieguessedprint = ''.join(guessedletters)
    movieprint = movieprint + '\nGuessed Letters: ' + movieguessedprint \
        + '\n'
    movieprint = movieprint + '\nIncorrect Guesses Remaining: ' \
        + str(remainingguesses) + '\n'
    hiddenmovie.set(movieprint)

    bguessletter = Button(game, text='Guess Letter', width=10,
                          command=lambda : letterguess(guessfield,
                          hiddenmovie, game, gamelabel1, man))
    bguessletter.pack()

    bguessmovie = Button(game, text='Guess Movie', width=10,
                         command=lambda : movieguess(guessfield,
                         hiddenmovie, game, man))
    bguessmovie.pack()

    bhint = Button(game, text='Hint', width=10, command=hint)
    bhint.pack()

    bchatroom = Button(game, text='Chat Room', width=10, command=hint)
    bchatroom.pack()


    game.mainloop()


## quit the game ##

def quitnow():
    tkinter.messagebox.showinfo('Movies Hangman',
                                'Thanks for playing! See you soon!')
    movie_metadata_connection.close()
    exit()


def win(game, movie):
    tkinter.messagebox.showinfo('Winnerx2-Chicken-Dinner',
                                'You WIN! The movie was ' + movie + '!')
    game.withdraw()


def lose(game, movie):
    tkinter.messagebox.showinfo('Loser-Shmooser',
                                'You LOSE! The movie was ' + movie + '!'
                                )
    game.withdraw()


def showhangman(gamelabel1, remainingguesses):
    if remainingguesses == 6:
        img = PhotoImage(file='hangman_pics/gallows.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 5:
        img = PhotoImage(file='hangman_pics/head.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 4:
        img = PhotoImage(file='hangman_pics/noarms.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 3:
        img = PhotoImage(file='hangman_pics/rightarm.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 2:
        img = PhotoImage(file='hangman_pics/nolegs.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 1:
        img = PhotoImage(file='hangman_pics/almostdead.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 0:
        img = PhotoImage(file='hangman_pics/dead.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img


# Connect to the movie database

global movie_metadata_connection
movie_metadata_connection = \
    sqlite3.connect('database/movie_metadata.sqlite')

root = Tk()
root.wm_title('Movies Hangman')
root.minsize(380, 380)
root.geometry('380x480')

title = PhotoImage(file='hangman_pics/title.gif')
titleLabel = Label(root, image=title)
titleLabel.image = title
titleLabel.pack()

bplay = Button(root, text='Play', width=10, command=startgame)
bplay.pack()

bquit = Button(root, text='Quit', width=10, command=quitnow)
bquit.pack()

mainloop()
