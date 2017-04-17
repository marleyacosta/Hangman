import select, socket, sys
import chat_utility
from chat_utility import Room, Hall, Player


BUFFER_SIZE = 1024

if len(sys.argv) < 2:
    print("Usage: python3 chat_client.py [hostname]", file = sys.stderr)
    sys.exit(1)
else:
    server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_connection.connect((sys.argv[1], chat_utility.PORT))

def prompt():
    print('>>', end=' ', flush = True)

print("You successfully connected to the server.\n")
message_prefix = ''

socket_list = [sys.stdin, server_connection]

while True:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])
    for s in read_sockets:
        if s is server_connection: # incoming message
            message = s.recv(BUFFER_SIZE)
            if not message:
                print("Sorry, the server is down.")
                sys.exit(2)
            else:
                if message == chat_utility.QUIT_STRING.encode():
                    sys.stdout.write('Goodbye.\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(message.decode())
                    if 'What is your name:' in message.decode():
                        message_prefix = 'name: ' # identifier for name
                    else:
                        message_prefix = ''
                    prompt()

        else:
            message = message_prefix + sys.stdin.readline()
            server_connection.sendall(message.encode())
