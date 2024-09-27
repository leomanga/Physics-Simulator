from ..Materials import Solid
from ..Vector import Vector, VectorZero

from icecream import ic

class Entity():
    id: int = 0
    def __init__(self, rotation, material):
        self._id = Entity.id
        Entity.id += 1

        self._centerOfMass: Vector = None
        self._velocity: Vector = Vector((0,0))
        self._acceleration: Vector = Vector((0,0))
        self._angularVelocity: int = 0
        self._angularAccelleration: int = 0

        self._rotation: int = rotation

        self._material: Solid = material

        self._area: float = None
        self._mass: float = None
        self._inertia: float = None

        self._contactPoint: Vector = None

        self._selected: bool = False
            
    def clicked(self):
        self._selected = not self._selected
    
    def setVelocity(self, velocity:tuple):
        self._velocity = Vector(velocity)
        
    def setAngularVelocity(self, angVelocity:int):
        self._angularVelocity = angVelocity

    def setAcceleration(self, acceleration:tuple):
        self._acceleration = Vector(acceleration)
    
    def setAngularAcceleration(self, angAcceleration:int):
        self._angularAccelleration = angAcceleration
       
    def setContactPoint(self, contactPoint:Vector):
        self._contactPoint = contactPoint   
    
    def stopMotion(self):
        self._acceleration = VectorZero()
        self._velocity = VectorZero()
        self._angularAccelleration = 0
        self._angularVelocity = 0
    
    def printItself(self, view):
        view.drawText(round(self._mass), tuple(self._centerOfMass))
        if self._contactPoint is not None:
            view.drawPoint(tuple(self._contactPoint))

    def _updateMotions(self, deltaTime: float):
        self._angularVelocity = self._angularVelocity + (self._angularAccelleration * deltaTime)
        self._rotation = self._rotation + self._angularVelocity * deltaTime

        self._velocity = self._velocity + (self._acceleration * deltaTime)
        self._centerOfMass = self._centerOfMass + self._velocity * deltaTime   
    
    def _initMass(self):
        self._mass = self._area * self._material.density 

    async def move(self, deltaTime:float):
        raise NotImplementedError("This method should be overridden by subclass")

    def _calculateArea(self):
       raise NotImplementedError("This method should be overridden by subclass") 

    @property
    def velocity(self):
        return self._velocity
    
    @property
    def angularVelocity(self):
        return self._angularVelocity

    @property
    def acceleration(self):
        return self._acceleration
    
    @property
    def angularAcceleration(self):
        return self._angularAccelleration

    @property
    def selected(self):
        return self._selected

    @property
    def centerOfMass(self):
        return self._centerOfMass