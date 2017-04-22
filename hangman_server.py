from socket import *
import time
import sqlite3
import threading
import random
from tkinter import *
import tkinter.messagebox

#UDP SERVER
UDPserverSocket = socket(AF_INET, SOCK_DGRAM)
UDPserverSocket.bind(('', 12000))
def udp_ping():
    ##UDP PING BEGIN
    while 1:
        rand = random.randint(0, 10)
        message, address = UDPserverSocket.recvfrom(1024)
        message = message.upper()
        if rand >= 4:
            UDPserverSocket.sendto(message, address)
    ##UDP PING END

thread_udp = threading.Thread(target=udp_ping, args=())
thread_udp.start()

def guesseslimit(movie):
    num_unique_letters = len(list(set(movie)))
    print("num letters: ", num_unique_letters)
    if(num_unique_letters <= 10):
        num_guesses = round(num_unique_letters + (num_unique_letters / 3))
    else:
        num_guesses = round(num_unique_letters - (num_unique_letters / 3))
    #print(num_guesses)
    return num_guesses


global movie_metadata_connection
movie_metadata_connection = \
    sqlite3.connect('database/movie_metadata.sqlite')

# This generated a random row from the movie_metadata database
cursor = movie_metadata_connection.cursor()
cursor.execute('SELECT * ' + 'FROM movie_metadata ' + 'ORDER BY RANDOM() ' + 'LIMIT 1')
results = cursor.fetchall()

row = results[0]

# Get the data from the row.
director_name = row[1]
actor_1_name = row[3]
actor_2_name = row[2]
actor_3_name = row[5]
title_year = row[6]
movie = row[4]

rowstring = '-'.join(row)


totalguesses = guesseslimit(movie)

connected_users = []
#SERVER SOCKET EX
server_name = 'localhost'
server_port = 2021
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind((server_name,server_port))
server_socket.listen(5)
print('The server is ready to receive')



def handlethread(conn):
    global director_name
    global actor_1_name
    global actor_2_name
    global actor_3_name
    global title_year
    global movie
    global totalguesses

    while True:
        try:
            guess = conn.recv(1024)
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                time.sleep(1)
                print("No data available")
                continue
            else:
                print(e)
                sys.exit(1)
        else:
            if guess:
                guessdecode = guess.decode()
                guesslist = list(guessdecode)

                if guesslist[0] == "l":
                    del guesslist[0]
    # return the new movielist and guessedletters and remainingguesses
                    letterguess(conn, ''.join(guesslist))

                elif guesslist[0] == "m":
                    del guesslist[0]
                # return true or false...
                    result = movieguess(conn, ''.join(guesslist))


                    #conn.sendto(str(director_name).encode(), user)
                    #time.sleep(0.5)
                    #conn.sendto(str(actor_1_name).encode(), user)
                    #time.sleep(0.5)
                    #conn.sendto(str(actor_2_name).encode(), user)
                    #time.sleep(0.5)
                    #conn.sendto(str(actor_3_name).encode(), user)
                    #time.sleep(0.5)
                    #conn.sendto(str(title_year).encode(), user)
                    #time.sleep(0.5)
                    #conn.sendto(str(movie).encode(), user)
                    #time.sleep(0.5)
        # maybe send remainingguesses instead..
                    conn.sendto(str(totalguesses).encode(), user)
                    time.sleep(0.5)



    ## letter guess section ##
def letterguess(conn, guessfield, hiddenmovie):
    global correctcounter
    global incorrectcounter
    global moviearray
    global guessedletters
    global movie
    global connected_users

    i = 0
    letterinmovie = False
    valid = True
    letter = guessfield.get()
    letter = letter.lower()
    guessfield.delete(0, END)

    ## account for blank input ##
    if (len(letter) == 0):
        #tkinter.messagebox.showinfo("Error", "Please enter a word or letter!")
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
    remainingguesses = guesseslimit(movie) - incorrectcounter
    movieguessedprint = ''.join(guessedletters)
    movieprint = ''.join(moviearray) + "\n"
    movieprint = movieprint + "\nGuessed Letters OR Numbers OR Symbols: \n" + movieguessedprint + "\n"
    movieprint = movieprint + "\nIncorrect Guesses Remaining: " + str(remainingguesses) + "\n"
    #hiddenmovie.set(movieprint)


# CLIENT HANDLING:
    ## update image ##
    #showhangman(gamelabel1, remainingguesses)
    match = " "

    ## win condition ##
    if correctcounter == len(movie) - movie.count(' '):
        #win(game, movie)
        match = "True"

    ## lose condition ##
    if incorrectcounter >= guesseslimit(movie):
        #lose(game, movie)
        match = "False"

    for user in connected_users:
        conn.sendto(str(match).encode(), user)
        time.sleep(0.5)
        conn.sendto(str(movieprint).encode(), user)
        time.sleep(0.5)
        conn.sendto(str(remainingguesses).encode(), user)



## movie guess section ##

def movieguess(
    conn,
    guessfield,
    hiddenmovie
    ):

    global movie
    global connected_users

    movieguess = guessfield.get()
    i = 0
    match = "False"

    if movie.lower() == movieguess.lower():
        match = "True"

# SEND MATCH TO CLIENT
    filler = " "
    for user in connected_users:
        conn.sendto(str(match).encode(), user)
        conn.sendto(filler.encode(), user)
        conn.sendto(filler.encode(), user)
    #if match:
        #win(game, movie)
    #else:
        #lose(game, movie)





while True:
    conn, addr = server_socket.accept()    #maybe move outside loop?
    print("Connected by", addr)


    #sentence = connectionSocket.recv(1024).decode()
    #capitalizedSentence = sentence.upper()
    #connectionSocket.send(capitalizedSentence.encode()) 
    connected_users.append(addr)

    for user in connected_users:
        conn.sendto(str(rowstring).encode(), user)
        time.sleep(0.5)

    t = threading.Thread(target=handlethread, args=(conn,))
    t.start()


    #conn.close()
