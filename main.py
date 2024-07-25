from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup
from Model.Materials import SolidGroup

from Model.Entities import Ball, Quadrato

import time

fluidGroup = FluidGroup()
solidGroup = SolidGroup()

size = (400, 400)
campo = Campo(fluidGroup.air, size)

palla = Ball((200,200), 20, solidGroup.wood)

palla.setVelocity((30,12))
palla.setAcceleration((-2.3, -0.2))

campo.addEntity(palla)

quadrato = Quadrato(29, (33,33), 45, solidGroup.wood)
quadrato.setVelocity((30,12))
quadrato.setAcceleration((-2.3, -0.2))

campo.addEntity(quadrato)

view = View(campo)

running = True

while running:
    campo.move()
    view.draw(campo.entities)
    view.update()

    for event in view.getEvents():
        if event.type == view.QUIT:
            running = False