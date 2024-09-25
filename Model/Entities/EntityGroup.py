import asyncio

from ..Utils import Utils
from ..Vector import Vector
from Model.Entities.Entity import Entity
from Model.Entities.Polygons import Polygon

from icecream import ic

class EntityGroup():
    def __init__(self):
        self._entities:list[Entity] = []
        
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
    
    def __getitem__(self, index):
        return self._entities[index]

    def __len__(self):
        return len(self._entities)

    def __repr__(self):
        return repr(self._entities)

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def manageClick(self, point:Vector):
        from ..Collisions import CollisionManager
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
    
    def manageCollisions(self):
        from ..Collisions import CollisionManager
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