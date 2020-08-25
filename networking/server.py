"""
This is the main server file.
"""

import socket
import pickle
from _thread import *
from chess.ChessEngine import *

# server is currently set to Kendal's local IPv4 Address
# change to your own for testing
#server = "97.107.134.52"
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

connected = set()
games = {}
idCount = 0


def threaded_client(conn, player, gameId):
    global idCount
    conn.send(str.encode(str(player)))  # sending chessboard object

    reply = ""
    while True:
        try:
            # larger the size of the bits, the longer it takes to receive information
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    print("Disconnected")
                    break
                else:
                    pass
                conn.sendall(pickle.dumps(game.board))
            else:
                print("No more data from client")
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing the Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    # conn is object connected,
    # adrs is the address
    conn, adrs = s.accept()
    print("Connected to:", adrs)
    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = GameState(gameId)
        print("Starting a new chess match...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))

