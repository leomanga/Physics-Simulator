import numpy as np

from .Entities import Entity, Polygon, Ball
from .Utils import Utils

from icecream import ic

class CollisionManager():
    async def manageCollisionFrom(entity1:"Entity", entity2:"Entity"):
        if isinstance(entity1, Polygon) and isinstance(entity2, Polygon):
            CollisionManager._manageCollisionFromPolygons(entity1, entity2)

        elif isinstance(entity1, Polygon) and isinstance(entity2, Ball):
            CollisionManager._manageCollisionBallPolygon(entity1, entity2)
         
        elif isinstance(entity1, Ball) and isinstance(entity2, Polygon):
            CollisionManager._manageCollisionBallPolygon(entity2, entity1)
           

    
    def _manageCollisionFromPolygons(pol1:"Entity", pol2:"Entity"): #usiamo Separate Axis Theorem
        contactPoint1 = CollisionManager._getContactPoint(pol1, pol2)
        if contactPoint1 == False:
            return
                    
        contactPoint2 = CollisionManager._getContactPoint(pol2, pol1)
        if contactPoint2 == False:
            return
        
        depth = None
        contactPoint = None

        if contactPoint1[0] < contactPoint2[0]:
            depth =  contactPoint1[0] 
            contactPoint = contactPoint1[1]
        else:
            depth =  contactPoint2[0] 
            contactPoint = contactPoint2[1]

        pol1.setVelocity((0,0))
        pol2.setVelocity((0,0))

        pol1.setContactPoint(contactPoint)
        pol2.setContactPoint(contactPoint)

    def _getContactPoint(entity1, entity2) -> tuple:
        minDepth , minSupportPoint = CollisionManager._findSupportPoint(entity1, entity2, 0)
        for i in range(1, entity1.numberOfSides):
            depth, supportPoint = CollisionManager._findSupportPoint(entity1, entity2, i)
            if depth < 0 :
                return False
            if depth < minDepth :
                minDepth = depth
                minSupportPoint = supportPoint

        return minDepth, minSupportPoint
        
    def _findSupportPoint(pol1, pol2, vertexIndex) -> tuple:
        maxDepth = CollisionManager._calculateDepth(pol1.vertexes[vertexIndex], pol1.normals[vertexIndex], pol2.vertexes[0])
        maxSupportPoint = pol2.vertexes[0]
        for i in range(1, pol2.numberOfSides):
            depth=CollisionManager._calculateDepth(pol1.vertexes[vertexIndex], pol1.normals[vertexIndex], pol2.vertexes[i])
            if depth > maxDepth:
                maxDepth = depth
                maxSupportPoint = pol2.vertexes[i]
        return maxDepth, maxSupportPoint

    def _calculateDepth(pol1Vertex, pol1Normal, pol2Vertex):
        return np.dot((pol2Vertex - pol1Vertex) * -1, pol1Normal)
    
    def _manageCollisionBallPolygon(pol:"Polygon", ball:"Ball"):
        contactInfo:ContactInfo = CollisionManager._manageCircleVsPolygonEdges(pol, ball)

        if contactInfo is None:
            contactInfo = CollisionManager._manageCircleVsPolygonVertices(pol, ball)
        
        if contactInfo is None:
            return
        
        pol.setVelocity((0,0))
        ball.setVelocity((0,0))

        pol.setAcceleration((0,0))
        ball.setAcceleration((0,0))

        pol.setContactPoint(contactInfo.penetrationPoint)
    
    def _manageCircleVsPolygonEdges(pol : "Polygon", ball : "Ball") -> "ContactInfo":
        contactInfo = None
        for i in range (pol.numberOfSides):
            direction =  pol.vertexes[(i+1) % pol.numberOfSides] - pol.vertexes[i]

            dirToCircle = ball.position - pol.vertexes[i]          

            value = np.dot(dirToCircle, Utils.normalize(direction))

            if value > 0 and value < pol.sidesLength[i]:
                info = CollisionManager._getContactInfo(pol, ball, i)

                if info is not None:
                    contactInfo = info

        return contactInfo
                
    def _getContactInfo(pol : "Polygon", ball : "Ball", index) -> "ContactInfo":
        projectionToEdgeNormal = np.dot(ball.position - pol.vertexes[index], pol.normals[index])
        if projectionToEdgeNormal < 0:
            projectionToEdgeNormal = -projectionToEdgeNormal
        
        penetrationDepth = projectionToEdgeNormal - ball.radius
        if penetrationDepth > 0:
            return None
        
        penetrationPoint = ball.position + np.dot(pol.normals[index], ball.radius * -1)
        
        return ContactInfo(penetrationPoint, pol.normals[index], penetrationDepth)
        
    def _manageCircleVsPolygonVertices(pol : "Polygon", ball : "Ball") -> "ContactInfo":
        for vertex in pol.vertexes:
            distance = Utils.calculateDistance(vertex, ball.position)
            if distance <= ball.radius:
                penetrationPoint = vertex
                penetrationNormal = Utils.normalize(vertex-ball.position)
                penetrationDepth = ball.radius - np.linalg.norm(vertex-ball.position)

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
    

        



      
