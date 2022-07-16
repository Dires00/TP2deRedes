import pygame
from time import sleep
class Level(object):
    def loadMap(self, mapName="./src/maps/first.map", tileSet='./src/maps/tileset.png'):
        self.map = [[]]
        file = open(mapName)
        self.height = 0
        self.width = 0
        while True:
            tile = file.read(1)
            if tile == '':
                break
            if tile == '\n':
                self.map.append([])
                self.height += 1
                continue
            self.map[self.height].append(tile)
            if self.height == 0:
                self.width += 1
        file.close()
        self.height += 1
        return (self.width, self.height)
    
    def loadTileTable(self, filename, width=32, height=32):
        image = pygame.image.load(filename).convert()
        imageWidth, imageHeight = image.get_size()
        self.tileTable = []
        for tileX in range(0, int(imageWidth/width)):
            line = []
            self.tileTable.append(line)
            for tileY in range(0, int(imageHeight/height)):
                rect = (tileX*width, tileY*height, width, height)
                line.append(image.subsurface(rect))

    def render(self, screen: pygame.Surface):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if(tile == '.'):
                    screen.blit(self.tileTable[1][0], (x*32, y*32))
                elif(tile == '#'):
                    screen.blit(self.tileTable[1][1], (x*32, y*32))
                elif(tile == '>'):
                    screen.blit(self.tileTable[5][2], (x*32, y*32))
                elif(tile == '<'):
                    screen.blit(self.tileTable[4][2], (x*32, y*32))
                elif(tile == '/'):
                    screen.blit(self.tileTable[5][1], (x*32, y*32))
                elif(tile == '\\'):
                    screen.blit(self.tileTable[4][1], (x*32, y*32))
                elif(tile == '('):
                    screen.blit(self.tileTable[4][0], (x*32, y*32))
                elif(tile == ')'):
                    screen.blit(self.tileTable[5][0], (x*32, y*32))
                elif(tile == '_'):
                    screen.blit(self.tileTable[2][1], (x*32, y*32))
                elif(tile == '0'):
                    screen.blit(self.tileTable[2][0], (x*32, y*32))
                elif(tile == '-'):
                    screen.blit(self.tileTable[6][2], (x*32, y*32))

    def getTile(self, x, y):
        try:
            char = self.map[y][x]
        except IndexError:
            return {}
        try:
            return self.key[char]
        except KeyError:
            return {}

    def verifyCollision(self, x, y):
        tilex = int(x//32) 
        tiley = int(y//32) 

        if self.map[tiley][tilex] != '.' and self.map[tiley][tilex] != '#':
            return True
        return False