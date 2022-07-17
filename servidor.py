from email import message
from http import server
from socket import *
import pickle
import threading
import sys
import time

class Server():
    """Classe que representa o servidor"""
    def __init__(self, serverPort: int):
        self.serverPort = serverPort
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', serverPort))
        self.serverSocket.listen()
        self.playerPosition = [
            [32*32-64, 21*32/2, 90],
            [64, 21*32/2, 270]
        ]
        self.newShot = [False, False]
        self.players = []
        self.threads = []
    
    def accept(self):
        """Método em que o servidor aceita o cliete e cria uma thread para o mesmo"""
        for i in range(2):
            print(f'Esperando o {i+1}º cliente ')
            self.players.append(self.serverSocket.accept())
            t =threading.Thread(target=self.connect, args=(self.players[i][0],i))
            self.threads.append(t)
        
        for thread in self.threads:
            thread.start()

        flag = True
        while flag:
            time.sleep(1)
            flag = False
            for thread in self.threads:
                if threading.Thread.is_alive():
                    flag = True
    
    def connect(self, player: socket, indice: int):
        """Método usado para o servidor receber uma mensagem do cliente"""
        self.recv(player)
        self.send(indice, player)
        
        while True:
            message = self.recv(player)

            position = message[:3]
            shot = message[3]
            self.playerPosition[indice] = position
            self.newShot[indice] = shot

            shot = self.newShot[0 if indice == 1 else 1]
            message = self.playerPosition[0 if indice == 1 else 1]
            message.append(shot)

            self.send(message, player)
            
            if shot:
                self.newShot[0 if indice == 1 else 1] = False
        
    def send(self, message, player:socket):
        print(message)
        message = pickle.dumps(message)
        print(f'message:{message}')
        player.send(message)

    def recv(self, player:socket):
        message = player.recv(2048)
        return pickle.loads(message)
            

def main(args):
    serverPort = int(args[1])
    server = Server(serverPort)
    server.accept()

if __name__ == '__main__':
    sys.exit(main(sys.argv))