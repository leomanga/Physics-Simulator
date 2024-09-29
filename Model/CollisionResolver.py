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
        correction = 0.1 * (entity1.mass * entity2.mass) / (entity1.mass + entity2.mass)
        amountToCorrect = info.penetrationDepth / correction
        correctionVector = info.penetrationNormal * amountToCorrect
        movementOne = (correctionVector / entity1.mass)
        movementTwo = -(correctionVector / entity2.mass)
        CollisionResolver.move(entity1, movementOne)
        CollisionResolver.move(entity2, movementTwo)
        
    @staticmethod
    def manageImpulse(entity1: Entity, entity2: Entity, info: ContactInfo):
        penetrationToCentroidA = info.penetrationPoint - entity1.centerOfMass
        penetrationToCentroidB = info.penetrationPoint - entity2.centerOfMass
        angularVelocityToA = Vector((-(entity1.angularVelocity*penetrationToCentroidA[1]), entity1.angularVelocity*penetrationToCentroidA[0]))
        angularVelocityToB = Vector((-(entity2.angularVelocity*penetrationToCentroidB[1]), entity2.angularVelocity*penetrationToCentroidB[0]))
        relativeVelocityA = entity1.velocity + angularVelocityToA
        relativeVelocityB = entity2.velocity + angularVelocityToB
        relativeVelocityNormal = (relativeVelocityA - relativeVelocityB)*info.penetrationNormal
        if relativeVelocityNormal > 0:
            return
        e = -0.5 #add bounciness
        pToCentroidCrossNormalA = penetrationToCentroidA.cross(info.penetrationNormal)
        pToCentroidCrossNormalB = penetrationToCentroidB.cross(info.penetrationNormal)
        invMassSum = (entity1.mass + entity1.mass) / (entity1.mass * entity2.mass)
        crossNsum = pToCentroidCrossNormalA * pToCentroidCrossNormalA / entity1._inertia + pToCentroidCrossNormalB * pToCentroidCrossNormalB / entity2._inertia
        j = (-(1+e)*relativeVelocityNormal) / (invMassSum + crossNsum)
        impulseVector = info.penetrationNormal * j
        entity1.velocity -= impulseVector / entity1.mass
        entity2.velocity -= impulseVector / entity2.mass
        entity1.angularVelocity -= pToCentroidCrossNormalA * j / entity1._inertia #add property
        entity2.angularVelocity += pToCentroidCrossNormalB * j / entity2._inertia
        
        