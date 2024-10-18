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
        # Corregge la penetrazione prima di gestire l'impulso
        CollisionResolver._correctPosition(entity1, entity2, info)

        # Energia cinetica iniziale
        k1 = entity1.kineticEnergy + entity2.kineticEnergy

        # Vettori dalla penetrazione al centro di massa
        r1 = info.penetrationPoint - entity1.centerOfMass
        r2 = info.penetrationPoint - entity2.centerOfMass

        # Rotazione dei vettori per ottenere la velocità angolare al punto di collisione
        angularVelocityPenetration1 = Vector((-r1[1], r1[0])) * entity1.angularVelocity
        angularVelocityPenetration2 = Vector((-r2[1], r2[0])) * entity2.angularVelocity

        # Velocità totale (lineare + angolare) al punto di collisione
        velocity1 = entity1.velocity + angularVelocityPenetration1
        velocity2 = entity2.velocity + angularVelocityPenetration2

        # Calcolo della velocità relativa e della sua componente lungo la normale
        relativeVelocity = velocity2 - velocity1
        relativeVelocityAlongNormal = relativeVelocity * info.penetrationNormal

        # Se la velocità relativa è positiva, i corpi si stanno già separando
        if relativeVelocityAlongNormal > 0:
            return

        restitutionProduct = entity1.material.restituitionCoeff * entity2.material.restituitionCoeff
        restitutionSum = entity1.material.restituitionCoeff +  entity2.material.restituitionCoeff

        bounciness = 2 * restitutionProduct / restitutionSum

        # Momenti rispetto al punto di collisione proiettati sulla normale
        r1CrossNormal = r1 @ info.penetrationNormal
        r2CrossNormal = r2 @ info.penetrationNormal

        # Somma delle masse inverse e degli effetti angolari sull'impulso
        invMassSum = 1 / entity1.mass + 1 / entity2.mass
        rotationalEffect = (r1CrossNormal ** 2) / entity1.inertia + (r2CrossNormal ** 2) / entity2.inertia

        # Denominatore dell'impulso, tenendo conto della massa e dell'inerzia
        impulseDenominator = invMassSum + rotationalEffect

        # Calcolo dell'impulso usando il coefficiente di restituzione
        impulseMagnitude = -(1 + bounciness) * relativeVelocityAlongNormal / impulseDenominator
        impulseVector = info.penetrationNormal * impulseMagnitude

        # Aggiornamento delle velocità lineari
        entity1.setVelocity(entity1.velocity - impulseVector / entity1.mass)
        entity2.setVelocity(entity2.velocity + impulseVector / entity2.mass)

        # Aggiornamento delle velocità angolari
        entity1.setAngularVelocity(entity1.angularVelocity - (r1CrossNormal * impulseMagnitude / entity1.inertia))
        entity2.setAngularVelocity(entity2.angularVelocity + (r2CrossNormal * impulseMagnitude / entity2.inertia))

    @staticmethod
    def manageImpulse2(entity1: Entity, entity2: Entity, info: ContactInfo):
        CollisionResolver._correctPosition(entity1, entity2, info)

        penetrationCentroidToEntity1: Vector = info.penetrationPoint - entity1.centerOfMass
        penetrationCentroidToEntity2: Vector = info.penetrationPoint - entity2.centerOfMass

        normalizedPenetrationPoint1 = Vector((-penetrationCentroidToEntity1[1], penetrationCentroidToEntity1[0])) # Rotates the vector 90 degrees counterclockwise
        normalizedPenetrationPoint2 = Vector((-penetrationCentroidToEntity2[1], penetrationCentroidToEntity2[0])) # Rotates the vector 90 degrees counterclockwise

        angularVelocityPenetrationCentroidEntity1 = normalizedPenetrationPoint1 * entity1.angularVelocity
        angularVelocityPenetrationCentroidEntity2 = normalizedPenetrationPoint2 * entity2.angularVelocity

        velocityEntity1 = entity1.velocity + angularVelocityPenetrationCentroidEntity1 # relative velocity of entity2 from entity1
        velocityEntity2 = entity2.velocity + angularVelocityPenetrationCentroidEntity2 
        """andrebbe sommato"""

        relativeVelocity = velocityEntity2 - velocityEntity1 # relative velocity of entity2 from entity1
        relativeVelocityAlongNormal = relativeVelocity * info.penetrationNormal

        if relativeVelocityAlongNormal > 0: # chech if the second entity is faster than the first
            return
                
        restitutionProduct = entity1.material.restituitionCoeff * entity2.material.restituitionCoeff
        restitutionSum = entity1.material.restituitionCoeff +  entity2.material.restituitionCoeff

        bounciness = 2 * restitutionProduct / restitutionSum

        pToCentroidCrossNormal1 = penetrationCentroidToEntity1 @ info.penetrationNormal
        pToCentroidCrossNormal2 = penetrationCentroidToEntity2 @ info.penetrationNormal

        ic(pToCentroidCrossNormal1, pToCentroidCrossNormal2)

        crossNSum1 = pToCentroidCrossNormal1 * pToCentroidCrossNormal1 / entity1.inertia
        crossNSum2 = pToCentroidCrossNormal2 * pToCentroidCrossNormal2 / entity2.inertia
        crossNSum = crossNSum1 + crossNSum2
        #print(relativeVelocityAlongNormal)
        #ic(-(1+bounciness) * relativeVelocityAlongNormal)
        #ic(1/entity1.mass + 1/entity2.mass + crossNSum)
        
        bounciness = 1

        impulse = -(1+bounciness) * relativeVelocityAlongNormal / (1/entity1.mass + 1/entity2.mass + crossNSum)
        impulseVector = info.penetrationNormal * impulse / 2
        #print(impulseVector)
        impulseVector*=40

        impulseVectorEntity1 = -impulseVector / entity1.mass
        impulseVectorEntity2 = impulseVector / entity2.mass
        #print(impulseVectorEntity1)

        entity1.setVelocity(entity1.velocity + impulseVectorEntity1)
        entity2.setVelocity(entity2.velocity + impulseVectorEntity2)

        entity1.setAngularVelocity(entity1.angularVelocity - pToCentroidCrossNormal1 * impulse / entity1.inertia)
        entity2.setAngularVelocity(entity2.angularVelocity + pToCentroidCrossNormal2 * impulse / entity2.inertia)
