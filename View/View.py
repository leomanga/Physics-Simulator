import pygame

class View():
    #events list
    QUIT = pygame.QUIT


    def __init__(self, campo):
        self._campo = campo
        pygame.init()
        self._screen = pygame.display.set_mode(self._campo.size)
        self._screen.fill((0,0,0))
        pygame.display.set_caption('ARMANDO')

    def getEvents(self):
        """
        events:
            - QUIT
        """
        return pygame.event.get()

    def _drawCircle(self, center:tuple, radius:float, color:tuple=(255,0,0)):
        pygame.draw.circle(self._screen, color, center, radius)
        
    def update(self):
        pygame.display.flip()

    def draw(self, entities):

        self._screen.fill((0,0,0))
        for e in entities:
            self._drawCircle(e.position, e.radius)
