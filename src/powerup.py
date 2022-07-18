import pygame
from random import randint

class PowerUp:
    # tipos de power up
    # 0: velocidade
    def __init__(self):
        self.type = 0
        self.isUp = False
        self.upLast = pygame.time.get_ticks()
        self.setRandLocation()
         
    
    def render(self, screen: pygame.Surface):
        now = pygame.time.get_ticks()
        if self.isUp:
            self.upLast = pygame.time.get_ticks()
            pygame.draw.circle(screen, (0,0,255), self.getLocation(), 15)
        elif now - self.upLast > 5000:
            self.setRandLocation()
            self.isUp = True

    def setLocation(self, place):
        self.place = place
    
    def setRandLocation(self):
        place = randint(0, 3)
        self.place = place

    def getLocation(self):
        places = [
            (15*32 + 16, 8*32 + 16),
            (13*32 + 16, 10*32 + 16),
            (15*32 + 16, 12*32 + 16),
            (17*32 + 16, 10*32 + 16)
        ]
        return places[self.place]

    def getPlace(self):
        return self.place

    def grabPowerUp(self, tanks: list):
        for tank in tanks:
            x, y = self.getLocation()
            if tank.rect.collidepoint(x, y):
                tank.addPowerUp(self.type)
                self.isUp = False
                self.upLast = pygame.time.get_ticks()
