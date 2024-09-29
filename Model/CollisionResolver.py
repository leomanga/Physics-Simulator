import numpy as np

from .Entities.Ball import Ball
from .Entities.EntityGroup import EntityGroup
from .Entities.Entity import Entity
from .Entities.Polygons import Polygon
from .Utils import Utils
from .ContactInfo import ContactInfo

from icecream import ic

from typing import Union
from .Vector import Vector

class CollisionResolver():
    @staticmethod
    def move(entity: Entity, deltaVector: Vector):
        entity.centerOfMass += deltaVector
        if isinstance(entity, Polygon):
            for i in entity.vertexes:
                i += deltaVector
        
    @staticmethod
    def positionalCorrection(entity1: Entity, entity2: Entity, info: ContactInfo):
        correction = 0.00001 * (entity1.mass * entity2.mass) / (entity1.mass + entity2.mass)
        amountToCorrect = info.penetrationDepth / correction
        correctionVector = info.penetrationNormal * amountToCorrect
        movementOne = (correctionVector / entity1.mass)
        movementTwo = -(correctionVector / entity2.mass)
        CollisionResolver.move(entity1, movementOne)
        CollisionResolver.move(entity2, movementTwo)
 