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

palla = Ball((200,200), 20, solidGroup.wood)

palla.setVelocity((30,12))
palla.setAcceleration((-2.3, -0.2))

campo.addEntity(palla)

quadrato = Quadrato(29, (33,33), 45, solidGroup.wood)
quadrato.setVelocity((40,12))
quadrato.setAcceleration((0.05, -0.2))

campo.addEntity(quadrato)

quadrato2 = Quadrato(43, (89,125), 10, solidGroup.wood)
quadrato2.setVelocity((40,23))
quadrato2.setAcceleration((-6, -0.2))

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