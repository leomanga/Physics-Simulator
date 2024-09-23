from .Materials import Solid
import math
from .Utils import Utils
import numpy as np
import asyncio

from .Vector import Vector
from .Vector import VectorZero

from icecream import ic
class EntityGroup():
    def __init__(self):
        self._entities:list[Entity] = []
        
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def manageClick(self, point:Vector):
        from .Collisions import CollisionManager
        entitySelected = False
        for entity in self._entities:
            result = CollisionManager.isPointInsideEntity(point, entity)
            if result == True:
                entity.clicked()
                entitySelected = True
        
        if not entitySelected:
            for entity in self._entities:
                if entity.selected:
                    velocity = point - entity.centerOfMass
                    entity.setVelocity(entity.velocity + velocity)
            
    def move(self, deltaTime:float):
        tasks = [entity.move(deltaTime) for entity in self._entities]
        Utils.runAsyncTasks(self._loop, tasks)
  
        self._manageCollisions()
    
    def _manageCollisions(self):
        from .Collisions import CollisionManager
        numberOfEntities = len(self._entities)
        #migliorini
        tasks = []
        for i in range(numberOfEntities):
            
            if isinstance(self._entities[i], Polygon):
                self._entities[i].setContactPoint(None)

            for j in range(i+1, numberOfEntities):
                tasks.append(CollisionManager.manageCollisionFrom(self._entities[i], self._entities[j]))

        Utils.runAsyncTasks(self._loop, tasks)
    
    @property
    def entities(self) -> list["Entity"]:
        return self._entities

class Entity():
    id: int = 0
    def __init__(self, rotation, material):
        self._id = Entity.id
        Entity.id += 1

        self._centerOfMass: Vector = None
        self._velocity: Vector = Vector((0,0))
        self._angularVelocity: int = 0
        self._angularAccelleration: int = 0
        self._acceleration: Vector = Vector((0,0))

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
    
    def _initMass(self):
        self._mass = self._area * self._material.density 

    async def move(self, deltaTime:float):
        raise NotImplementedError("This method should be overridden by subclass")

    def printItself(self, view):
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
    
class Polygon(Entity):
    def __init__(self, rotation, material):
        super().__init__(rotation, material)
        
        self._numberOfSides: int = None

        self._vertexes: list[Vector] = []
        self._normals: list[Vector] = []
        
        self._sidesLength: list[float] = []
        
    async def move(self, deltaTime:float):
        self._velocity = self._velocity + (self._acceleration * deltaTime)
        self._angularVelocity = self._angularVelocity + (self._angularAccelleration * deltaTime)
        for i in range(self._numberOfSides):
            self._vertexes[i] = Utils.rotate (self._vertexes[i], self._centerOfMass, self._angularVelocity * deltaTime)
            self._normals[i] = Utils.rotate (self._normals[i], VectorZero(), self._angularVelocity * deltaTime)
            self._vertexes[i] = self._vertexes[i] + self._velocity * deltaTime
            

        self._centerOfMass = self._centerOfMass + self._velocity * deltaTime          

    def printItself(self, view):
        listVertexes=[tuple(vertex) for vertex in self._vertexes]
        color = view.baseColor if self._selected == False else view.clickedColor
        view.drawPolygon(listVertexes, color)   
        length = len(self._normals)
        view.drawText(round(self._mass), tuple(self._centerOfMass))
        for i in range(length):
            startingPoint = self._calculateMidPoint(self.vertexes[i], self.vertexes[(i + 1) % length])            
            view.drawLine(tuple(startingPoint), tuple((startingPoint + self._normals[i]*15)))
            view.drawText(i, tuple(self.vertexes[i]))
        
        if self._contactPoint is not None: 
            view.drawPoint(tuple(self._contactPoint)) 

    def _calculateNormals(self):
        length = len(self._vertexes)
        for i in range(length):
            direction : Vector = self.vertexes[i] - self.vertexes[(i + 1) % length]
            directionVersor = direction / math.sqrt(direction[0] ** 2 + direction[1] ** 2) * -1
            normalX = directionVersor[1]
            normalY = - directionVersor[0]

            self._normals.append(Vector((normalX, normalY)))

    def _calculateMidPoint(self, vec1:Vector, vec2:Vector) -> Vector:
        return vec1 + (vec2 - vec1) / 2 
    
    def _initSidesLength(self):
        for i in range(self._numberOfSides):
             direction: Vector = self.vertexes[(i+1) % self._numberOfSides] - self.vertexes[i]
             self._sidesLength.append(direction.norm)
    
    def _initArea(self, shape):
        self._area = 0
        for i in range(self._numberOfSides):
            self._area += shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0]
        self._area /= 2
        
    def _initInertia(self):
        self._inertia = 0
        massPerTriangle = self._mass / self._numberOfSides
        for i in range(self._numberOfSides):
            centerToVertice1 = self._vertexes[i] - self._centerOfMass
            centerToVertice2 = self._vertexes[(i+1)%self._numberOfSides] - self._centerOfMass
            self._inertia += massPerTriangle * (centerToVertice1.norm + centerToVertice2.norm + centerToVertice1 * centerToVertice2) / 6
            

        
        
    @property
    def vertexes(self) -> list[Vector]:
        return self._vertexes
    
    @property
    def normals(self) -> list[Vector]:
        return self._normals
    
    @property
    def numberOfSides(self):
        return self._numberOfSides
    
    @property
    def sidesLength(self):
        return self._sidesLength
    

class IrregularPolygon(Polygon):
    def __init__(self ,shape: list[tuple], centerOfMass: tuple, rotation, material):
        super().__init__(rotation, material)
        self._numberOfSides = len(shape)
        self._centerOfMass = Vector(centerOfMass)
        
        self._initArea(shape)
        self._initVertexes(shape)
        self._calculateNormals()
        self._initSidesLength()
        self._initMass()
        self._initInertia()
        
    def _initVertexes(self, shape):
        centroid = self._getCentroid(shape)
        offset = self._centerOfMass - centroid
        for i in range(self._numberOfSides):
            self._vertexes.append(Vector(shape[i])+ offset)
    
    def _getCentroid(self, shape):
        if self._area == None:
            self._initArea()
        cx = 0
        cy = 0 
        for i in range(self._numberOfSides):
            cx += (shape[i][0] + shape [(i+1)% self._numberOfSides][0])*(shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0])
            cy += (shape[i][1] + shape [(i+1)% self._numberOfSides][1])*(shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0])
        cx /= 6*self._area
        cy /= 6*self._area
        return Vector((cx, cy))
        
    
class RegularPolygon(Polygon):
    def __init__(self, sideLength, centerOfMass: tuple, rotation, numberOfSides, material: Solid):
        super().__init__(rotation, material)
        
        self._sideLength = sideLength
        self._centerOfMass = Vector(centerOfMass)

        self._numberOfSides = numberOfSides

        self._apothem = self._calculateApothem()
        
        self._initVertexes()
        self._initArea(self._vertexes)
                
        self._material:Solid = material
        
        self._calculateNormals()
        self._initSidesLength()
        self._initMass()
        self._initInertia()
    
    def _initVertexes(self):
        angles = np.linspace(math.radians(self._rotation), 2*np.pi + math.radians(self._rotation), self._numberOfSides, endpoint=False)
        x:list =self._apothem*np.cos(angles)
        y:list =self._apothem*np.sin(angles)
        xOffset:list =x+self._centerOfMass[0]
        yOffset:list =y+self._centerOfMass[1]

        for i in range(self._numberOfSides):
            self._vertexes.append(Vector((xOffset[i], yOffset[i])))    

    """def _calculateArea(self):
        perimeter = self._sideLength*self._numberOfSides
        return 0.5*self._apothem*perimeter"""

    def _calculateApothem(self):
        return (self._sideLength/2)/Utils.sin(180/self._numberOfSides)

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
            self._velocity = self._velocity + (self._acceleration * deltaTime)
            deltaPosition = self._velocity * deltaTime
            self._centerOfMass = self._centerOfMass + deltaPosition      

    def setPosition(self, position:tuple):
        self._centerOfMass = Vector(position)

    def printItself(self, view):
        color = view.baseColor if self._selected == False else view.clickedColor
        view.drawCircle(tuple(self._centerOfMass), self._radius, color)   
        view.drawText(round(self._mass), tuple(self._centerOfMass))
        if self._contactPoint is not None:
            view.drawPoint(tuple(self._contactPoint))
            
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
