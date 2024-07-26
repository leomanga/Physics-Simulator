from .Materials import Solid
import math
from .Utils import Utils
import numpy as np

from icecream import ic
class EntityGroup():
    def __init__(self):
        self._entities:list[Entity] = []

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def move(self, deltaTime:float):
        for entity in self._entities:
            entity.move(deltaTime)
        self._checkCollisions()
    
    def _checkCollisions(self):
        numberOfEntities=len(self._entities)
        #migliorini
        for i in range(numberOfEntities):
            for j in range(i+1, numberOfEntities):
                self.separateAxisTheorem(self._entities[i], self._entities[j])
    
    def separateAxisTheorem(self, ent1, ent2):
        pass
        
    @property
    def entities(self):
        return self._entities

class Entity():
    def move(self, deltaTime:float):
        raise NotImplementedError("This method should be overridden by subclass")

    def setVelocity(self, velocity:tuple):
        raise NotImplementedError("This method should be overridden by subclass")
    
    def setAcceleration(self, acceleration:tuple):
        raise NotImplementedError("This method should be overridden by subclass")

    def printItself(self, view):
        raise NotImplementedError("This method should be overridden by subclass")

class Ball(Entity):
    def __init__(self, position:tuple, raggio:int, materiale:Solid):
        # position identify the center of the ball
        self._position = np.array(position)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))

        self._raggio : int = raggio
        self._materiale : Solid = materiale

        self._weight : float = self._calculateWeight()

    def move(self, deltaTime:float):
            self._velocity = self._velocity + (self._acceleration * deltaTime)
            self._position = self._position + (self._velocity * deltaTime)

    def setPosition(self, position:tuple):
        self._position = np.array(position)

    def setVelocity(self, velocity:tuple):
        self._velocity = np.array(velocity)
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = np.array(acceleration)

    def printItself(self, view):
        view.drawCircle(self._position, self._raggio)   

    def _calculateWeight(self):
        return math.pi * self._raggio**2 * self._materiale.density
    
    @property
    def position(self):
        return self._position
    
    @property
    def radius(self):
        return self._raggio
    
class Quadrato():
    def __init__(self, length, mainVertex: tuple, rotation, material: Solid ):
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
        vector2 = np.array((Utils.cos(self._rotation), Utils.sin(self._rotation)))*self._length
        vector4 = np.array((-Utils.sin(self._rotation), Utils.cos(self._rotation)))*self._length
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

    def move(self, deltaTime:float):
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
