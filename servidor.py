from socket import *
import pickle, threading, sys, time

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
        self.choice = -1
    
    def accept(self):
        """Método em que o servidor aceita o cliete e cria uma thread para o mesmo"""
        for i in range(2):
            print(f'Esperando o {i+1}º cliente ')
            self.players.append(self.serverSocket.accept())
            if i == 0:
                t =threading.Thread(target=self.mapChoice, args=(self.players[i][0], ))
                t.start()
            t =threading.Thread(target=self.connect, args=(self.players[i][0],i))
            self.threads.append(t)
        
        while self.choice == -1:
            time.sleep(0.5)

        for t in self.threads:
            t.start()

        flag = True
        while flag:
            time.sleep(1)
            flag = False
            for thread in self.threads:
                if thread.is_alive():
                    flag = True
    
    def mapChoice(self, player: socket):
        self.recv(player)
        self.send(0, player)
        self.choice = self.recv(player)

    def connect(self, player: socket, indice: int):
        """Método usado para o servidor receber uma mensagem do cliente"""
        if indice == 1:
            self.recv(player)
            self.send(indice, player)
            self.send(self.choice, player)
        else:
            self.send(self.choice, player)
        
        while True:
            message = self.recv(player)

            position = message[:3]
            shot = message[3]

            if position[0] == -1:
                break
            self.playerPosition[indice] = position
            self.newShot[indice] = shot

            shot = self.newShot[0 if indice == 1 else 1]
            message = self.playerPosition[0 if indice == 1 else 1]
            message.append(shot)

            self.send(message, player)
            
            if shot:
                self.newShot[0 if indice == 1 else 1] = False
        
        player.close()
        
    def send(self, message, player:socket):
        message = pickle.dumps(message)
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