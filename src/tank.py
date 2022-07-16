import pygame
from math import sin, cos, radians
import time

from src.bulletFactory import BulletFactory
class Tank():
    def __init__(self):
        self.lastShot = 0

    def loadTank(self, path: str, inicialX: int, inicialY: int, dimension=(25,32), orientation=0):
        self.orientation = orientation
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, dimension)
        self.x = inicialX
        self.y = inicialY

    def getPosition(self):
        return (self.x, self.y)
    
    def setPosition(self, position:tuple):
        self.x = position[0]
        self.y = position[1]

    def render(self, screen):
        """
        Coloca o tanque na tela
        """
        image, rect = self.rotCenter(self.image, self.orientation, self.x, self.y)
        screen.blit(image, rect)

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
        x = self.x - 5 * sin(radians(self.orientation))
        y = self.y - 5 * cos(radians(self.orientation))
        if self.verifications(level,x,y):
            self.x = x
            self.y = y

    def moveBackward(self, level):
        x = self.x + 5 * sin(radians(self.orientation))
        y = self.y + 5 * cos(radians(self.orientation))
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
            bulletFactory.makeBullet(self.x, self.y, self.orientation)