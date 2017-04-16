
from socket import *
import select
import sys
from chat_utility import Room, Hall, Player
import chat_utility

READ_BUFFER = 1024

if len(sys.argv) < 2:
    print("Usage: python3 chat_client.py [hostname]", file = sys.stderr)
    sys.exit(1)
else:
    server_connection = socket(AF_INET, SOCK_STREAM)
    server_connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_connection.connect((sys.argv[1], chat_utility.PORT))

def prompt():
    print('>', end=' ', flush=True)

print("Connected to server\n")
msg_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

    for s in read_sockets:
        if s is server_connection:
            msg = s.recv(READ_BUFFER)

            if not msg:
                print("Server down")
                sys.exit(2)
            else:
                if msg == chat_utility.QUIT_STRING.encode():
                    sys.stdout.write('Bye\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())

                    if 'Please enter your name' in msg.decode():
                        msg_prefix = 'name: '
                    else:
                        msg_prefix = ''

                    prompt()
        else:
            msg = msg_prefix + sys.stdin.readline()
            server_connection.sendall(msg.encode())
