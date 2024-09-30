from ..Materials import Solid
from ..Vector import Vector, VectorZero
from Model.Entities.BoundingBox import BoundingBox
from icecream import ic

class Entity():
    idCounter: int = 0
    def __init__(self, rotation, material):
        self._id = Entity.idCounter
        Entity.idCounter += 1

        self._centerOfMass: Vector = None
        self._velocity: Vector = Vector((0,0))
        self._acceleration: Vector = Vector((0,0))
        self._angularVelocity: float = 0
        self._angularAccelleration: float = 0

        self._rotation: float = rotation

        self._material: Solid = material

        self._area: float = None
        self._mass: float = None
        self._inertia: float = None

        self._contactPoint: Vector = None
        self._boundingBox: BoundingBox = BoundingBox()

        self._selected: bool = False
    
    def __repr__(self) -> str:
        return f"id:{self._id}, center of mass:{self._centerOfMass}"

    def __str__(self) -> str:
        return f"id:{self._id}"
            
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
    
    def addForce(self, force: Vector):
        self._acceleration += force / self._mass

    def stopMotion(self):
        self._acceleration = VectorZero()
        self._velocity = VectorZero()
        self._angularAccelleration = 0
        self._angularVelocity = 0
    
    def printItself(self, view, debug = False):
        if debug:
            view.drawText(round(self._mass), tuple(self._centerOfMass))
            if self._contactPoint is not None:
                view.drawPoint(tuple(self._contactPoint))

    def _updateMotions(self, deltaTime: float):
        self._velocity += self._acceleration * deltaTime
        self._centerOfMass += self._velocity * deltaTime

        self._angularVelocity += (self._angularAccelleration * deltaTime)
        self._rotation += (self._angularVelocity * deltaTime)
    
    def _initMass(self):
        self._mass = self._area * self._material.density 

    async def move(self, deltaTime: float):
        raise NotImplementedError("This method should be overridden by subclass")

    def _calculateArea(self):
       raise NotImplementedError("This method should be overridden by subclass") 

    @property
    def id(self) -> int:
        return self._id

    @property
    def mass(self) -> float:
        return self._mass
    
    @property
    def velocity(self) -> Vector:
        return self._velocity
    
    @velocity.setter
    def velocity(self, new):
        self._velocity = new
    
    @property
    def angularVelocity(self) -> float:
        return self._angularVelocity
    
    @angularVelocity.setter
    def angularVelocity(self, new):
        self._angularVelocity = new

    @property
    def acceleration(self) -> Vector:
        return self._acceleration
    
    @property
    def angularAcceleration(self) -> float:
        return self._angularAccelleration

    @property
    def selected(self) -> bool:
        return self._selected

    @property
    def centerOfMass(self) -> Vector:
        return self._centerOfMass
    
    @centerOfMass.setter
    def centerOfMass(self, value):
        self._centerOfMass = value
    
    @property
    def boundingBox(self) -> BoundingBox:
        return self._boundingBox