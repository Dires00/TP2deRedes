import pygame
import pygame.locals
from map_def import Level

if __name__=='__main__':
    pygame.init()
    level = Level()
    width, height = level.loadMap()
    screen = pygame.display.set_mode((width*32, height*32))
    screen.fill((255, 255, 255))
    level.loadTileTable('tileset.png')
    level.render(screen)
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass