import socket, pdb

MAX_USERS = 30
PORT = 2021
QUIT_STRING = '<$quit$>'


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_USERS)
    print("Listening at: ", address)
    return s

class Hall:
    def __init__(self):
        self.rooms = {}
        self.room_player_map = {}

    def welcome_user(self, new_player):
        new_player.socket.sendall(b'Welcome to the Movies Hangman Chatroom.\nWhat is your name:\n')

    def list_rooms(self, player):

        if len(self.rooms) == 0:
            message = 'There are no active rooms currently but you create your own.\n' \
                + 'Use [join room_name] to create a room.\n'
            player.socket.sendall(message.encode())
        else:
            message = 'List of current rooms:\n'
            for room in self.rooms:
                message += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.socket.sendall(message.encode())

    def handle_message(self, player, message):

        instructions = b'Instructions:\n'\
            + b'[list] to list all the rooms\n'\
            + b'[join room_name] to join, create, or switch to a room\n' \
            + b'[manual] to show instructions\n' \
            + b'[quit] to quit\n' \
            + b'Otherwise, start typing.' \
            + b'\n'

        print(player.name + " says: " + message)
        if "name:" in message:
            name = message.split()[1]
            player.name = name
            print("There is a new connection from: ", player.name)
            player.socket.sendall(instructions)

        elif "join" in message:
            same_room = False
            if len(message.split()) >= 2:
                room_name = message.split()[1]
                if player.name in self.room_player_map:
                    if self.room_player_map[player.name] == room_name:
                        player.socket.sendall(b'You are in room: ' + room_name.encode())
                        same_room = True
                    else: # switch
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_user(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.socket.sendall(instructions)

        elif "list" in message:
            self.list_rooms(player)

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
                message = 'You are currently not in any room. \n' \
                    + 'Use [list] to see the available rooms.\n' \
                    + 'Use [join room_name] to join a room. \n'
                player.socket.sendall(message.encode())

    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print("Player: '" + player.name + "' has left\n")


class Room:
    def __init__(self, name):
        self.players = []
        self.name = name

    def welcome_user(self, from_player):
        message = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.socket.sendall(message.encode())

    def broadcast(self, from_player, message):
        message = from_player.name.encode() + b": " + message
        for player in self.players:
            player.socket.sendall(message)

    def remove_player(self, player):
        self.players.remove(player)
        leave_message = player.name.encode() + b" has left the room.\n"
        self.broadcast(player, leave_message)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.socket.fileno()
