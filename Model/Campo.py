from .Materials import Fluid
from .Entities.EntityGroup import EntityGroup
from .Vector import Vector
from .CollisionDetector import CollisionManager

from datetime import datetime
import time
class Campo():
    def __init__(self, composition: Fluid, size:tuple):
        self._entities : EntityGroup = EntityGroup()# CLASSE

        self._composition : Fluid = composition
        self._size = size

        self._lastTime = None

    def move(self):
        #qua si puo fare di meglio
        if self._lastTime == None:
            self._lastTime = datetime.now()

        newTime = datetime.now()

        deltaTime = newTime - self._lastTime 

        self._lastTime = newTime

        self._entities.move(deltaTime.total_seconds())
        self._entities.manageCollisions()

        self._manageBorderCollision()

    def _manageBorderCollision(self):
        CollisionManager.manageElementsVsBorderCollisions(self._entities, self._size)

    def addEntity(self, entity):
        self._entities.addEntity(entity)
    
    def manageClick(self, point:tuple):
        self._entities.manageClick(Vector(point))

    @property
    def entities(self) -> list:
        return self._entities.entities
    
    @property
    def size(self):
        return self._size

