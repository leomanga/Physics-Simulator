from .Materials import Solid
import math
from .Utils import Utils
import numpy as np
from numpy import _ArrayOrScalarCommon

from icecream import ic
class EntityGroup():
    def __init__(self):
        self._entities = []

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

class Ball():
    def __init__(self, position:tuple, raggio:int, materiale:Solid):
        self._position = np.array(position)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))

        self._raggio : int = raggio
        self._materiale : Solid = materiale

        self._weight : float = self._calculateWeight()

        #TEST
        self._counter = 0

    def setPosition(self, position:tuple):
        self._position = np.array(position)

    def setVelocity(self, velocity:tuple):
        self._velocity = np.array(velocity)
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = np.array(acceleration)

    def move(self, deltaTime:float):
        #vedere come fare meglio
        self._velocity = self._velocity + (self._acceleration * deltaTime)

        self._position = self._position + (self._velocity * deltaTime)

        # TEST   
        self._counter = 0
        #ic(self._counter, self._counter * deltaTime, deltaTime )
        if (self._counter * deltaTime) > 1:
            self._counter = 0
            ic(self._position)

    def _calculateWeight(self):
        return math.pi * self._raggio**2 * self._materiale.density
    
    def printItself(self, view):
        view.drawCircle(self._position, self._raggio)    
    
    @property
    def position(self):
        return self._position
    
    @property
    def radius(self):
        return self._raggio
    
class Quadrato():
    def __init__(self, length, mainVertex: tuple, rotation, material: Solid ):
        self._mainVertex= np.array(mainVertex)
        self._velocity = np.array((0,0))
        self._acceleration = np.array((0,0))
        
        self._length= length
        self._rotation= rotation
        
        self._vertexes=[self._mainVertex]
        self._initVertexes()
        
        self._material = material
        self._counter=0
    
    def _initVertexes (self):
        vector2 = np.array((math.cos(self._rotation), math.sin(self._rotation)))*self._length
        vector4 = np.array((-math.sin(self._rotation), math.cos(self._rotation)))*self._length
        vector3 = vector2+vector4
        self._vertexes.append(self._traslation(self._mainVertex, vector2))
        self._vertexes.append(self._traslation(self._mainVertex, vector3))
        self._vertexes.append(self._traslation(self._mainVertex, vector4))
    
    def _traslation(self, v1, traslVector):
        return v1 + traslVector

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
    
    @property
    def vertexes(self) -> list[_ArrayOrScalarCommon]:
        return self._vertexes
