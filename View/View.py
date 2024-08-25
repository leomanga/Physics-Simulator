import pygame
from datetime import datetime

class View():
    #events list
    QUIT = pygame.QUIT
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

    clickedColor = (177, 177, 177)
    baseColor = (255, 0, 0)

    def __init__(self, campo, screenColor:tuple=(255,255,255)):
        self._campo = campo
        pygame.init()
        self._screen = pygame.display.set_mode(self._campo.size)
        self._screenColor = screenColor
        self._fillScreen(screenColor)
        pygame.display.set_caption('ARMANDO')
        pygame.font.init()
        self._font = pygame.font.SysFont('Comic Sans MS', 30)
        self._lastTime = datetime.now()
        
    def getEvents(self):
        """
        events:
            - QUIT
            - MOUSEBUTTONDOWN
        """
        return pygame.event.get()

    def drawCircle(self, center:tuple, radius:float, color:tuple=baseColor):
        pygame.draw.circle(self._screen, color, center, radius)
    
    def drawPolygon(self, vectorList: list[tuple], color:tuple=baseColor):
        pygame.draw.polygon(self._screen, color, vectorList)
    
    def drawLine(self, point1:tuple, point2:tuple, color:tuple=baseColor):
        #print(point2)
        pygame.draw.line(self._screen, color, point1, point2, 3)

    def drawPoint(self, contactPoint):
        self.drawCircle(contactPoint, 3, (255,170,170))

    def drawText(self, text, coord):
        textSurface = self._font.render(f"{text}", False, (0, 0, 0))
        self._screen.blit(textSurface, coord)
    
    def update(self):
        pygame.display.flip()

    def draw(self, entities):
        self._fillScreen(self._screenColor)
        for e in entities:
            e.printItself(self)
        self._printFps()       
            
    def setScreenColor(self, color:tuple):
        # può fare comodo per cambiare colore dello sfondo in base al materiale
        self._screenColor = color

    def getMousePosition(self):
        return pygame.mouse.get_pos()

    def _printFps(self):
        newTime = datetime.now()
        deltaTime = newTime - self._lastTime
        self._lastTime = newTime
        fps = 1 // deltaTime.total_seconds()
        textSurface = self._font.render(f"fps:{fps}", False, (0, 0, 0))
        self._screen.blit(textSurface, (0,0))

    def _fillScreen(self, color:tuple):
        self._screen.fill(color)
    
