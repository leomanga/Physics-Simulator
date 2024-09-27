import numpy as np

from .Entities.Ball import Ball
from .Entities.EntityGroup import EntityGroup
from .Entities.Entity import Entity
from .Entities.Polygons import Polygon
from .Utils import Utils

from icecream import ic

from typing import Union
from .Vector import Vector


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
                polygon.stopMotion()
                return
            

    @staticmethod
    def _manageBallVSBorder(ball: Ball, size: tuple):
        if not CollisionManager._isBallCollidingBorder(ball, size):
            return 
        
        ball.stopMotion()

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
    async def manageCollisionFrom(entity1:"Entity", entity2:"Entity"):
        info = None
        if isinstance(entity1, Polygon) and isinstance(entity2, Polygon):
            info = CollisionManager._manageCollisionPolygonVSPolygon(entity1, entity2)

        elif isinstance(entity1, Polygon) and isinstance(entity2, Ball):
            info = CollisionManager._manageCollisionBallVSPolygon(entity1, entity2)
         
        elif isinstance(entity1, Ball) and isinstance(entity2, Polygon):
            info = CollisionManager._manageCollisionBallVSPolygon(entity2, entity1)
        
        else:
            info = CollisionManager._manageCollisionBallVSBall(entity1, entity2)
        
        #CollisionResolver.manageImpulse(entity1, entity2, info)
        
            
    
    @staticmethod
    def _manageCollisionPolygonVSPolygon(pol1:"Entity", pol2:"Entity"): #usiamo Separate Axis Theorem
        contactInfo1: ContactInfo | None = CollisionManager._getContactInfoPolVSPol(pol1, pol2)
        if contactInfo1 is None:
            return
                    
        contactInfo2: ContactInfo | None = CollisionManager._getContactInfoPolVSPol(pol2, pol1)
        if contactInfo2 is None:
            return
        
        contactInfo: ContactInfo = contactInfo1

        if contactInfo1.penetrationDepth > contactInfo2.penetrationDepth:
            contactInfo = contactInfo2

        pol1.stopMotion()
        pol2.stopMotion()

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
        
        pol.stopMotion()
        ball.stopMotion()

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
        
        ball1.stopMotion()
        ball2.stopMotion()
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
        projectionToEdgeNormal = (ball.position - pol.vertexes[index]) * pol.normals[index]
        if projectionToEdgeNormal < 0:
            projectionToEdgeNormal = -projectionToEdgeNormal
        
        penetrationDepth = projectionToEdgeNormal - ball.radius
        if penetrationDepth > 0:
            return None
        
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
        contactInfo = None
        for i in range (pol.numberOfSides):
            direction: Vector =  pol.vertexes[(i+1) % pol.numberOfSides] - pol.vertexes[i]

            dirToCircle = ball.position - pol.vertexes[i]          

            value = dirToCircle * direction.normalized

            if value > 0 and value < pol.sidesLength[i]:
                info = CollisionManager._getContactInfoPolVSBall(pol, ball, i)

                if info is not None:
                    contactInfo = info

        return contactInfo
    
    @staticmethod
    def _manageCircleVsPolygonVertices(pol : "Polygon", ball : "Ball") -> Union["ContactInfo", None]:
        for vertex in pol.vertexes:
            distance = Utils.calculateDistance(vertex, ball.position)
            if distance <= ball.radius:
                penetrationPoint = vertex
                penetrationNormal = Utils.normalize(vertex-ball.position)

                offset = vertex-ball.position

                penetrationDepth = ball.radius - offset.norm

                return ContactInfo(penetrationPoint, penetrationNormal, penetrationDepth)
            

            
class ContactInfo():
    def __init__(self, penetrationPoint, penetrationNormal, penetrationDepth):
        self._penetrationPoint = penetrationPoint
        self._penetrationNormal = penetrationNormal
        self._penetrationDepth = penetrationDepth

    @property
    def penetrationPoint(self):
        return self._penetrationPoint
    
    @property
    def penetrationNormal(self):
        return self._penetrationNormal
    
    @property
    def penetrationDepth(self):
        return self._penetrationDepth
    

        



      
