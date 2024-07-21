from Materials import Solid
import math
from Utils import Utils

class EntityGroup():
    def __init__(self):
        self._entities = []

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def move(self):
        for entity in self._entities():
            entity.move()
            print(entity.position)

class Ball():
    def __init__(self, centro:tuple, raggio:int, materiale:Solid):
        self._centro : tuple = centro
        self._raggio : int = raggio
        self._materiale : Solid = materiale

        self._weight : float = self._calculateWeight()

        self._position : tuple = (0,0) 
        self._velocity : tuple = (0,0)
        self._acceleration : tuple = (0,0)

    def setPosition(self, position:tuple):
        self._position = position

    def setVelocity(self, velocity:tuple):
        self._velocity = velocity
    
    def setAcceleration(self, acceleration:tuple):
        self._acceleration = acceleration

    def move(self):
        #vedere come fare meglio
        self._velocity = Utils.sumVec(self._velocity, self._acceleration)

        self._position = Utils.sumVec(self._position, self._velocity)

    def _calculateWeight(self):
        return math.pi * self._raggio**2 * self._materiale.density
    
    @property
    def position(self):
        return self._position
    
