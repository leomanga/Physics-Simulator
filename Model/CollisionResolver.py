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

#still testing

class CollisionResolver():
    @staticmethod
    def move(entity: Entity, deltaVector: Vector):
        entity.centerOfMass += deltaVector
        if isinstance(entity, Polygon):
            for i in entity.vertexes:
                i += deltaVector
        
    @staticmethod
    def positionalCorrection(entity1: Entity, entity2: Entity, info: ContactInfo):
        correction = 0.7 * (entity1.mass * entity2.mass) / (entity1.mass + entity2.mass)
        amountToCorrect = -info.penetrationDepth / correction
        correctionVector = info.penetrationNormal * amountToCorrect
        movementOne = (correctionVector / entity1.mass)
        movementTwo = -(correctionVector / entity2.mass)
        CollisionResolver.move(entity1, movementOne)
        CollisionResolver.move(entity2, movementTwo)
    
    @staticmethod
    def _correctPosition(entity1: Entity, entity2: Entity, info: ContactInfo):
        push = info.penetrationNormal * info.penetrationDepth / 2
        entity1.translate(-push)
        entity2.translate(push)
        
    @staticmethod
    def manageImpulse(entity1: Entity, entity2: Entity, info: ContactInfo):
        #CollisionResolver._correctPosition(entity1, entity2, info)
        #entity1.stopMotion()
        #entity2.stopMotion()
        #return

        penetrationCentroidToEntity1: Vector = info.penetrationPoint - entity1.centerOfMass
        penetrationCentroidToEntity2: Vector = info.penetrationPoint - entity2.centerOfMass

        normalizedPenetrationPoint1 = Vector((-penetrationCentroidToEntity1[1], penetrationCentroidToEntity1[0])) # Rotates the vector 90 degrees counterclockwise
        normalizedPenetrationPoint2 = Vector((-penetrationCentroidToEntity2[1], penetrationCentroidToEntity2[0])) # Rotates the vector 90 degrees counterclockwise

        angularVelocityPenetrationCentroidEntity1 = normalizedPenetrationPoint1 * entity1.angularVelocity
        angularVelocityPenetrationCentroidEntity2 = normalizedPenetrationPoint2 * entity2.angularVelocity

        velocityEntity1 = entity1.velocity - angularVelocityPenetrationCentroidEntity1 # relative velocity of entity2 from entity1
        velocityEntity2 = entity2.velocity - angularVelocityPenetrationCentroidEntity2 
        """andrebbe sommato"""

        relativeVelocity = velocityEntity2 - velocityEntity1 # relative velocity of entity2 from entity1
        #print(relativeVelocity)
        #print(info.penetrationNormal)
        relativeVelocityAlongNormal = relativeVelocity * info.penetrationNormal
        #print(relativeVelocityAlongNormal)

        if relativeVelocityAlongNormal > 0: # chech if the second entity is faster than the first
            return
        
        #ic(relativeVelocityAlongNormal)
        
        restitutionProduct = entity1.material.restituitionCoeff * entity2.material.restituitionCoeff
        restitutionSum = entity1.material.restituitionCoeff +  entity2.material.restituitionCoeff

        bounciness = 2 * restitutionProduct / restitutionSum
        #bounciness = -1

        pToCentroidCrossNormal1 = penetrationCentroidToEntity1 @ info.penetrationNormal
        pToCentroidCrossNormal2 = penetrationCentroidToEntity2 @ info.penetrationNormal

        crossNSum1 = pToCentroidCrossNormal1 * pToCentroidCrossNormal1 / entity1.inertia
        crossNSum2 = pToCentroidCrossNormal2 * pToCentroidCrossNormal2 / entity2.inertia
        crossNSum = crossNSum1 + crossNSum2
        #print(relativeVelocityAlongNormal)
        #ic(-(1+bounciness) * relativeVelocityAlongNormal)
        #ic(1/entity1.mass + 1/entity2.mass + crossNSum)
        

        impulse = -(1+bounciness) * relativeVelocityAlongNormal / (1/entity1.mass + 1/entity2.mass + crossNSum)
        impulseVector = info.penetrationNormal * impulse / 2
        #print(impulseVector)

        impulseVectorEntity1 = -impulseVector / entity1.mass
        impulseVectorEntity2 = impulseVector / entity2.mass
        #print(impulseVectorEntity1)

        entity1.setVelocity(entity1.velocity + impulseVectorEntity1)
        entity2.setVelocity(entity2.velocity + impulseVectorEntity2)

        entity1.setAngularVelocity(entity1.angularVelocity - pToCentroidCrossNormal1 * impulse / entity1.inertia)
        entity2.setAngularVelocity(entity2.angularVelocity + pToCentroidCrossNormal2 * impulse / entity2.inertia)