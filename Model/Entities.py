from .Materials import Solid
import math
from .Utils import Utils
import numpy as np
import asyncio


from icecream import ic
class EntityGroup():
    def __init__(self):
        self._entities:list[Entity] = []
        
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def addEntity(self, entity):
        self._entities.append(entity)
    
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
            for j in range(i+1, numberOfEntities):
                tasks.append(CollisionManager.manageCollisionFrom(self._entities[i], self._entities[j]))

        Utils.runAsyncTasks(self._loop, tasks)
    
    @property
    def entities(self) -> list["Entity"]:
        return self._entities

class Entity():
    id = 0
    async def move(self, deltaTime:float):
        raise NotImplementedError("This method should be overridden by subclass")

    def setVelocity(self, velocity:tuple):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def setAcceleration(self, acceleration:tuple):
        raise NotImplementedError("This method should be overridden by subclass")

    def printItself(self, view):
        raise NotImplementedError("This method should be overridden by subclass")
    
    @property
    def vertexes(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
    @property
    def velocity(self):
        raise NotImplementedError("This method should be overridden by subclass")

    @property
    def acceleration(self):
        raise NotImplementedError("This method should be overridden by subclass")
    
class Polygon(Entity):
    def _calculateArea(self):
       raise NotImplementedError("This method should be overridden by subclass")
    
    def _calculateCentroid(self):
        pass

    def _calculateNormals(self, normalLength:int = 15):
        length = len(self._vertexes)
        for i in range(length):
            direction : np.array = self.vertexes[i] - self.vertexes[(i + 1) % length]
            directionVersor = direction / math.sqrt(direction[0] ** 2 + direction[1] ** 2) * -normalLength
            normalX = directionVersor[1]
            normalY = - directionVersor[0]

            self._normals.append(np.array((normalX, normalY)))

    def printItself(self, view):
        listVertexes=[tuple(vertex) for vertex in self._vertexes]
        view.drawPolygon(listVertexes)   
        length = len(self._normals)
        for i in range(length):
            startingPoint = self._calculateMidPoint(self.vertexes[i], self.vertexes[(i + 1) % length])            
            view.drawLine(tuple(startingPoint), tuple(startingPoint + self._normals[i]))
        
        if self._contactPoint is not None:
            view.drawPoint(tuple(self._contactPoint))

    def _calculateMidPoint(self, vec1:np.ndarray, vec2:np.ndarray) -> np.ndarray:
        return vec1 + (vec2 - vec1) / 2 
        
class RegularPolygon(Polygon):
    def __init__(self, length, centerOfMass: tuple, rotation, numberOfSides, material: Solid):
        self._id = Entity.id
        Entity.id += 1 
    
        self._centerOfMass = np.array(centerOfMass)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))
        
        self._length = length
        self._rotation = rotation
        
        self._numberOfSides = numberOfSides
        self._vertexes = []
        self._apothem = self._calculateApothem()
        self._area = self._calculateArea()
        self._initVertexes()
        
        self._normals = []
        self._calculateNormals()
        
        self._material = material
        self._weight : float = self._calculateWeight()

        self._counter=0

        self._contactPoint = None
    
    def _initVertexes(self):
        angles = np.linspace(math.radians(self._rotation), 2*np.pi + math.radians(self._rotation), self._numberOfSides, endpoint=False)
        x=self._apothem*np.cos(angles)
        y=self._apothem*np.sin(angles)
        xOffset=x+self._centerOfMass[0]
        yOffset=y+self._centerOfMass[1]
        for i in range(self._numberOfSides):
            self._vertexes.append(np.array((xOffset[i], yOffset[i])))    
    

    def setVelocity(self, velocity:tuple):
        self._velocity = np.array(velocity)
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = np.array(acceleration)

    async def move(self, deltaTime:float):
        self._velocity = self._velocity + (self._acceleration * deltaTime)
        for i in range(len(self._vertexes)):
            self._vertexes[i] = self._vertexes[i] + self._velocity * deltaTime           

        """       
        def printItself(self, view):
            listVertexes=[tuple(vertex) for vertex in self._vertexes]
            view.drawPolygon(listVertexes)   
            for i in range(len(self._normals)):
                view.drawVector()"""

    def _calculateWeight(self):
        """
        TODO
        """
        pass 
    
    def _calculateArea(self):
        perimeter = self._length*self._numberOfSides
        return 0.5*self._apothem*perimeter

    def _calculateApothem(self):
        return (self._length/2)/Utils.sin(180/self._numberOfSides)
    
    def setContactPoint(self, contactPoint):
        self._contactPoint = contactPoint    
    
    @property
    def vertexes(self) -> list[np.ndarray]:
        return self._vertexes
    
    @property
    def normals(self) -> list[np.ndarray]:
        return self._normals
    
    @property    
    def velocity(self):
        return self._velocity
    
    @property
    def acceleration(self):
        return self._acceleration
    
    @property
    def id(self):
        return self._id
    
    @property
    def numberOfSides(self):
        return self._numberOfSides
    
class Ball(Entity):
    def __init__(self, position:tuple, raggio:int, materiale:Solid):
        self._id = Entity.id
        Entity.id += 1
    
        # position identify the center of the ball
        self._position = np.array(position)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))
        self._numberOfSides = 16

        self._raggio : int = raggio
        self._vertexes : list[np.ndarray] = []
        self._initVertexes()
        
        self._materiale : Solid = materiale

        self._weight : float = self._calculateWeight()



    async def move(self, deltaTime:float):
            self._velocity = self._velocity + (self._acceleration * deltaTime)
            deltaPosition = self._velocity * deltaTime
            self._position = self._position + (deltaPosition)
            for i in range(self._numberOfSides):
                self._vertexes[i] = self._vertexes[i] + deltaPosition
            

    def setPosition(self, position:tuple):
        self._position = np.array(position)

    def setVelocity(self, velocity:tuple):
        self._velocity = np.array(velocity)
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = np.array(acceleration)

    def printItself(self, view):
        view.drawCircle(self._position, self._raggio)   
        """listVertexes=[tuple(vertex) for vertex in self._vertexes]
        view.drawPolygon(listVertexes)  """

    def _calculateWeight(self):
        return math.pi * self._raggio**2 * self._materiale.density
    
    def _initVertexes(self):
        angles = np.linspace(0, 2*np.pi, self._numberOfSides, endpoint=False)
        x=self._raggio*np.cos(angles)
        y=self._raggio*np.sin(angles)
        xOffset=x+self._position[0]
        yOffset=y+self._position[1]
        for i in range(self._numberOfSides):
            self._vertexes.append(np.array((xOffset[i], yOffset[i])))    
    
    @property
    def vertexes(self) -> list[np.ndarray]:
        return self._vertexes

    @property
    def position(self):
        return self._position
    
    @property
    def radius(self):
        return self._raggio
    
    @property
    def velocity(self):
        return self._velocity
    
    @property
    def acceleration(self):
        return self._acceleration

    @property
    def id(self):
        return self._id  
