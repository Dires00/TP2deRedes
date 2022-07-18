from src.jumbotron import Jumbotron
from src.bulletFactory import BulletFactory
from src.tank import Tank
import pygame, sys, pickle, time
from src.map_def import Level
from socket import *
from src.powerup import PowerUp

class Client():
    """
    Classe que representa o cliente
    """
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
        client.recv()

    else:
        choice = client.recv()

    blueTank = Tank('./src/images/blueTank.png', width*32-64, height*32/2, orientation=90)
    blueTank.render(screen)
    
    redTank = Tank('./src/images/redTank.png', 64, height*16, orientation=270)
    redTank.render(screen)
    jumbotron.scoreBoard(redTank, blueTank, screen)
    
    if choice == 2:
        whiteTank = Tank('./src/images/whiteTank.png', width*16, 64, orientation=180)
        whiteTank.render(screen)
    
        purpleTank = Tank('./src/images/purpleTank.png', width*16, height*32-64, orientation=0)
        purpleTank.render(screen)
        jumbotron.bigScoreBoard('3   :   3   :   3   :   3', screen)

    width, height = level.loadMap(maps[choice])
    screen.fill((0, 0, 0))
    level.render(screen)  
    
    pygame.mixer.music.fadeout(500)

    powerUp = PowerUp()

    screen.fill((0, 0, 0))
    level.render(screen)        
    jumbotron.readyToGo(screen, level)
    pygame.display.update()

    pygame.mixer.music.load('./src/audio/music/music_zapsplat_game_music_action_agressive_pounding_tense_electro_synth_028.mp3')
    pygame.mixer.music.play(-1)
    if choice == 2:
        tanks = [blueTank, redTank, whiteTank, purpleTank]
    else:
        tanks = [blueTank, redTank]

    if choice != 2:
        if player == 1:
            myTank = redTank
            enemyTank = blueTank
        else:
            myTank = blueTank
            enemyTank = redTank
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

            if keys[pygame.K_f] or keys[pygame.K_RETURN]:
                myTank.consumePowerUp()

            screen.fill((0, 0, 0))
            level.render(screen)

            death = myTank.render(screen)
            kill = enemyTank.render(screen)
            jumbotron.scoreBoard(redTank.getHp(), blueTank.getHp(), screen)
            
            powerUp.render(screen)
            powerUp.grabPowerUp(tanks)
            bulletFactory.renderBullets(screen, level, (myTank, enemyTank))
            place = -1
            if player == 0:
                place = powerUp.getPlace()

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
            message.append(place)
            client.send(message)

            message = client.recv()
            position = message[:3]
            shot = message[3]
            place = message[4]

            powerUp.setLocation(place)

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
        client.send([-1, -1, -1, False, -1])

    else:
        run = True
        alive = 4
        wasAlive = 4
        
        while run:
            shot = False
            pygame.time.delay(75)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                tanks[player].rotateLeft()

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                tanks[player].rotateRight()

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                tanks[player].moveFoward(level)

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                tanks[player].moveBackward(level)

            if keys[pygame.K_RSHIFT] or keys[pygame.K_SPACE]:
                shot = tanks[player].shoot(bulletFactory)
                if shot:
                    shotSound.play()
            if keys[pygame.K_f] or keys[pygame.K_RETURN]:
                tanks[player].consumePowerUp()

            screen.fill((0, 0, 0))
            level.render(screen)

            powerUp.render(screen)
            powerUp.grabPowerUp(tanks)

            place = -1
            if player == 0:
                place = powerUp.getPlace()

            jumbotron.bigScoreBoard(f'{tanks[0].getHp()}   :   {tanks[1].getHp()}   :   {tanks[2].getHp()}   :   {tanks[3].getHp()}', screen)
            
            bulletFactory.renderBullets(screen, level, tanks)

            alive = 0
            for tank in tanks:
                if tank.isAlive():
                    tank.render(screen)
                    alive += 1

            if wasAlive > alive:
                lowerExplosionSound.play()

            if alive == 1:
                auxPosition = tanks[0].getInicialPosition()
                for i, tank in enumerate(tanks):
                    if i != 3:
                        tank.reset(tanks[i+1].getInicialPosition())
                    else:
                        tank.reset(auxPosition)
            
            position = tanks[player].getPosition()
            message = position
            message.append(shot)
            message.append(place)
            client.send(message)

            message = client.recv()
            for i, information in enumerate(message):
                if i != player and i != 4:
                    position = information[:3]
                    shot = information[3]
                    tanks[i].setPosition(position[:])
                    if shot:
                        tanks[i].shoot(bulletFactory)

            alive = 0
            for tank in tanks:
                if tank.isAlive():
                    alive += 1

            if alive == 1:
                break

            wasAlive = alive
            place = message[4]
            
            powerUp.setLocation(place)
            pygame.display.update()
        
        if tanks[player].getHp() > 0:
            jumbotron.youWin(screen)
        else:
            jumbotron.youLose(screen)
        
        if choice != 2:
            jumbotron.scoreBoard(redTank.getHp(), blueTank.getHp(), screen)
            finalExplosionSound.play()
        else:
            jumbotron.bigScoreBoard(f'{tanks[0].getHp()}   :   {tanks[1].getHp()}   :   {tanks[2].getHp()}   :   {tanks[3].getHp()}', screen)
        pygame.display.update()
        time.sleep(5)
        client.send([-1, -1, -1, False])


if __name__ == '__main__':
    sys.exit(main(sys.argv))
