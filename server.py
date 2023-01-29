import pickle
import socket
import threading
import sys
from player import Player
from game import Game

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

players = [Player(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 'yellow'),
           Player(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, 'red')]

games = [Game(1, False, False)]

def handle_client(sock, tid, addr, game):

    print(f'New Client number {tid} from {addr}')

    sock.send(pickle.dumps(players[int(tid)]))
    reply = ""
    while True:
        try:
            data = pickle.loads(sock.recv(2048))
            players[int(tid)] = data

            if not data:
                print("Disconnected")
                break
            else:
                if int(tid) == 1:
                    reply = players[0]
                    players[1].isConnected()

                if int(tid) == 0:
                    reply = players[1]
                    players[0].isConnected()


                #print(tid + " " + reply.str())

                #print("Received: ", data)
                #print("Sending: ", reply)

            sock.sendall(pickle.dumps(reply))
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    sock.close

def main():
    server = "0.0.0.0"
    port = 5555

    threads = []

    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        srv_sock.bind((server, port))

    except socket.error as e:
        print(str(e))

    srv_sock.listen(4)
    print("Waiting for a connection, Server Started")

    game_counter = 0

    i = 0
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock, str(i), addr, games[game_counter]))
        t.start()
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break


if __name__ == '__main__':
    main()



