from socket import *
from tkinter import *
import tkinter.messagebox
#from tkinter.scrolledText import ScrolledText
import sqlite3



# socket ex

server_name = 'localhost'
server_port = 2021
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))
# sentence = input('Input lowercase sentence:')
#clientSocket.send(sentence.encode())
#modified_sentence = client_socket.recv(1024)
#print('From Server:', modifiedSentence.decode())



#global variables
movie = ""
director_name = ""
actor_1_name = ""
actor_2_name = ""
actor_3_name = ""
title_year = ""
correctcounter = 0
incorrectcounter = 0
moviearray = []
guessedletters = []
totalguesses = 0
remainingguesses = 0
#movie_metadata_connection =

def sendletterguess(guessfield):
    guessfield = "l" + guessfield
    client_socket.send(guessfield.encode())

def sendmovieguess(guessfield):
    guessfield = "m" + guessfield
    client_socket.send(guessfield.encode())

## enter the chatroom ##
def chatroom():
    chatroom_top = tkinter.Tk()
    chatroom_top.wm_title("Movies Hangman Chatroom")
    chatroom_top.resizable('1','1')

    chatroom_messages = ScrolledText(
        master=chatroom_top,
        wrap=tkinter.WORD,
        width=50,  # In chars
        height=25,
        highlightbackground = "#004d40")  # In chars

    chatroom_display = Text(
        master=chatroom_top,
        wrap=tkinter.WORD,
        width=50,
        height=3,
        highlightbackground = "#000")

    send_button = Button(
        master=chatroom_top,
        text="Send",
        bg= "#F00",
        command=quit)

    # Compute display position for all objects
    chatroom_messages.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    chatroom_display.pack(side=tkinter.TOP, fill=tkinter.BOTH)
    send_button.pack(side=tkinter.LEFT)




########## probably dont need for client. get remainingguesses from server #######
def guesseslimit(movie):
    num_unique_letters = len(list(set(movie)))
    print("num letters: ", num_unique_letters)
    if(num_unique_letters <= 10):
        num_guesses = round(num_unique_letters + (num_unique_letters / 3))
    else:
        num_guesses = round(num_unique_letters - (num_unique_letters / 3))
    #print(num_guesses)
    return num_guesses


# get vars from server #######################################
def hint():
    hint = 'The movie was released in ' + title_year \
        + ' and directed by ' + director_name + '.\n' + 'Starring ' \
        + actor_1_name + ', ' + actor_2_name + ', and ' + actor_3_name \
        + '.'
    tkinter.messagebox.showinfo('Hint', hint)

def startgame():
    global movie
    global director_name
    global actor_1_name
    global actor_2_name
    global actor_3_name
    global title_year



    # GET HINT INFO FROM SERVER #################

    #cursor = movie_metadata_connection.cursor()


    #cursor.execute('SELECT * ' + 'FROM movie_metadata '
                   #+ 'ORDER BY RANDOM() ' + 'LIMIT 1')

    #results = cursor.fetchall()

    #row = results[0]

    director_name = client_socket.recv(1024).decode()
    actor_1_name = client_socket.recv(1024).decode()
    actor_2_name = client_socket.recv(1024).decode()
    actor_3_name = client_socket.recv(1024).decode()
    title_year = client_socket.recv(1024).decode()
    movie = client_socket.recv(1024).decode()

    #global movie
    global moviearray
    global guessedletters
    global remainingguesses
    global totalguesses

    totalguesses = int(client_socket.recv(1024).decode())
    remainingguesses = int(client_socket.recv(1024).decode())

    i = 0
    #print(movie)
    while i < len(movie):

        moviearray.append('_')
        moviearray.append(' ')

        #if(movie[i] == " "):
            #moviearray.append('  ')
        #else:
            #moviearray.append('_')
            #moviearray.append(' ')

        i = i + 1

    global correctcounter
    correctcounter = 0
    global incorrectcounter
    incorrectcounter = 0

    game = Toplevel()
    game.wm_title('Movies Hangman')
    game.configure(bg="#e0e0e0")
    game.minsize(380, 380)
    game.geometry('680x490')

    man = PhotoImage(file='hangman_pics/gallows.gif')
    hiddenmovie = StringVar()
    gamelabel1 = Label(game, image=man)
    gamelabel1.image = man
    gamelabel1.pack()

    gamelabel2 = Label(game, textvariable=hiddenmovie)
    gamelabel2.pack()

    guessfield = Entry(game)
    guessfield.pack()

# remainingguesses -> get from server
    #remainingguesses = guesseslimit(movie) - incorrectcounter

    #movieprint = ''.join(moviearray)
    #movieguessedprint = ''.join(guessedletters)
    #movieprint = movieprint + '\nGuessed Letters OR Numbers OR Symbols: ' + movieguessedprint \
    #    + '\n'
    #movieprint = movieprint + '\nIncorrect Guesses Remaining: ' \
    #    + str(remainingguesses) + '\n'
    #hiddenmovie.set(movieprint)
    showhangman(gamelabel1, remainingguesses)

    movieprint = client_socket.recv(1024).decode()
    hiddenmovie.set(movieprint)

    bguessletter = Button(game, text='Guess Letter', width=10,
                          command=lambda : sendletterguess(guessfield))
    bguessletter.pack()

    bguessmovie = Button(game, text='Guess Movie', width=10,
                         command=lambda : sendmovieguess(guessfield))
    bguessmovie.pack()

    bhint = Button(game, text='Hint', width=10, command=hint)
    bhint.pack()

    bchatroom = Button(game, text='Chat Room', width=10, command=chatroom)
    bchatroom.pack()

    game.mainloop()

def quitnow():
    tkinter.messagebox.showinfo('Movies Hangman',
                                'Thanks for playing! See you soon!')
    client_socket.close()
    exit()

def win(game, movie):
    tkinter.messagebox.showinfo('WINNER',
                                'You WIN! The movie was ' + movie + '!')
    game.withdraw()

def lose(game, movie):
    tkinter.messagebox.showinfo('LOSER',
                                'You LOSE! The movie was ' + movie + '!')
    game.withdraw()

def showhangman(gamelabel1, remainingguesses):
    global totalguesses
    limit = totalguesses
    increment = round(limit / 7)
    #print("increment: ", increment)

    if remainingguesses == limit:
        img = PhotoImage(file='hangman_pics/gallows.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == (limit - increment):
        img = PhotoImage(file='hangman_pics/head.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == (limit - 2 * increment):
        img = PhotoImage(file='hangman_pics/noarms.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == (limit - 3 * increment):
        img = PhotoImage(file='hangman_pics/rightarm.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == (limit - 4 * increment):
        img = PhotoImage(file='hangman_pics/nolegs.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == (limit - 5 * increment):
        img = PhotoImage(file='hangman_pics/almostdead.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img
    if remainingguesses == 0:
        img = PhotoImage(file='hangman_pics/dead.gif')
        gamelabel1.configure(image=img)
        gamelabel1.image = img






# Connect to the movie database

#global movie_metadata_connection
#movie_metadata_connection = \
#    sqlite3.connect('database/movie_metadata.sqlite')

root = Tk()
root.wm_title('Movies Hangman')
root.configure(bg="#e0e0e0")
root.minsize(380, 380)
root.geometry('680x490')

title = PhotoImage(file='hangman_pics/title.gif')
titleLabel = Label(root, image=title)
titleLabel.image = title
titleLabel.pack()

bplay = Button(root, text='Play', width=10, command=startgame)

bplay.pack()

bquit = Button(root, text='Quit', width=10, command=quitnow)
bquit.pack()

mainloop()
