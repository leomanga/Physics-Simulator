import numpy as np

from .Entities.Ball import Ball
from .Entities.EntityGroup import EntityGroup
from .Entities.Entity import Entity
from .Entities.Polygons import Polygon
from .Utils import Utils

from icecream import ic

from typing import Union
from .Vector import Vector

from .ContactInfo import ContactInfo
from .CollisionResolver import CollisionResolver
from View.View import View


class CollisionManager():
    @staticmethod
    def isPointInsideEntity(point:Vector, entity:"Entity") -> bool:
        if isinstance(entity, Ball):
            distance: Vector = point - entity.position
            return True if distance.norm < entity.radius else False
        else:
            return CollisionManager._isPointInsidePolygon(point, entity)
        
    def _isPointInsidePolygon(point:"Vector", polygon:"Polygon"):
        for i in range(polygon.numberOfSides):
            depth = (point - polygon.vertexes[i]) * polygon.normals[i] * -1
            if depth < 0:
                return False
        
        return True
    
    @staticmethod
    def manageElementsVsBorderCollisions(entityGroup: EntityGroup, size: tuple):
        """
        TODO:
            - quando faremo oggetti fissi avrà senso rimuovere questa funzione e mettere degli oggetti ai bordi
        """
        for entity in entityGroup:
            if isinstance(entity, Polygon):
                CollisionManager._managePolygonVSBorder(entity, size)
            
            elif isinstance(entity, Ball):
                CollisionManager._manageBallVSBorder(entity, size)

    @staticmethod
    def _managePolygonVSBorder(polygon: Polygon, size: tuple):
        for vertex in polygon.vertexes:
            if CollisionManager._isVertexInsideBorder(vertex, size):
                #polygon.stopMotion()
                polygon._velocity*=-0.5
                polygon._angularVelocity*=-0.5
                delta = polygon._velocity * 0.01
                polygon._centerOfMass-=delta
                for i in polygon._vertexes:
                    i +=delta
                return
            

    @staticmethod
    def _manageBallVSBorder(ball: Ball, size: tuple):
        if not CollisionManager._isBallCollidingBorder(ball, size):
            return 
        
        #ball.stopMotion()

    @staticmethod
    def _isVertexInsideBorder(vertex: Vector, size: tuple):
        if vertex[0] < 0: # left
            return True
        if vertex[1] < 0: # up
            return True
        if vertex[0] > size[0]: # right
            return True
        if vertex[1] > size[1]: # down
            return True
        
        return False

    @staticmethod
    def _isBallCollidingBorder(ball: Ball, size: tuple):
        if ball.centerOfMass[0] - ball.radius < 0: # left
            return True
        if ball.centerOfMass[1] - ball.radius < 0: # up
            return True
        if ball.centerOfMass[0] + ball.radius > size[0]: # right
            return True
        if ball.centerOfMass[1] + ball.radius > size[1]: # down
            return True
        
        return False

    @staticmethod
    def manageCollisionFrom(entity1:"Entity", entity2:"Entity"):
        info = None
        if not CollisionManager._boundingBoxCollides(entity1, entity2):
            return
        
        if isinstance(entity1, Polygon) and isinstance(entity2, Polygon):
            info = CollisionManager._manageCollisionPolygonVSPolygon(entity1, entity2)

        elif isinstance(entity1, Ball) and isinstance(entity2, Polygon):
            info = CollisionManager._manageCollisionBallVSPolygon(entity2, entity1)
        
        elif isinstance(entity1, Polygon) and isinstance(entity2, Ball):
            info = CollisionManager._manageCollisionBallVSPolygon(entity1, entity2)
            entity1, entity2 = entity2, entity1
        else:
            info = CollisionManager._manageCollisionBallVSBall(entity1, entity2)
        
        if info is not None:
            #entity1.stopMotion()
            #entity2.stopMotion()
            #CollisionResolver.positionalCorrection(entity1, entity2, info)
            CollisionResolver.manageImpulse(entity1, entity2, info)
        
    @staticmethod
    def _boundingBoxCollides(entity1: Entity, entity2: Entity):
        if not (entity1.boundingBox.bottomRight[0] > entity2.boundingBox.topLeft[0] and entity2.boundingBox.bottomRight[0] > entity1.boundingBox.topLeft[0]):
            return False
        
        if entity1.boundingBox.topLeft[1] < entity2.boundingBox.bottomRight[1] and entity2.boundingBox.topLeft[1] < entity1.boundingBox.bottomRight[1]:
            return True
        
        return False
    
    @staticmethod
    def _manageCollisionPolygonVSPolygon(pol1:"Entity", pol2:"Entity"): #usiamo Separate Axis Theorem
        contactInfo1: ContactInfo | None = CollisionManager._getContactInfoPolVSPol(pol1, pol2)
        if contactInfo1 is None:
            return
                    
        contactInfo2: ContactInfo | None = CollisionManager._getContactInfoPolVSPol(pol2, pol1)
        if contactInfo2 is None:
            return
        
        contactInfo: ContactInfo = contactInfo1

        if contactInfo1.penetrationDepth < contactInfo2.penetrationDepth:
            contactInfo1._penetrationDepth = -(contactInfo1._penetrationDepth)
            contactInfo = contactInfo1
            
        else:
            contactInfo = contactInfo2
            contactInfo._penetrationNormal*=-1 #fare setter
        

        #pol1.stopMotion()
        #pol2.stopMotion()

        pol1.setContactPoint(contactInfo.penetrationPoint)
        pol2.setContactPoint(contactInfo.penetrationPoint)
        return contactInfo
 
    @staticmethod
    def _manageCollisionBallVSPolygon(pol:"Polygon", ball:"Ball"):
        contactInfo: ContactInfo | None = CollisionManager._manageCircleVsPolygonEdges(pol, ball)

        if contactInfo is None:
            contactInfo: ContactInfo | None = CollisionManager._manageCircleVsPolygonVertices(pol, ball)
        
        if contactInfo is None:
            return
        
        #pol.stopMotion()
        #ball.stopMotion()

        pol.setContactPoint(contactInfo.penetrationPoint)
        return contactInfo

    
    @staticmethod
    def _manageCollisionBallVSBall(ball1: "Ball", ball2: "Ball"):
        maxDistance = ball1.radius + ball2.radius
        direction = ball1.position - ball2.position
        if direction.norm > maxDistance:
            return 

        depth = maxDistance - direction.norm
        penetrationPoint = direction.normalized * (ball2.radius - depth) + ball2.position
        
        #ball1.stopMotion()
        #ball2.stopMotion()
        ball1._contactPoint = penetrationPoint
        
        return ContactInfo(penetrationPoint, direction, depth)



    @staticmethod
    def _getContactInfoPolVSPol(pol1:"Polygon", pol2:"Polygon") -> Union["ContactInfo", None]:
        minDepth , minSupportPoint, minNormal = CollisionManager._findSupportPoint(pol1, pol2, 0)
        for i in range(1, pol1.numberOfSides):
            depth, supportPoint, normal = CollisionManager._findSupportPoint(pol1, pol2, i)
            if depth < 0 :
                return None
            if depth < minDepth :
                minDepth = depth
                minSupportPoint = supportPoint
                minNormal = normal
      
        return ContactInfo(minSupportPoint, minNormal , minDepth)
        
    @staticmethod         
    def _getContactInfoPolVSBall(pol : "Polygon", ball : "Ball", index) -> "ContactInfo":
        k=1
        projectionToEdgeNormal = (ball.position - pol.vertexes[index]) * pol.normals[index]
        if projectionToEdgeNormal < 0:
            projectionToEdgeNormal = -projectionToEdgeNormal
            k=-1
            
        
        penetrationDepth = projectionToEdgeNormal - ball.radius
        if penetrationDepth > 0:
            return None
        
        penetrationDepth = k*projectionToEdgeNormal - ball.radius
        
        penetrationPoint = ball.position + (pol.normals[index] * ball.radius * -1)
        
        return ContactInfo(penetrationPoint, pol.normals[index], penetrationDepth)

    @staticmethod
    def _findSupportPoint(pol1, pol2, vertexIndex) -> tuple:
        maxDepth = CollisionManager._calculateDepth(pol1.vertexes[vertexIndex], pol1.normals[vertexIndex], pol2.vertexes[0])
        maxSupportPoint = pol2.vertexes[0]
        maxNormal = pol2.normals[0]
        for i in range(1, pol2.numberOfSides):
            depth=CollisionManager._calculateDepth(pol1.vertexes[vertexIndex], pol1.normals[vertexIndex], pol2.vertexes[i])
            if depth > maxDepth:
                maxDepth = depth
                maxSupportPoint = pol2.vertexes[i]
                maxNormal = pol2.normals[i]
        return maxDepth, maxSupportPoint, maxNormal

    @staticmethod
    def _calculateDepth(pol1Vertex, pol1Normal, pol2Vertex):
        return ((pol2Vertex - pol1Vertex) * -1) * pol1Normal
    
    @staticmethod
    def _manageCircleVsPolygonEdges(pol : "Polygon", ball : "Ball") -> Union["ContactInfo", None]:
        nearestEdgeVertex = None
        nearestEdgeNormal = None
        for i in range (pol.numberOfSides):
            vertToCircle = ball.centerOfMass - pol.vertexes[i]
            vertToVert = pol.vertexes[(i+1)%pol.numberOfSides] - pol.vertexes[i]
            vertToVertLength = vertToVert.norm
            circleDirToNextProj = vertToCircle * vertToVert.normalized
            circleDirToNormalProjection = vertToCircle * pol.normals[i]
            if(circleDirToNormalProjection>=0 and circleDirToNextProj > 0 and circleDirToNextProj < vertToVertLength):
                nearestEdgeNormal = pol.normals[i]
                nearestEdgeVertex = pol.vertexes[i]
    
        if nearestEdgeNormal == None or nearestEdgeVertex == None:
            return None
        
        vertexToCircle = ball.centerOfMass - nearestEdgeVertex
        projectionToEdgeNormal = nearestEdgeNormal*vertexToCircle
        if (projectionToEdgeNormal - ball.radius) < 0:
            penetration = projectionToEdgeNormal - ball.radius
            penetrationPoint = ball.centerOfMass + nearestEdgeNormal*ball.radius*-1
            return ContactInfo(penetrationPoint, nearestEdgeNormal, -penetration)
    
        return None
    
    @staticmethod
    def _manageCircleVsPolygonVertices(pol : "Polygon", ball : "Ball") -> Union["ContactInfo", None]:
        for vertex in pol.vertexes:
            distance = (vertex-ball.centerOfMass).norm
            if distance <= ball.radius:
                penetrationPoint = vertex
                penetrationNormal = (vertex-ball.centerOfMass).normalized

                offset = vertex-ball.position

                penetrationDepth = ball.radius - offset.norm
                
                
                contact = ContactInfo(penetrationPoint, penetrationNormal, penetrationDepth)
                CollisionResolver.manageImpulse(ball, pol, contact)
                return
        return None
            



        



      
