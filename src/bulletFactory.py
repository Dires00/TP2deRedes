
from pygame import Surface
from src.bullet import Bullet


class BulletFactory:
    def __init__(self):
        self.bullets = []

    def makeBullet(self, x, y, orientation, tank):
        bullet = Bullet(x, y, orientation, tank)
        self.bullets.append(bullet)
        return True
        

    def renderBullets(self, screen: Surface, level, tanks):
        ex_bullets = []
        for bullet in self.bullets:
            bullet.updatePosition()
            if bullet.verifications(level, tanks):
                bullet.render(screen)
            else:
                ex_bullets.append(bullet)

        for bullet in ex_bullets:
           self.bullets.remove(bullet)
           del bullet
    
    def reset(self):
        for bullet in self.bullets:
            self.bullets.remove(bullet)
            del bullet
        