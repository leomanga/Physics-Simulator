from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup
from Model.Materials import SolidGroup

from Model.Entities import Ball, Quadrato

import time

fluidGroup = FluidGroup()
solidGroup = SolidGroup()

size = (800, 800)
campo = Campo(fluidGroup.air, size)

palla = Ball((200,33), 20, solidGroup.wood)

palla.setVelocity((-30,0))
palla.setAcceleration((-2.3, 0))

campo.addEntity(palla)

quadrato = Quadrato(29, (33,33), 0, solidGroup.wood)
quadrato.setVelocity((23, 0))
quadrato.setAcceleration((0.05, 0))

campo.addEntity(quadrato)

quadrato2 = Quadrato(43, (600,33), 0, solidGroup.wood)
quadrato2.setVelocity((-19,0))
quadrato2.setAcceleration((-0.2, 0))

campo.addEntity(quadrato2)

view = View(campo)

running = True

while running:
    campo.move()
    view.draw(campo.entities)
    view.update()

    for event in view.getEvents():
        if event.type == view.QUIT:
            running = False