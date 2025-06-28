import socket
from _thread import *
import pickle
from game import Game

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def update_status_file(game):
    try:
        with open("status.txt", "r") as f:
            lines = f.readlines()
    except:
        lines = [
            "games_played: 0\n",
            "p1_win: 0\n",
            "p2_win: 0\n",
            "ties: 0\n"
        ]

    data = {line.split(":")[0].strip(): int(line.split(":")[1]) for line in lines}
    data["games_played"] += 1
    hasil = game.winner()
    if hasil == 0:
        data["p1_win"] += 1
    elif hasil == 1:
        data["p2_win"] += 1
    else:
        data["ties"] += 1

    with open("status.txt", "w") as f:
        for k in data:
            f.write(f"{k}: {data[k]}\n")

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    if game.bothWent() and not game.reported:
                        update_status_file(game)
                        game.reported = True

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
