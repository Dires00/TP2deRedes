from src.scoreBoard import ScoreBoard
from src.bulletFactory import BulletFactory
from src.tank import Tank
import pygame, sys, pickle
from src.map_def import Level
from socket import *
from struct import *
import time

class Client():
    def __init__(self, serverName: str, serverPort: int):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((serverName, serverPort))

    def send(self, message):
        message = pickle.dumps(message)
        self.clientSocket.send(message)

    def recv(self):
        message = self.clientSocket.recv(2048)
        return pickle.loads(message)
        
def main(args):
    client = Client(args[1], int(args[2]))
    
    pygame.init()
    level = Level()
    width, height = level.loadMap()
    screen = pygame.display.set_mode((width*32, height*32+64))
    scoreBoard = ScoreBoard()
    screen.fill((0, 0, 0))
    level.loadTileTable('./src/images/tileset.png')
    level.render(screen)

    bulletFactory = BulletFactory()
    client.send('Hello!')
    scoreBoard.loading(screen)
    pygame.display.update()
    player = client.recv()

    tanqueAzul = Tank('./src/images/tanqueazul.png', width*32-64, height*32/2, orientation=90)
    tanqueAzul.render(screen)
    
    tanqueVermelho = Tank('./src/images/tanquevermelho.png', 64, height*16, orientation=270)
    tanqueVermelho.render(screen)
    scoreBoard.render(tanqueVermelho, tanqueAzul, screen)

    if player == 0:
        myTank = tanqueAzul
        enemyTank = tanqueVermelho
    else:
        myTank = tanqueVermelho
        enemyTank = tanqueAzul

    pygame.display.flip()
    run = True
    while run:
        kill = False
        death = False
        shot = False
        pygame.time.delay(75)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            myTank.rotateLeft()

        if keys[pygame.K_RIGHT]:
            myTank.rotateRight()

        if keys[pygame.K_UP]:
            myTank.moveFoward(level)

        if keys[pygame.K_DOWN]:
            myTank.moveBackward(level)

        if keys[pygame.K_RSHIFT]:
            shot = myTank.shoot(bulletFactory)

        screen.fill((0, 0, 0))
        level.render(screen)

        death = myTank.render(screen)
        kill = enemyTank.render(screen)
        scoreBoard.render(tanqueVermelho.getHp(), tanqueAzul.getHp(), screen)
        
        bulletFactory.renderBullets(screen, level, (myTank, enemyTank))
        
        if kill:
            myTank.reset()
            run = enemyTank.reset()
            bulletFactory.reset()
        
        elif death:
            run = myTank.reset()
            enemyTank.reset()
            bulletFactory.reset()

        position = myTank.getPosition()
        message = position
        message.append(shot)
        client.send(message)

        message = client.recv()
        position = message[:3]
        shot = message[3]

        enemyTank.setPosition(position)

        if shot:
            enemyTank.shoot(bulletFactory)

        pygame.display.update()

    if myTank.getHp() > 0:
        scoreBoard.youWin(screen)
    else:
        scoreBoard.youLose(screen)
    pygame.display.update()

    time.sleep(6)
if __name__ == '__main__':
    sys.exit(main(sys.argv))
