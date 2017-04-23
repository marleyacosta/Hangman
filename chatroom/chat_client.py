import select, socket, sys

import chat_utility
from chat_utility import Room, Hall, Player

from tkinter import *
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText

hostname = 'localhost' #sys.argv[1]
BUFFER_SIZE = 1024

server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_connection.connect((hostname, chat_utility.PORT))

## enter the chatroom ##

def chatroom(name, top):
    nombre = name.get()
    top.destroy()

    chatroom_display.insert(tkinter.INSERT, "You successfully connected to the server.\n")
    chatroom_display.yview(tkinter.END)  # Auto-scrolling
    #stextbox = getmessage()
    #input = stextbox.get("1.0",END)

    socket_list = [sys.stdin, server_connection]

    while True:
        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
        for s in read_sockets:
            if s is server_connection: # incoming message
                message = s.recv(BUFFER_SIZE)
                if not message:
                    chatroom_display.insert(tkinter.INSERT, "\n Sorry, the server is down.")
                    chatroom_display.yview(tkinter.END)  # Auto-scrolling
                    sys.exit(2)
                else:
                    if message == chat_utility.QUIT_STRING.encode():

                        chatroom_display.insert(tkinter.INSERT, "\n Goodbye.")
                        chatroom_display.yview(tkinter.END)  # Auto-scrolling
                        sys.exit(2)
                    else:
                        chatroom_display.insert(INSERT, message.decode())
                        sys.stdout.write(message.decode())
                        if 'What is your name:' in message.decode():
                            message_prefix = "name: " + nombre# identifier for name


                        else:
                            message_prefix = ''

                        prompt()

            else:

                message = message_prefix +
                # Add this data to the message window
                chatroom_display.insert(INSERT, message)
                chatroom_display.yview(tkinter.END)  # Auto-scrolling

                # Clean out input field for new data
                chatroom_messages.delete("0.0", tkinter.END)

                server_connection.sendall(message.encode())

def getmessage(textbox):
    return textbox


def prompt():
    print('>>', end=' ', flush = True)



chatroom_top = Tk()
chatroom_top.wm_title("Movies Hangman Chatroom")
chatroom_top.configure(bg="#4db6ac")
chatroom_top.resizable('1','1')

chatroom_display = Text(master=chatroom_top,wrap=tkinter.WORD,width=25,height=30,highlightbackground = "#000")
chatroom_display.pack(side=tkinter.TOP, fill=tkinter.BOTH)

chatroom_messages = ScrolledText(master=chatroom_top,wrap=tkinter.WORD,width=55,height=3,highlightbackground = "#000")  # In chars
chatroom_messages.pack(side=LEFT, fill=tkinter.BOTH)

send_button = Button(master=chatroom_top,text="Send",bg= "#F00",command=quit)
send_button.pack(side=RIGHT)



top = Toplevel()
top.wm_title("What is your name: ")
top.minsize(200,100)
top.geometry("300x80")

label = Label(top)
label.pack()

e = Entry(top, width=30)
e.insert(0, "")
e.pack()

benter = Button(top, text="Submit", width=7, command= lambda:chatroom(e, top))
benter.pack()

top.mainloop()

mainloop()
