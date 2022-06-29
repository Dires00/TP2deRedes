    # Simple pygame program

# Import and initialize the pygame library
import pygame
pygame.init()


def loadImage(filename: str, dimension=(32, 32), orientation=90):
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

# Set up the drawing window
screen = pygame.display.set_mode((1500, 800))

tanqueAzul = loadImage('./images/tanqueazul.png')
tanqueVermelho = loadImage('./images/tanquevermelho.png', orientation=270)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((0, 0, 0))
    
    """
    Aqui determinamos em que posição um elemento vai aparecer na tela.
    """
    screen.blit(tanqueAzul, (screen.get_width()/2, screen.get_height()/2) )    
    screen.blit(tanqueVermelho, (100, 100) )

    # Draw a solid blue circle in the center
    ''' pygame.draw.circle(screen, (255, 0, 0), (375, 250), 248)
    pygame.draw.rect(screen, (255, 255, 255), (450,225,50,50)) '''

    ''' surf = pygame.Surface((50, 50))
    surf.fill((255,255,255))
    react = surf.get_rect()
    screen.blit(surf, (250/2, 250/2)) '''

    #pygame.draw.polygon(screen, (255, 255, 255), [(0,0), (0,10), (10,10), (10,0)])
    

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()