import numpy as np
import math
from icecream import ic
import asyncio
from .Vector import Vector

class Utils(): 
    def traslateVector(v1:np.ndarray, v2:np.ndarray) -> np.ndarray:
        return v1 + v2
    
    def sin(x:float) -> float:
        #in degrees
        return math.sin(math.radians(x))
    
    def cos(x:float) -> float:
        #in degrees
        return math.cos(math.radians(x))
    
    def rotate(vertex, point, rotationAngle):
        direction = vertex - point
        x = direction[0] * Utils.cos(rotationAngle) - direction[1] * Utils.sin(rotationAngle)
        y = direction[0] * Utils.sin(rotationAngle) + direction[1] * Utils.cos(rotationAngle)
        return Vector((x, y)) + point
    
    def ProjectEntityVertexes(direction:np.ndarray, vertexes:list[np.ndarray]) -> tuple[np.ndarray]: 
        #tuple[0]->point1 of the projection, tuple[1] point2 of the projection   
        minVector= Utils.project(direction, vertexes[0])
        maxVector= minVector
        length= len(vertexes)
        componentPosition = 1 if direction[0]==0 else 0
        for vertex in vertexes[1:]:
            actualProjection = Utils.project(direction, vertex)
            if actualProjection[componentPosition] < minVector[componentPosition]:
                minVector = actualProjection
            elif actualProjection[componentPosition] > maxVector[componentPosition]:
                maxVector = actualProjection
        return minVector, maxVector
                
    def project(direction:np.ndarray, vertex:np.ndarray)->np.ndarray:
        return (np.dot(direction,vertex)/np.dot(direction, direction))*direction
    
    def checkOverlap(entityProjection1, entityProjection2):
        # entityProjection[0] -> min projection vector, entityProjection[1] -> min projection vector
        minVector1 = entityProjection1[0]
        maxVector1 = entityProjection1[1]
        
        minVector2 = entityProjection2[0]
        maxVector2 = entityProjection2[1]
        
        # check if the projection are perpendicular to the x axes
        componentPosition = 1 if (minVector1[0]==0 and maxVector1[0] == 0) else 0
                
        overlapType1 = minVector1[componentPosition] <= maxVector2[componentPosition]
        overlapType2 = maxVector1[componentPosition] >= minVector2[componentPosition]
        return True if overlapType1 and overlapType2 else False
    
    def runAsyncTasks(loop:asyncio.AbstractEventLoop, tasks: list):
        loop.run_until_complete(asyncio.gather(*tasks))
        
    def normalize(vector):
       return vector / np.linalg.norm(vector)
       #return vector / math.sqrt(vector[0]**2 + vector[1]**2)  

    def calculateDistance(vector1:np.ndarray, vector2:np.ndarray):
        return np.linalg.norm(vector1 - vector2)      

    def clampIndex(index: int, minIndexAccepted: int, maxIndexAccepted:int) -> int:
        return max(min(index, maxIndexAccepted), minIndexAccepted)