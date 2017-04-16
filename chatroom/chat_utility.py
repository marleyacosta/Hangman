
from socket import *
import pdb

MAX_CLIENTS = 30
PORT = 2021
QUIT_STRING = '<$quit$>'


def create_socket(address):
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(address)
    s.listen(MAX_CLIENTS)
    print("Now listening at ", address)
    return s

class Hall:
    def __init__(self):
        self.rooms = {}
        self.room_player_map = {}

    def welcome_new(self, new_player):
        new_player.sendall(b'Welcome to the chat room.\nPlease tell us your name:\n')

    def list_rooms(self, player):

        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            player.sendall(msg.encode())
        else:
            msg = 'Listing current rooms...\n'
            for room in self.rooms:
                msg += room + ": " + str(len(self.rooms[room].players)) + " player(s)\n"
            player.sendall(msg.encode())

    def handle_msg(self, player, msg):

        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
            + b'[<manual>] to show instructions\n' \
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(player.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            player.name = name
            print("New connection from:", player.name)
            player.sendall(instructions)

        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: 
                room_name = msg.split()[1]
                if player.name in self.room_player_map:
                    if self.room_player_map[player.name] == room_name:
                        player.sendall(b'You are already in room: ' + room_name.encode())
                        same_room = True
                    else:
                        old_room = self.room_player_map[player.name]
                        self.rooms[old_room].remove_player(player)
                if not same_room:
                    if not room_name in self.rooms:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    self.rooms[room_name].players.append(player)
                    self.rooms[room_name].welcome_new(player)
                    self.room_player_map[player.name] = room_name
            else:
                player.sendall(instructions)

        elif "<list>" in msg:
            self.list_rooms(player)

        elif "<manual>" in msg:
            player.sendall(instructions)

        elif "<quit>" in msg:
            player.sendall(QUIT_STRING.encode())
            self.remove_player(player)

        else:
            if player.name in self.room_player_map:
                self.rooms[self.room_player_map[player.name]].broadcast(player, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' \
                    + 'Use [<join> room_name] to join a room! \n'
                player.sendall(msg.encode())

    def remove_player(self, player):
        if player.name in self.room_player_map:
            self.rooms[self.room_player_map[player.name]].remove_player(player)
            del self.room_player_map[player.name]
        print("Player: " + player.name + " has left\n")


class Room:
    def __init__(self, name):
        self.players = []
        self.name = name

    def welcome_new(self, from_player):
        msg = self.name + " welcomes: " + from_player.name + '\n'
        for player in self.players:
            player.sendall(msg.encode())

    def broadcast(self, from_player, msg):
        msg = from_player.name.encode() + b":" + msg
        for player in self.players:
            player.sendall(msg)

    def remove_player(self, player):
        self.players.remove(player)
        leave_msg = player.name.encode() + b"has left the room\n"
        self.broadcast(player, leave_msg)

class Player:
    def __init__(self, socket, name = "new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name

    def fileno(self):
        return self.fileno()
