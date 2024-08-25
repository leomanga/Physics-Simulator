from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup
from Model.Materials import SolidGroup

from Model.Entities import Ball, RegularPolygon

from Model.Vector import Vector

from EventHandler import EventHandler

import time

fluidGroup = FluidGroup()
solidGroup = SolidGroup()

size = (800, 800)
campo = Campo(fluidGroup.air, size)

palla = Ball((300,300), 50, solidGroup.wood)

palla.setVelocity((30,30))
palla.setAcceleration((0, 0))

campo.addEntity(palla)

quadrato = RegularPolygon(123, (10,10), 45, 5, solidGroup.wood)
quadrato.setVelocity((10, 10))
quadrato.setAcceleration((10, 10))

campo.addEntity(quadrato)

quadrato2 = RegularPolygon(40, (650,200), 45, 4, solidGroup.wood)
quadrato2.setVelocity((-20,0))
quadrato2.setAcceleration((-0.05, 0))

campo.addEntity(quadrato2)

quadrato3 = RegularPolygon(40, (700,200), 36, 4, solidGroup.wood)
quadrato3.setVelocity((-20,0))
quadrato3.setAcceleration((-0.6, 0))

campo.addEntity(quadrato3)


palla2 = Ball((60, 600), 40, solidGroup.wood)
palla2.setVelocity((65,-40))
palla2.setAcceleration((0,+9.81))

campo.addEntity(palla2)


"""for i in range (10):
    e = Ball((80 * i, 60 * i), 32, solidGroup.wood)
    e.setVelocity((10,10))
    campo.addEntity(e)"""

view = View(campo)

eventHandler = EventHandler(view, campo)

running = True

while running:
    campo.move()
    view.draw(campo.entities)
    view.update()
    eventHandler.handleEvents()
    """
    TODO:
        -gestire meglio
    """
    if eventHandler.quit == True:
        running = False


