from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup, SolidGroup
from Model.Spawner import Spawner

from EventHandler import EventHandler

import time

fluidGroup = FluidGroup()
solidGroup = SolidGroup()

size = (800, 800)
campo = Campo(fluidGroup.air, size)

spawner = Spawner(campo)
spawner.spawnEntities()

view = View(campo)

eventHandler = EventHandler(view, campo)

running = True

while running:
    campo.move()
    view.draw()
    view.update()
    eventHandler.handleEvents()
    """
    TODO:
        -gestire meglio
    """
    if eventHandler.quit == True:
        running = False


