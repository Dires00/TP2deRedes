import pygame

class Tank():
    def loadTank(self, path: str, inicialX: int, inicialY: int, dimension=(50,60), orientation=0):
        self.orientation = orientation
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, dimension)
        self.x = inicialX
        self.y = inicialY

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
        
        