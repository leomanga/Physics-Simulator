import pygame

class View():
    def __init__(self, campo):
        self._campo = campo

    def start(self):
        pygame.init()
        pygame.display.set_mode(self._campo.size)

        running = True

        while running:

            self._campo.move()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False