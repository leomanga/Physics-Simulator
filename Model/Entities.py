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
        numberOfEntities = len(self._entities)
        #migliorini
        tasks = []
        for i in range(numberOfEntities):
            for j in range(i+1, numberOfEntities):
                tasks.append(self._manageCollisionFrom(self._entities[i], self._entities[j]))

        Utils.runAsyncTasks(self._loop, tasks)

    async def _manageCollisionFrom(self, entity1:"Entity", entity2:"Entity"):
        collide = self._areColliding(entity1, entity2)
        if collide:
            #collision(self._entities[i], self._entities[j], pointOfCOllision)
            entity1.setVelocity(entity1.velocity * -1)
            entity1.setAcceleration(entity1.acceleration * -1)
            entity2.setVelocity(entity2.velocity * -1)
            entity2.setAcceleration(entity2.acceleration * -1)

    def _areColliding(self, ent1:"Entity", ent2:"Entity"): #usiamo Separate Axis Theorem
        length1 = len(ent1.vertexes) #gestire cerchio
        length2 = len(ent2.vertexes)
        for i in range(length1):
            direction = ent1.vertexes[i]-ent1.vertexes[(i+1)%length1]
            projection1 = Utils.ProjectEntityVertexes(direction, ent1.vertexes)
            projection2 = Utils.ProjectEntityVertexes(direction, ent2.vertexes)
            if not Utils.checkOverlap(projection1, projection2):
                return False
            
        for i in range(length2):
            direction = ent2.vertexes[i]-ent2.vertexes[(i+1)%length2]
            projection1 = Utils.ProjectEntityVertexes(direction, ent1.vertexes)
            projection2 = Utils.ProjectEntityVertexes(direction, ent2.vertexes)
            if not Utils.checkOverlap(projection1, projection2):
                return False
            
        return True
    
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
class Quadrato():
    def __init__(self, length, mainVertex: tuple, rotation, material: Solid ):
        self._id = Entity.id
        Entity.id += 1 
    
        self._mainVertex = np.array(mainVertex)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))
        
        self._length = length
        self._rotation = rotation
        
        self._vertexes = [self._mainVertex]
        self._initVertexes()
        
        self._material = material
        self._weight : float = self._calculateWeight()

        self._counter=0
    
    def _initVertexes(self):
        # calculating vectors by rotation and length
        side1 = Utils.cos(self._rotation) * self._length
        side2 = Utils.sin(self._rotation) * self._length
        
        vector2 = np.array((side1, side2))
        vector4 = np.array((-side2, side1))
        vector3 = vector2+vector4

        vector2Traslated = Utils.traslateVector(self._mainVertex, vector2)
        vector3Traslated = Utils.traslateVector(self._mainVertex, vector3)
        vector4Traslated = Utils.traslateVector(self._mainVertex, vector4)
        
        # the append order is important for printing the Quadrato on the view
        self._vertexes.append(vector2Traslated)
        self._vertexes.append(vector3Traslated)
        self._vertexes.append(vector4Traslated)

    def setVelocity(self, velocity:tuple):
        self._velocity = np.array(velocity)
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = np.array(acceleration)

    async def move(self, deltaTime:float):
        self._velocity = self._velocity + (self._acceleration * deltaTime)
        for i in range(len(self._vertexes)):
            self._vertexes[i] = self._vertexes[i] + self._velocity * deltaTime           
            
    def printItself(self, view):
        listVertexes=[tuple(vertex) for vertex in self._vertexes]
        view.drawPolygon(listVertexes)   

    def _calculateWeight(self):
        """
        TODO
        """
        pass 
    
    @property
    def vertexes(self) -> list[np.ndarray]:
        return self._vertexes
    
    @property    
    def velocity(self):
        return self._velocity
    
    @property
    def acceleration(self):
        return self._acceleration
    
    @property
    def id(self):
        return self._id