from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup
from Model.Materials import SolidGroup

from Model.Entities import Ball

fluidGroup = FluidGroup()
solidGroup = SolidGroup()

size = (400, 400)
campo = Campo(fluidGroup.air, size)

palla = Ball((200,200), 20, solidGroup.wood)

palla.setVelocity((2,1))
palla.setAcceleration((-0.5, -0.2))

campo.addEntity(palla)

view = View(campo)
view.start()