import select, socket, sys

import chat_utility
from chat_utility import Room, Hall, Player

from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


# global functions
global hostname
hostname = 'localhost' #sys.argv[1]

global BUFFER_SIZE
BUFFER_SIZE = 1024


## enter the chatroom ##
def chatroomGUI():


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

    # Connects a client to the chatroom server
    clientconnection(chatroom_top)

    chatroom_top.mainloop()

def prompt():
    print('>>', end=' ', flush = True)

def clientconnection(chatroom_wn):


    # Connect to the server
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection.connect((hostname, chat_utility.PORT))


    tkinter.messagebox.showinfo('Hint', "You successfully connected to the server.\n")
    socket_list = [sys.stdin, server_connection]

    clientloop(server_connection, socket_list, chatroom_wn)


def clientloop(server_connection, socket_list, chatroom_wn):

    message_prefix = ''

    while True:
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for s in read_sockets:
            if s is server_connection: # incoming message
                message = s.recv(BUFFER_SIZE)

                print("line 83 message: ", message)

                if not message:
                    tkinter.messagebox.showinfo('Server is down.', "Sorry, the server is down.")
                    chatroom_wn.quit() # close the chatroom window
                    server_connection.close()
                    #sys.exit(2)
                else:
                    if message == chat_utility.QUIT_STRING.encode():
                        tkinter.messagebox.showinfo('Goodbye', "You are exiting the chatroom. Goodbye.")
                        chatroom_wn.quit() # close the chatroom window
                        server_connection.close()
                        #sys.exit(2)
                    else:
                        sys.stdout.write(message.decode())
                        print("line 96 message: ", message.decode())
                        if 'What is your name:' in message.decode():
                            message_prefix = 'name: ' # identifier for name
                        else:
                            message_prefix = ''
                        prompt()

            else:
                message = message_prefix + sys.stdin.readline()
                print("line 105 message: ", message)
                server_connection.sendall(message.encode())
