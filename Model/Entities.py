from .Materials import Solid
import math
from .Utils import Utils
import numpy as np

from icecream import ic
class EntityGroup():
    def __init__(self):
        self._entities = []

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def move(self, deltaTime:float):
        for entity in self._entities:
            entity.move(deltaTime)
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
        self._counter += 1
        #ic(self._counter, self._counter * deltaTime, deltaTime )
        if (self._counter * deltaTime) > 1:
            self._counter = 0
            ic(self._position)

    def _calculateWeight(self):
        return math.pi * self._raggio**2 * self._materiale.density
    
    @property
    def position(self):
        return self._position
    
    @property
    def radius(self):
        return self._raggio
    
    
    
