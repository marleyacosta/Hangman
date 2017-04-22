import select, socket, sys, pdb
import chat_utility
from chat_utility import Hall, Room, Player


BUFFER_SIZE = 1024

host = 'localhost'
listen_sock = chat_utility.create_socket((host, chat_utility.PORT))

hall = Hall()
connection_list = []
connection_list.append(listen_sock)

while True:

    read_players, write_players, error_sockets = select.select(connection_list, [], [])
    for player in read_players:
        if player is listen_sock:
            new_socket, add = player.accept()
            new_player = Player(new_socket)
            connection_list.append(new_player)
            hall.welcome_user(new_player)

        else: # new message
            message = player.socket.recv(BUFFER_SIZE)
            if message:
                message = message.decode().lower()
                hall.handle_message(player, message)
            else:
                player.socket.close()
                connection_list.remove(player)

    for sock in error_sockets: # close the error sockets
        sock.close()
        connection_list.remove(sock)
