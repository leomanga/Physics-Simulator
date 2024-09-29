from .Materials import Fluid
from .Entities.EntityGroup import EntityGroup
from .Vector import Vector
from .CollisionDetector import CollisionManager
from .SpatialGrid import SpatialGrid

from datetime import datetime
import time
from icecream import ic
class Campo():
    def __init__(self, composition: Fluid, size:tuple):
        self._entities : EntityGroup = EntityGroup()# CLASSE

        self._composition : Fluid = composition
        self._size = size
        self._spatialGrid = SpatialGrid(size, (7,5), self._entities)
        self._lastTime = None

    def move(self):
        #qua si puo fare di meglio
        if self._lastTime == None:
            self._lastTime = datetime.now()

        newTime = datetime.now()

        deltaTime = newTime - self._lastTime 

        self._lastTime = newTime
        self._entities.move(deltaTime.total_seconds())
        self._spatialGrid._resetGrids()
        self._spatialGrid._populateGrids()
        self._manageCollisions()
        #self._entities.manageCollisions()

        self._manageBorderCollision()

    def _manageCollisions(self):
        for entities in self._spatialGrid._grids:
            for i in range(len(entities)):
                for j in range(i+1, len(entities)):
                    CollisionManager.manageCollisionFrom(entities[i], entities[j])

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
    def size(self) -> tuple[float, float]:
        return self._size

    @property
    def spatialGrid(self) -> SpatialGrid:
        return self._spatialGrid

