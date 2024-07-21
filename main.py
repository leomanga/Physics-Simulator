from View.View import View
from Model.Campo import Campo

from Model.Materials import FluidGroup
from Model.Materials import SolidGroup

from Model.Entities import Ball

size = (400, 400)
campo = Campo(FluidGroup.air, size)

palla = Ball((200,200), 20, SolidGroup.wood)

palla.setVelocity((2,1))
palla.setAcceleration((-0.5, -0.2))

campo.addEntity()

view = View(campo)
view.start()