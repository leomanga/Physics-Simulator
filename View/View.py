import pygame
from datetime import datetime
from icecream import ic
from Model.ContactInfo import ContactInfo

from Model.Entities.BoundingBox import BoundingBox

class View():
    #events list
    QUIT = pygame.QUIT
    MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN

    clickedColor = (177, 177, 177)
    baseColor = (255, 0, 0)
    debugColor = (0,0,255)

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
    
    def drawBoundingBox(self, boundingBox: BoundingBox, color:tuple=debugColor):
        topRight = (boundingBox.topLeft[0], boundingBox.bottomRight[1])
        bottomLeft = (boundingBox.bottomRight[0], boundingBox.topLeft[1])
        
        self.drawLine(topRight, tuple(boundingBox.topLeft), color)
        self.drawLine(tuple(boundingBox.topLeft), bottomLeft, color)
        self.drawLine(bottomLeft, tuple(boundingBox.bottomRight), color)
        self.drawLine(tuple(boundingBox.bottomRight), topRight, color)
    
    def drawLine(self, point1:tuple, point2:tuple, color:tuple=baseColor):
        #print(point2)
        pygame.draw.line(self._screen, color, point1, point2, 2)

    def drawInfo(self, contactInfo: ContactInfo, centerOfMass):
        self.drawCircle(contactInfo._penetrationPoint, 10, (255,170,170))
        self.drawCircle(centerOfMass, 10, (255,170,170))
        normalAdj = contactInfo._penetrationNormal*300
        self.drawLine(tuple(contactInfo._penetrationPoint), tuple(contactInfo._penetrationPoint + normalAdj), (0,255,90) )

    def drawText(self, text, coord):
        textSurface = self._font.render(f"{text}", False, (0, 0, 0))
        self._screen.blit(textSurface, coord)
    
    def update(self):
        pygame.display.flip()

    def draw(self, debug = False):
        self._fillScreen(self._screenColor)
        for e in self._campo.entities:
            e.printItself(self, debug)

        if debug:
            self._drawGrids()
            
        self._printFps()    

    def _drawGrids(self):
        nCols = self._campo.spatialGrid.nCellsAxis[0]
        nRows = self._campo.spatialGrid.nCellsAxis[1]

        colLength = self._campo.spatialGrid.gridColLength
        rowLength = self._campo.spatialGrid.gridRowLength

        for i in range(nCols):       
            pygame.draw.line(self._screen, (23,234,243) ,(colLength * i ,0), (colLength * i,self._campo._size[1]) , 3)

        for j in range(nRows):
            pygame.draw.line(self._screen, (23,234,243), (0, rowLength * j), (self._campo._size[0], rowLength*j))
            
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
    
