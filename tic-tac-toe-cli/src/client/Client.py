import socket
import sys
import select

import client_constants
import ClientMessages
from Game import Game

class Client:

    def __init__(self, port, serverIP, serverPort):
        self.port = port
        self.serverIP = serverIP;
        self.serverPort = serverPort;
        self.client = socket.socket(client_constants.SOCKET_TYPE, client_constants.SOCKET_PROTOCOL)
        self.playing = False
        self.waitingForPlay = False

    def start(self):
        self.client.bind(('', self.port))


    def get_messages(self):
        inputs = [self.client, sys.stdin]

        while True:
            if not self.playing:
                print("1.Convidar\n2.Listar \n0.Sair")
                print("Escolha uma opção:")
            elif not self.waitingForPlay:
                self.read_play()
                continue

            ins, outs, exs = select.select(inputs,[],[])

            for i in ins:
                if i == sys.stdin:
                    if not (self.playing):
                        res=input()
                        if res=="1":
                            print("Username to invite: ")
                            username = sys.stdin.readline()
                            if(self.invite_player(username)):
                                self.currentGame = Game()
                                self.waitingForPlay = False
                                self.playing = True
                                self.opponent = username
                            continue
                        elif res=="2":
                            self.request_list()
                            continue
                        elif res=="0":
                            return
                        else:
                            print("\n Escolha inválida")
                            continue
                    else:
                        if self.waitingForPlay:
                            continue
                        self.read_play()


                elif i == self.client:
                    msg = self.recv_message()
                    msg = msg.split()
                    if msg[0] == ClientMessages.USER_INVITE:
                        if self.playing:
                            self.invite_response(False, msg[1])
                            continue
                        print("Player " + msg[1] + " wants to play a game")
                        while True:
                            print("Accept? (y/n)")
                            accept = input()
                            if (accept == "y") or (accept =="n"): break
                        accept = accept == "y"
                        self.invite_response(accept, msg[1])
                        if accept:
                            self.playing = True
                            self.waitingForPlay = True
                            self.opponent = msg[1]
                            self.currentGame = Game()
                        continue
                    if msg[0] == ClientMessages.RCV_PLAY:
                        self.recv_play(msg)
                        continue



    def read_play(self):
        while (1):
            try:
                print("Column: ")
                column = int(sys.stdin.readline())
                if column not in (1,2,3):
                    print("Invalid play. Please go again.")
                    continue
                print("Row: ")
                row = int(sys.stdin.readline())
                if row not in (1,2,3):
                    print("Invalid play. Please go again.")
                    continue
                break
            except ValueError:
                print("Invalid play. Please go again.")
        while not(self.currentGame.play(column, row)):
            print("Invalid play")
            print("Column: ")
            column = int(sys.stdin.readline())
            print("Row: ")
            row = int(sys.stdin.readline())
        ended = self.currentGame.isFinished()
        self.send_play(column, row, ended)
        self.currentGame.drawBoard()
        if ended:
            self.waitingForPlay = False
            self.playing = False
        self.waitingForPlay = True

    def recv_play(self, msg):
        self.currentGame.play(int(msg[2]), int(msg[3]))
        self.currentGame.drawBoard()
        self.waitingForPlay = False
        if msg[4] == "True":
            self.playing = False
            self.currentGame = False



    def register(self, username):
        self.send_message("REG " + username)
        msg = self.recv_message()
        msg = msg.split()
        if msg[0] != "REG":
            return False
        if msg[1] == "ok":
            return True
        else:
            return False

    def request_list(self):
        self.send_message(ClientMessages.LIST_USERS)
        msg = self.recv_message()
        msg = msg.split()
        for i in range(1, len(msg), 2):
            print(msg[i] + "   " + ("occupied" if (msg[i+1] == "false") else "free"))

    def invite_player(self, username):
        msg = ClientMessages.USER_INVITE + " " + username
        self.send_message(msg)
        msg = self.recv_message()
        msg = msg.split()
        return msg[2] == 'True'

    def invite_response(self, accept, username):
        msg = "ACP " + username + " " + str(accept)
        self.send_message(msg)

    def send_play(self, row, column, end):
        msg = ClientMessages.MAKE_PLAY + " " + self.opponent + " " + str(row) + " " + str(column) + " " + str(end)
        self.send_message(msg)


    def send_message(self, msg):
        self.client.sendto(msg.encode(), (self.serverIP, self.serverPort))
        (msg, addr) = self.recv_message()

    def recv_message(self):
        (msg, addr) = self.client.recvfrom(1024)
        return msg.decode()

    def kill(self):
        self.client.close()
