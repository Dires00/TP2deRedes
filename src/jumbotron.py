import time
import pygame
from src.map_def import Level

class Jumbotron():
    def __init__(self):
        self.font = pygame.font.Font(None, 50)

    def scoreBoard(self, score1:int, score2:int,screen: pygame.Surface):
        if score1 == 3:
            if score2 == 3:
                text = self.font.render('3           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('3           :           2', True,(255,255,255))
            elif score2 == 0:
                text = self.font.render('3           :           0', True,(255,255,255))
            else:
                text = self.font.render('3           :           1', True,(255,255,255))
            
        elif score1 == 2:
            if score2 == 3:
                text = self.font.render('2           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('2           :           2', True,(255,255,255))
            elif score2 == 0:
                text = self.font.render('2           :           0', True,(255,255,255))
            else:
                text = self.font.render('2           :           1', True,(255,255,255))

        elif score1 == 1:
            if score2 == 3:
                text = self.font.render('1           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('1           :           2', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('1           :           0', True,(255,255,255))
            else:
                text = self.font.render('1           :           1', True,(255,255,255))

        else:
            if score2 == 3:
                text = self.font.render('0           :           3', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('0           :           2', True,(255,255,255))
            elif score2 == 2:
                text = self.font.render('0           :           0', True,(255,255,255))
            else:
                text = self.font.render('0           :           1', True,(255,255,255))


        textRect = text.get_rect()
        textRect.center = (32*16, 21*32+32) 
        screen.blit(text, textRect)

    def loading(self, screen):
        text = self.font.render('Aguardando o outro jogador...', True,(255,255,255))

        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)

    def youWin(self, screen):
        winnerSound = pygame.mixer.Sound('./src/audio/sounds/winner.mp3')
        text = self.font.render('Você Venceu!!!!', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        winnerSound.play()

    def youLose(self, screen):
        loserSound = pygame.mixer.Sound('./src/audio/sounds/loser.mp3')
        text = self.font.render('Você Perdeu!!!!', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        loserSound.play()

    def readyToGo(self, screen, level: Level):

        bepSound = pygame.mixer.Sound('./src/audio/sounds/bep.wav')
        beeeeeeeepSound = pygame.mixer.Sound('./src/audio/sounds/beeeeep.mp3')

        level.render(screen)
        text = self.font.render('3', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        pygame.display.update()
        bepSound.play()
        time.sleep(1)

        level.render(screen)
        text = self.font.render('2', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        pygame.display.update()
        bepSound.play()
        time.sleep(1)

        level.render(screen)
        text = self.font.render('1', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        pygame.display.update()
        bepSound.play()
        time.sleep(1)

        level.render(screen)
        text = self.font.render('Ready?', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        pygame.display.update()
        bepSound.play()
        time.sleep(1)

        level.render(screen)
        text = self.font.render('Go!!', True,(255,255,255))
        textRect = text.get_rect()
        textRect.center = (32*16, (21*32+64)/2) 
        screen.blit(text, textRect)
        pygame.display.update()
        beeeeeeeepSound.play()
        time.sleep(0.4)