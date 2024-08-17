import numpy as np

from .Entities import Entity, Polygon, Ball
from .Utils import Utils

from icecream import ic

from typing import Union
from .Vector import Vector

class CollisionManager():
    @staticmethod
    async def manageCollisionFrom(entity1:"Entity", entity2:"Entity"):
        if isinstance(entity1, Polygon) and isinstance(entity2, Polygon):
            CollisionManager._manageCollisionPolygonVSPolygon(entity1, entity2)

        elif isinstance(entity1, Polygon) and isinstance(entity2, Ball):
            CollisionManager._manageCollisionBallVSPolygon(entity1, entity2)
         
        elif isinstance(entity1, Ball) and isinstance(entity2, Polygon):
            CollisionManager._manageCollisionBallVSPolygon(entity2, entity1)
    
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

        pol1.setVelocity((0,0))
        pol2.setVelocity((0,0))

        pol1.setContactPoint(contactInfo.penetrationPoint)
        pol2.setContactPoint(contactInfo.penetrationPoint)
 
    @staticmethod
    def _manageCollisionBallVSPolygon(pol:"Polygon", ball:"Ball"):
        contactInfo: ContactInfo | None = CollisionManager._manageCircleVsPolygonEdges(pol, ball)

        if contactInfo is None:
            contactInfo: ContactInfo | None = CollisionManager._manageCircleVsPolygonVertices(pol, ball)
        
        if contactInfo is None:
            return
        
        pol.setVelocity((0,0))
        ball.setVelocity((0,0))

        pol.setAcceleration((0,0))
        ball.setAcceleration((0,0))

        pol.setContactPoint(contactInfo.penetrationPoint)

    @staticmethod
    def _getContactInfoPolVSPol(pol1:"Polygon", pol2:"Polygon") -> Union["ContactInfo", None]:
        minDepth , minSupportPoint = CollisionManager._findSupportPoint(pol1, pol2, 0)
        for i in range(1, pol1.numberOfSides):
            depth, supportPoint = CollisionManager._findSupportPoint(pol1, pol2, i)
            if depth < 0 :
                return None
            if depth < minDepth :
                minDepth = depth
                minSupportPoint = supportPoint
        """
        TODO:
        -inserire la penetration normal, per ora è None
        """
        return ContactInfo(minSupportPoint, None, minDepth)
        
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
        for i in range(1, pol2.numberOfSides):
            depth=CollisionManager._calculateDepth(pol1.vertexes[vertexIndex], pol1.normals[vertexIndex], pol2.vertexes[i])
            if depth > maxDepth:
                maxDepth = depth
                maxSupportPoint = pol2.vertexes[i]
        return maxDepth, maxSupportPoint

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
    

        



      
