
from Entities import EntityGroup
from Materials import Fluid

class Campo():
    def __init__(self, composition: Fluid, size:tuple):
        self._entities : EntityGroup = EntityGroup()# CLASSE

        self._composition : Fluid = composition
        self._size = size

    def move(self):
        self._entities.move()

    def addEntity(self, entity):
        self._entities.addEntity(entity)

    def _checkCollision(self):
        pass
    
    @property
    def size(self):
        return self._size

c = Campo()