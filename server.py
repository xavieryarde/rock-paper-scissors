import socket
import threading
import pickle
import random
from game import Game

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

options = ["Rock", "Paper", "Scissors"]
connected = set()
games = {}
idCount = 0
timeout = 10


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
                    if data.startswith("player:"):
                        player_name = data.split("player:")[1].strip()
                        game.set_player_name(p, player_name)

                    if data == "reset":
                        game.resetWent()
                        game.start_timer() 

                    elif data != "get" and not(data.startswith("player:")):
                        game.play(p, data)

                    elapsed_time = game.get_elapsed_time()
                    if elapsed_time > timeout:
                        if p == 0:
                            if not game.p1Went:
                                random_choice = random.choice(options)
                                game.play(p, random_choice)

                        else:
                            if not game.p2Went:
                                random_choice = random.choice(options)
                                game.play(p, random_choice)
    

                    game.set_countdown(int(timeout - elapsed_time))

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
        games[gameId].start_timer()
        p = 1


    threading.Thread(target=threaded_client, args=(conn, p, gameId)).start()