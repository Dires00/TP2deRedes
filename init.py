from src.jumbotron import Jumbotron
from src.bulletFactory import BulletFactory
from src.tank import Tank
import pygame, sys, pickle, time
from src.map_def import Level
from socket import *

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
    
    pygame.mixer.init()
    
    pygame.mixer.music.load('./src/audio/music/wait.mp3')
    finalExplosionSound = pygame.mixer.Sound('./src/audio/sounds/finalexplosion.wav')
    lowerExplosionSound = pygame.mixer.Sound('./src/audio/sounds/lowerexplosion.wav')
    shotSound = pygame.mixer.Sound('./src/audio/sounds/shot.mp3')

    
    level = Level()

    client.send('Hello!')
    player = client.recv()

    width, height = level.loadMap('first.map')
    screen = pygame.display.set_mode((width*32, height*32+64))
    jumbotron = Jumbotron()
    screen.fill((0, 0, 0))
    level.loadTileTable('./src/images/tileset.png')
    level.render(screen)
    pygame.display.update()

    maps = ['first.map', 'second.map', 'third.map']
    choice = 0

    bulletFactory = BulletFactory()

    if choice == 3:
        whiteTank = Tank('./src/images/whiteTank.png', width*16, 64, orientation=90)
        whiteTank.render(screen)

        purpleTank = Tank('./src/images/purpleTank.png', width*16, height*32-64, orientation=90)
        purpleTank.render(screen)

    blueTank = Tank('./src/images/blueTank.png', width*32-64, height*32/2, orientation=90)
    blueTank.render(screen)
    
    redTank = Tank('./src/images/redTank.png', 64, height*16, orientation=270)
    redTank.render(screen)
    jumbotron.scoreBoard(redTank, blueTank, screen)
    enemyTanks = []

    pygame.mixer.music.play(-1)
    if player == 0:
        run = True
        while run:
            pygame.time.delay(75)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            width, height = level.loadMap(maps[choice])
            screen.fill((0, 0, 0))
            level.render(screen)
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_RSHIFT]:
                break
            
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                choice += 1
                if choice == len(maps):
                    choice = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                choice -= 1
                if choice == -1:
                    choice = len(maps) -1

        client.send(choice)
        jumbotron.loading(screen)
        pygame.display.update()
        print(client.recv())

    else:
        choice = client.recv()

    if choice == 3:
        tanks = [blueTank, redTank, whiteTank, purpleTank]

    else:
        if player == 0:
            myTank = blueTank
            enemyTanks.append(redTank)
        else:
            myTank = redTank
            enemyTanks.append(blueTank)


    width, height = level.loadMap(maps[choice])
    screen.fill((0, 0, 0))
    level.render(screen)  
    
    pygame.mixer.music.fadeout(500)

    screen.fill((0, 0, 0))
    level.render(screen)        
    jumbotron.readyToGo(screen, level)
    pygame.display.update()

    pygame.mixer.music.load('./src/audio/music/music_zapsplat_game_music_action_agressive_pounding_tense_electro_synth_028.mp3')
    pygame.mixer.music.play(-1)

   
    enemyTank = enemyTanks[0]
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
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            myTank.rotateLeft()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            myTank.rotateRight()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            myTank.moveFoward(level)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            myTank.moveBackward(level)

        if keys[pygame.K_RSHIFT] or keys[pygame.K_SPACE]:
            shot = myTank.shoot(bulletFactory)
            if shot:
                shotSound.play()

        screen.fill((0, 0, 0))
        level.render(screen)

        death = myTank.render(screen)
        kill = enemyTank.render(screen)
        jumbotron.scoreBoard(redTank.getHp(), blueTank.getHp(), screen)
        
        bulletFactory.renderBullets(screen, level, (myTank, enemyTank))
        
        if kill:
            auxPosition = myTank.getInicialPosition()
            myTank.reset(enemyTank.getInicialPosition())
            run = enemyTank.reset(auxPosition)
            bulletFactory.reset()
            if enemyTank.getHp() != 0:
                lowerExplosionSound.play()
        
        elif death:
            auxPosition = myTank.getInicialPosition()
            run = myTank.reset(enemyTank.getInicialPosition())
            enemyTank.reset(auxPosition)
            bulletFactory.reset()
            if myTank.getHp() != 0:
                lowerExplosionSound.play()

        position = myTank.getPosition()
        message = position
        message.append(shot)
        client.send(message)

        message = client.recv()
        position = message[:3]
        shot = message[3]

        enemyTank.setPosition(position)

        if shot:
            shotSound.play()
            enemyTank.shoot(bulletFactory)

        pygame.display.update()
    
    if enemyTank.getHp() > 0:
        jumbotron.youLose(screen)
    else:
        jumbotron.youWin(screen)
    
    jumbotron.scoreBoard(redTank.getHp(), blueTank.getHp(), screen)
    finalExplosionSound.play()
    pygame.display.update()
    time.sleep(5)
    client.send([-1, -1, -1, False])

   

if __name__ == '__main__':
    sys.exit(main(sys.argv))
