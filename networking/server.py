import socket
from _thread import *
from chess.ChessEngine import *
import pickle
import time
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# '97.107.134.52' server ipaddress
server = '97.107.134.52'
port = 5555

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen()
print("[START] Waiting for a connection")

connections = 0

games = {0: GameState()}


def threaded_client(conn, game):
    global currentId, pos, connections

    name = None
    gameset = games[game]

    if connections % 2 == 0:
        currentId = "White"
    else:
        currentId = "Black"

    gameset.start_user = currentId

    # pickles objects and sends to server
    data_string = pickle.dumps(gameset)

    if currentId == "Black":
        gameset.ready = True
        gameset.startTime = time.time()

    conn.send(data_string)
    connections += 1

    while True:
        if game not in games:
            break

        try:
            data = conn.recv(8192 * 3)
            dedata = data.decode("utf-8")
            if not data:
                break
            else:
                if dedata == "winner black":
                    gameset.winner = "black"
                    print("[GAME] Player Black won the game!", game)
                if dedata == "winner white":
                    gameset.winner = "white"
                    print("[GAME] Player White won the game!", game)

                # this needs to be updated to commands used to update chess board moves
                if dedata == "update moves":
                    gameset.update_moves()

                if dedata.count("name") == 1:
                    name = data.split(" ")[1]
                    if currentId == "Black":
                        gameset.p2Name = name
                    elif currentId == "White":
                        gameset.p1Name = name

                print("Received a board from", currentId, "in the game", game)

                if gameset.ready:
                    if gameset.turn == "w":
                        gameset.time1 = 900 - (time.time() - gameset.startTime) - gameset.storedTime1
                    else:
                        gameset.time2 = 900 - (time.time() - gameset.startTime) - gameset.storedTime2

                sendData = pickle.dumps(gameset)
                print("Sending the board to the player", currentId, "in the game", game)

            conn.sendall(sendData)

        except Exception as e:
            print(e)

        connections -= 1
        try:
            del games[game]
            print("[GAME] Game", game, "ended")
        except:
            pass
        print("[DISCONNECTED] Player", name, "left the game", game)
        conn.close()


while True:
    conn, addr = s.accept()
    g = -1
    print("[CONNECT] New connection to: ", addr)

    for game in games.keys():
        if games[game].ready is False:
            g = game

    if g == -1:
        try:
            g = list(games.keys())[-1]+1
            games[g] = GameState()
        except:
            g = 0
            games[g] = GameState()

    print("[DATA] Number of Connections:", connections + 1)
    print("[DATA] Number of Games:", len(games))

    start_new_thread(threaded_client, (conn, g))
