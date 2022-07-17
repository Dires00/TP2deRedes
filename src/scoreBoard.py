from email import message
import pygame

class ScoreBoard():
    def __init__(self):
        self.font = pygame.font.Font(None, 50)

    def render(self, score1:int, score2:int,screen: pygame.Surface):
        if score1 == 3:
            if score2 == 3:
                text = self.font.render('3           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('3           :           2', True,(255,255,255))
            else:
                text = self.font.render('3           :           1', True,(255,255,255))
            
        elif score1 == 2:
            if score2 == 3:
                text = self.font.render('2           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('2           :           2', True,(255,255,255))
            else:
                text = self.font.render('2           :           1', True,(255,255,255))

        else:
            if score2 == 3:
                text = self.font.render('1           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('1           :           2', True,(255,255,255))
            else:
                text = self.font.render('1           :           1', True,(255,255,255))

        textRect = text.get_rect()
        textRect.center = (32*16, 21*32+32) 
        screen.blit(text, textRect)

    def loading(self, screen):
        text = self.font.render('Aguardando o outro jogador...', True,(255,255,255))

        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)

    def youWin(self, screen):
        text = self.font.render('Você Venceu!!!!', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)

    def youLose(self, screen):
        text = self.font.render('Você Perdeu!!!!', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
