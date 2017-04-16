import socket, pdb

MAX_USERS = 30
PORT = 2021
QUIT_STRING = 'quit'


def create_a_socket(address):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    a_socket.setblocking(0)
    a_socket.bind(address)
    a_socket.listen(MAX_USERS)
    print("Currently listening at ", address)
    return a_socket

class ChatHall:
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        self.room_player_map = {} # {playerName: roomName}

    def welcome_new_user(self, new_player):
        new_player.socket.sendall(b'Welcome to the Hangman Chat Room.\nWhat is your name?\n')

    def list_all_rooms(self, player):

        if len(self.rooms) == 0:
            message = 'Currently there are no active chat rooms. You can create a chat room.\n' \
                + 'Use [join room_name] to create a room.\n'
            player.socket.sendall(message.encode())
        else:
            message = 'These are the current available chat rooms:\n'
            for room in self.rooms:
                message += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(message.encode())

    def handle_message(self, player, message):

        instructions = b'Instructions:\n'\
            + b'Type [list] to list all rooms\n'\
            + b'Type [join room_name] to join, create, or switch to a room\n' \
            + b'Type [manual] to show instructions\n' \
            + b'Type [quit] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(player.name + " says: " + message)
        if "name:" in message:
            name = message.split()[1]
            player.name = name
            print(player.name, " is entering the chat room.")
            player.socket.sendall(instructions)

        elif "join" in message:
            same_room = False
            if len(message.split()) >= 2:
                room_name = message.split()[1]
                if player.name in self.room_player_map:
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are already in the room: ' + room_name.encode())
                        same_room = True
                    else: # switch to another room
                        previous_room = self.room_player_map[player.name]
                        self.rooms[previous_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new_user(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(instructions)

        elif "list" in message:
            self.list_all_rooms(player)

        elif "manual" in message:
            player.socket.sendall(instructions)

        elif "quit" in message:
            player.socket.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
            # check if in a room or not first
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, message.encode())
            else:
                message = 'You are currently not in any rooms. \n' \
                    + 'Use [list] to see all the available chat rooms you can join.\n' \
                    + 'Use [join room_name] to join a chat room. \n'
                player.socket.sendall(message.encode())

    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print("The player '" + player.name + "' has left the chat room.\n")


class Chat_Room:
    def __init__(self, name):
        self.players = [] # a list of sockets
        self.name = name

    def welcome_new_user(self, from_player):
        message = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(message.encode())

    def broadcast(self, from_player, message):
        message = from_player.name.encode() + b":" + message
        for player in self.players:
            player.socket.sendall(message)

    def remove_player(self, player):
        self.players.remove(player)
        leave_message = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_message)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
