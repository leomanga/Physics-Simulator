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

    def __repr__(self):
        return f"Ball, {super().__repr__()}"  
     
    def __str__(self):
        return f"Ball, {super().__str__()}"
    
    async def move(self, deltaTime:float):
        self._updateMotions(deltaTime)
        self._boundingBox.setBallBox(self._centerOfMass, self.radius)

    def printItself(self, view, debug = False):
        color = view.baseColor if self._selected == False else view.clickedColor
        view.drawCircle(tuple(self._centerOfMass), self._radius, color)   

        vector = self._centerOfMass + Vector((self._radius, 0))
        directionVector = Utils.rotate(vector, self._centerOfMass, self._rotation)
        view.drawLine(self._centerOfMass, directionVector, (0,0,0))
        
        if debug:
            view.drawBoundingBox(self._boundingBox)

        super().printItself(view, debug)
            
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
