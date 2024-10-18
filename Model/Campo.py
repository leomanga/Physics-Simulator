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

        self._totalEnergy = 0
        self._composition : Fluid = composition
        self._size = size
        self._spatialGrid = SpatialGrid(size, (5,5), self._entities)
        self._lastTime = None

    def move(self):
        #qua si puo fare di meglio
        if self._lastTime == None:
            self._lastTime = datetime.now()

        newTime = datetime.now()

        deltaTime = newTime - self._lastTime 

        self._lastTime = newTime
        self._entities.move(deltaTime.total_seconds())
        self._spatialGrid.resetGrids()
        self._spatialGrid.populateGrids()
        self._manageCollisions2()

        self._manageBorderCollision()

        self._updateTotalEnergy()

    def _manageCollisions(self):
        for i, entity in enumerate(self._entities):
            for neighbour in self._spatialGrid.getNeighbourEntities(i):
                CollisionManager.manageCollisionFrom(entity, neighbour)

            #self._spatialGrid.clearEntity(i)

    def _manageCollisions2(self):
        numberOfEntities = len(self._entities)
        for i in range(numberOfEntities):

            for j in range(i+1, numberOfEntities):
                CollisionManager.manageCollisionFrom(self._entities[i], self._entities[j])
    
    def _manageBorderCollision(self):
        CollisionManager.manageElementsVsBorderCollisions(self._entities, self._size)

    def addEntity(self, entity):
        self._entities.addEntity(entity)
        self._updateTotalEnergy()
    
    def manageClick(self, point:tuple):
        self._entities.manageClick(Vector(point))

    def _updateTotalEnergy(self):
        self._totalEnergy = self._entities.totalEnergy

    @property
    def entities(self) -> list:
        return self._entities.entities
    
    @property
    def size(self) -> tuple[float, float]:
        return self._size

    @property
    def spatialGrid(self) -> SpatialGrid:
        return self._spatialGrid

    @property
    def totalEnergy(self) -> float:
        return self._totalEnergy
