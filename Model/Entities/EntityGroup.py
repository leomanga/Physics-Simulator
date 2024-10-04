from ..Vector import Vector
from Model.Entities.Entity import Entity
from Model.Entities.Polygons import Polygon

from icecream import ic

class EntityGroup():
    def __init__(self):
        self._entities:list[Entity] = []
    
    def __getitem__(self, index) -> Entity:
        return self._entities[index]

    def __iter__(self):
        return iter(self._entities)

    def __len__(self):
        return len(self._entities)

    def __repr__(self):
        return repr(self._entities)

    def addEntity(self, entity):
        self._entities.append(entity)
    
    def manageClick(self, point:Vector):
        from Model.CollisionDetector import CollisionManager
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
        for entity in self._entities:
            entity.move(deltaTime)
    
    @property
    def entities(self) -> list["Entity"]:
        return self._entities