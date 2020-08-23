"""
This is the main server file.
"""

<<<<<<< Updated upstream
=======
import socket
import pickle
from _thread import *
from player import Player

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

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50,(0,0,255))]

def threaded_client(conn, player):

    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            # larger the size of the bits, the longer it takes to receive information
            data = pickle.loads(conn.recv(2048))  # "45, 67" -> (45, 67)
            players[player] = data


            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
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
>>>>>>> Stashed changes
