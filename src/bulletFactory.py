
from pygame import Surface
from src.bullet import Bullet


class BulletFactory:
    def __init__(self):
        self.bullets = []

    def makeBullet(self, x, y, orientation):
        self.bullets.append(Bullet(x, y, orientation))

    def renderBullets(self, screen: Surface, level, tanks: tuple):
        ex_bullets = []
        for bullet in self.bullets:
            bullet.updatePosition()
            if bullet.verifications(level, tanks):
                bullet.render(screen)
            else:
                ex_bullets.append(bullet)

        for bullet in ex_bullets:
           self.bullets.remove(bullet)