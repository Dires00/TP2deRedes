from turtle import position
import pygame
from math import sin, cos, radians


class Bullet:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.updatePosition(22)

    def render(self, screen: pygame.Surface):
        pygame.draw.circle(screen, (250,130,60), (self.x, self.y), 7)

    def verifyOutOfBounds(self):
        
        if self.x < 0 or self.y < 0 or self.x > 32*32 or self.y > 32*21:
            return True
        return False

    def verifyColision(self, level):
        return level.verifyCollision(self.x, self.y)
            
    def verifyKill(self, tanks):
        for tank in tanks:
            positionx, positiony = tank.getPosition()
            position = (positionx//32, positiony//32)
            if position == (self.x//32, self.y//32):
                print('MORTE')
                return True
        return False

    def verifications(self, level, tanks):
        if self.verifyOutOfBounds() or self.verifyColision(level) or self.verifyKill(tanks):
            return False
        return True

    def updatePosition(self, len=20):
        x = self.x - len * sin(radians(self.orientation))
        y = self.y - len * cos(radians(self.orientation))
        self.x = x
        self.y = y
