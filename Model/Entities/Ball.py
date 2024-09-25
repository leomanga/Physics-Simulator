import math

from ..Materials import Solid
from ..Utils import Utils
from ..Vector import Vector
from Model.Entities.Entity import Entity

from icecream import ic

class Ball(Entity):
    def __init__(self, center:tuple, raggio:int, material:Solid):
        super().__init__(0, material)
        # position identify the center of the ball
        self._centerOfMass = Vector(center)

        self._radius : int = raggio

        self._initArea()
        self._initMass()
        self._initInertia()

    async def move(self, deltaTime:float):
            self._updateMotions(deltaTime)

    def setPosition(self, position:tuple):
        self._centerOfMass = Vector(position)

    def printItself(self, view):
        color = view.baseColor if self._selected == False else view.clickedColor
        view.drawCircle(tuple(self._centerOfMass), self._radius, color)   

        vector = self._centerOfMass + Vector((self._radius, 0))
        directionVector = Utils.rotate(vector, self._centerOfMass, self._rotation)
        view.drawLine(self._centerOfMass, directionVector, (0,0,0))

        super().printItself(view)
            
    def _initArea(self):
        self._area = math.pi * self._radius**2
        
    def _initInertia(self):
        self._inertia = 0.5* self._mass* self._radius * self._radius

    @property
    def position(self) -> Vector:
        return self._centerOfMass
    
    @property
    def radius(self) -> int | float:
        return self._radius
