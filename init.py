from tanque import Tank
import pygame
import pygame.locals
from map_def import Level

def loadImage(filename: str, dimension=(50, 60), orientation=90):
    """
    Método usado para carregar algumas imagens para o codigo.

    filename: nome do arquivo que será carregado
    dimension: dimensão que o arquivo será carregado (largura, altura)
    orientation: rotação da imagem
    return: retorna a imagem carregada
    """
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, dimension)
    image = pygame.transform.rotate(image, orientation)
    return image

def rotCenter(image, ang: int, x: int, y: int):
    rotateImage = pygame.transform.rotate(image, ang)
    new_rect = rotateImage.get_rect(center = image.get_rect(center = (x, y)).center )
    return rotateImage, new_rect

if __name__=='__main__':
    pygame.init()
    level = Level()
    width, height = level.loadMap()
    screen = pygame.display.set_mode((width*32, height*32))
    screen.fill((255, 255, 255))
    level.loadTileTable('images/tileset.png')
    level.render(screen)

    tanqueAzul = Tank()
    tanqueAzul.loadTank('./images/tanqueazul.png', width*32-64, height*32/2, orientation=90)
    tanqueAzul.render(screen)
    
#6r5tu6yiu8y7uyrte
    tanqueVermelho = Tank()
    tanqueVermelho.loadTank('./images/tanquevermelho.png', 64, height*16, orientation=270)
    tanqueVermelho.render(screen)
    """
    Carrega as images e geram os tanques
    """

    #screen.blit(tanqueAzul, (width*32-64, height*16-tanqueAzul.get_height()/2) )  
    """
    Coloca os tanques na tela, nas posições passadas como parametros
    """
    pygame.display.flip()
    run = True
    while run:
        pygame.time.delay(75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            tanqueAzul.rotateLeft()

        if keys[pygame.K_RIGHT]:
            tanqueAzul.rotateRight()

        if keys[pygame.K_UP]:
            pass

        level.render(screen)
        tanqueAzul.render(screen)
        tanqueVermelho.render(screen)
        pygame.display.update()

    
    """
    game_over = False
    while not game_over:
        pygame.time.delay(100)
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                game_over = True
            
            
            elif event.type == pygame.locals.KEYDOWN:
                pressed_key = pygame.key.get_pressed()

        if pressed_key[pygame.K_LEFT]:
            print('Vai para a esquerda')
            orin += 45
            width -= 45
            tanqueAzul =  pygame.transform.rotate(tanqueAzul, orin)
            #level.render(screen)
            screen.blit(tanqueAzul, (width*32/2, height*16))
            tanqueAzul.scroll(-100, -100)
            pygame.display.flip()
                    
    """
    

    while pygame.event.wait().type != pygame.locals.QUIT:
        pass