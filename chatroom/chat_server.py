
from socket import *
import select
import sys
import pdb
from chat_utility import Room, Hall, Player
import chat_utility

READ_BUFFER = 1024

host = sys.argv[1] if len(sys.argv) >= 2 else ''
listen_sock = chat_utility.create_socket((host, chat_utility.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:
    read_players, write_players, error_sockets = select.select(connection_list, [], [])

    for p in read_players:
        if p is listen_sock:
            new_socket, addr = p.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_new(new_player)
        else:
            msg = p.recv(READ_BUFFER)
            if msg:
                msg = msg.decode().lower()
                hall.handle_msg(p, msg)
            else:
                p.close()
                connection_list.remove(p)

    for s in error_sockets:
        s.close()
        connection_list.remove(s)
