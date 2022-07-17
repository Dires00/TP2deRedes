from json import load
import pygame
from math import sin, cos, radians
import time

from src.bulletFactory import BulletFactory

class Tank():
    def __init__(self, path, x, y, dimension = (48,64), orientation=0):
        self.lastShot = 0
        self.hp = 3
        self.inicialPosition = (x, y, orientation)
        self.speed = 20
        self.loadTank(path, x, y, dimension, orientation)

    def loadTank(self, path: str, x: int, y: int, dimension=(48,64), orientation=0):
        self.orientation = orientation
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, dimension)
        self.x = x
        self.y = y
        self.alive = True

    def isAlive(self):
        return self.alive
    
    def getPosition(self):
        return [self.x, self.y, self.orientation]
    
    def setPosition(self, position:list):
        self.x = position[0]
        self.y = position[1]
        self.orientation = position[2]

    def getHp(self):
        return self.hp

    def getInicialPosition(self):
        return self.inicialPosition

    def reset(self, inicialPosition=-1):
        if inicialPosition == -1:
            inicialPosition = self.inicialPosition
        else:
            self.inicialPosition = inicialPosition
        self.x, self.y, self.orientation = inicialPosition
        self.alive = True
        if self.hp == 0:
            return False
        return True

    def render(self, screen):
        """
        Coloca o tanque na tela
        """
        if self.alive:
            image, self.rect = self.rotCenter(self.image, self.orientation, self.x, self.y)
            screen.blit(image, self.rect)
        
        return not self.alive

    def verifyDeath(self, x, y):
        if self.rect.collidepoint(x, y):
            self.alive = False
            self.hp -= 1
            return True
        return False

    def rotCenter(self, image: pygame.Surface, ang: int, x: int, y: int):
        rotateImage = pygame.transform.rotate(image, ang)
        new_rect = rotateImage.get_rect(center = image.get_rect(center = (x, y)).center )
        return rotateImage, new_rect

    def rotateLeft(self):
        if self.orientation > 315:
            self.orientation = 0
        else:
            self.orientation += 45

    def rotateRight(self):
        if self.orientation < 0:
            self.orientation = 315
        else:
            self.orientation -= 45
    
    def verifyColision(self, level, x, y):
        return level.verifyCollision(x, y)

    def verifications(self, level, x, y):
        if self.verifyOutOfBounds(x,y) or self.verifyColision(level,x, y):
            return False
        return True

    def moveFoward(self, level):
        x = self.x - self.speed * sin(radians(self.orientation))
        y = self.y - self.speed * cos(radians(self.orientation))
        if self.verifications(level,x,y):
            self.x = x
            self.y = y

    def moveBackward(self, level):
        x = self.x + self.speed * sin(radians(self.orientation))
        y = self.y + self.speed * cos(radians(self.orientation))
        if self.verifications(level, x, y):
            self.x = x
            self.y = y

    def verifyOutOfBounds(self, x, y):
        if x < 0 or y < 0 or x > 32*32 or y > 32*21:
            return True
        return False

    def shoot(self, bulletFactory: BulletFactory):
        currentTime = time.time()
        if (currentTime - self.lastShot) > 1.2:
            self.lastShot = currentTime
            return bulletFactory.makeBullet(self.x, self.y, self.orientation, self)
        return False