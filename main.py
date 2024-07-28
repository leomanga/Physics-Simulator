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

palla = Ball((400,33), 50, solidGroup.wood)

palla.setVelocity((-30,0))
palla.setAcceleration((-2.3, 0))

campo.addEntity(palla)

quadrato = Quadrato(29, (33,33), 0, solidGroup.wood)
quadrato.setVelocity((23, 23))
quadrato.setAcceleration((0.05, 0))

campo.addEntity(quadrato)

quadrato2 = Quadrato(43, (650,650), 0, solidGroup.wood)
quadrato2.setVelocity((-20,-20))
quadrato2.setAcceleration((-0.05, 0))

campo.addEntity(quadrato2)

for i in range (10):
    e = Ball((80 * i, 60 * i), 32, solidGroup.wood)
    e.setVelocity((10,10))
    campo.addEntity(e)

view = View(campo)

running = True

while running:
    campo.move()
    view.draw(campo.entities)
    view.update()
    for event in view.getEvents():
        if event.type == view.QUIT:
            running = False