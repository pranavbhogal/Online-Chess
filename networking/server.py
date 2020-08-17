"""
This is the main server file.
Run this file first. Then run client twice to add players.
"""

import socket
from _thread import *
import sys

# server is currently set to Kendal's local IPv4 Address
# change to your own for testing
server = "192.168.1.39"
port = 5555

# socket.AF_INET & socket.SOCK_STREAM specify the type of connection/stream
# we'll use these to connect to an ipv4 address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# open port and listen for connections, setting to 2 to allow 2 players
s.listen(2)
print("Server started, waiting for a connection")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def convert_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0), (100,100)]

def threaded_client(conn, player):

    conn.send(str.encode(convert_pos(pos[player])))
    reply = ""
    while True:
        try:
            # larger the size of the bits, the longer it takes to receive information
            data = read_pos(conn.recv(2048).decode())  # "45, 67" -> (45, 67)
            pos[player] = data


            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(str.encode(convert_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    # conn is object connected,
    # adrs is the address
    conn, adrs = s.accept()
    print("Connected to:", adrs)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
