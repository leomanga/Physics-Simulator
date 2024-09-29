from ..Vector import Vector

from icecream import ic
class BoundingBox():
    def __init__(self):
        self._topLeft = None
        self._bottomRight = None

    def setBallBox(self, position: Vector, radius: float):
        self._topLeft = position - Vector((radius, radius))
        self._bottomRight = position + Vector((radius, radius))
        
    def setPolygonBox(self, vertexes: list[Vector]):
        minX = vertexes[0][0]
        maxX = vertexes[0][0]

        minY = vertexes[0][1]
        maxY = vertexes[0][1]

        for i in range(1, len(vertexes)):
            if vertexes[i][0] < minX:
                minX = vertexes[i][0]
            if vertexes[i][0] > maxX:
                maxX = vertexes[i][0]
            if vertexes[i][1] < minY:
                minY = vertexes[i][1]
            if vertexes[i][1] > maxY:
                maxY = vertexes[i][1]
            
        self._topLeft = Vector((minX, minY))
        self._bottomRight = Vector((maxX, maxY))
    
    @property
    def topLeft(self):
        return self._topLeft

    @property
    def bottomRight(self):
        return self._bottomRight

    