import math
import numpy as np
from abc import ABC, abstractmethod

from ..Materials import Solid
from ..Utils import Utils
from ..Vector import Vector, VectorZero
from Model.Entities.Entity import Entity

from icecream import ic

class Polygon(Entity, ABC):
    def __init__(self, rotation, material):
        super().__init__(rotation, material)
        
        self._numberOfSides: int = None

        self._vertexes: list[Vector] = []
        self._normals: list[Vector] = []
        
        self._sidesLength: list[float] = []
    
    def __repr__(self):
        return f"Polygon, {super().__repr__()}"  
     
    def __str__(self):
        return f"Polygon, {super().__str__()}"
    
    def translate(self, translation: Vector):
        super().translate(translation)
        for i in range(self._numberOfSides):
            self._vertexes[i] += translation
    
    def setCenterOfMass(self, newCenterOfMass: Vector):
        delta = newCenterOfMass - self._centerOfMass
        super().setCenterOfMass(newCenterOfMass)
        for i in range(self._numberOfSides):
            self._vertexes[i] += delta

    def move(self, deltaTime:float):
        self._updateMotions(deltaTime)

        deltaSpace = self._velocity * deltaTime
        deltaAngle = self._angularVelocity * deltaTime

        for i in range(self._numberOfSides):
            movedVertex = self._vertexes[i] + deltaSpace
            self._vertexes[i] = Utils.rotate(movedVertex, self._centerOfMass, -deltaAngle)
            self._normals[i] = Utils.rotate(self._normals[i], VectorZero(), -deltaAngle) 

        self._boundingBox.setPolygonBox(self._vertexes)    

    def printItself(self, view, debug = False):
        listVertexes=[tuple(vertex) for vertex in self._vertexes]
        color = view.baseColor if self._selected == False else view.clickedColor
        view.drawPolygon(listVertexes, color)  

        if debug:
            length = len(self._normals)
            for i in range(length):
                startingPoint = self._calculateMidPoint(self.vertexes[i], self.vertexes[(i + 1) % length])            
                view.drawLine(tuple(startingPoint), tuple((startingPoint + self._normals[i]*15)))
                view.drawText(i, tuple(self.vertexes[i]))

                view.drawBoundingBox(self._boundingBox)

        super().printItself(view, debug)

    def _initProperties(self):
        if len(self._vertexes) == 0:
                raise NotImplementedError(
                   "The _vertexes list is not initialized. Ensure that _vertexes is populated with valid data before calling _initProperties, as it relies on vertex information to function correctly."
                )

        self._initArea(self._vertexes)
        self._calculateNormals()
        self._initSidesLength() # It has to be initialized in a subclass
        self._initMass()
        self._initInertia()

    def _calculateNormals(self):
        for i in range(self.numberOfSides):
            direction : Vector = self.vertexes[i] - self.vertexes[(i + 1) % self.numberOfSides]
            directionVersor = -direction.normalized
            normalX = directionVersor[1]
            normalY = - directionVersor[0]

            self._normals.append(Vector((normalX, normalY)))

    def _calculateMidPoint(self, vec1:Vector, vec2:Vector) -> Vector:
        return vec1 + (vec2 - vec1) / 2 
    
    @abstractmethod
    def _initSidesLength(self):
        pass
    
    def _initArea(self, shape):
        self._area = 0
        for i in range(self._numberOfSides):
            self._area += shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0]
        self._area /= 2
        
    def _initInertia(self):
        self._inertia = 0
        massPerTriangle = self._mass / self._numberOfSides
        for i in range(self._numberOfSides):
            centerToVertice1 = self._vertexes[i] - self._centerOfMass
            centerToVertice2 = self._vertexes[(i+1)%self._numberOfSides] - self._centerOfMass
            self._inertia += massPerTriangle * (centerToVertice1.norm + centerToVertice2.norm + centerToVertice1 * centerToVertice2) / 6

    @property
    def vertexes(self) -> list[Vector]:
        return self._vertexes
    
    @property
    def normals(self) -> list[Vector]:
        return self._normals
    
    @property
    def numberOfSides(self):
        return self._numberOfSides
    
    @property
    def sidesLength(self):
        return self._sidesLength

class IrregularPolygon(Polygon):
    def __init__(self, shape: list[tuple], centerOfMass: tuple, rotation, material):
        super().__init__(rotation, material)
        self._numberOfSides = len(shape)
        self._centerOfMass = Vector(centerOfMass)
        
        self._initVertexes(shape)
        self._initProperties()
    
    def __repr__(self):
        return f"Irregular {super().__repr__()}"  
     
    def __str__(self):
        return f"Irregular {super().__str__()}"

    def _initVertexes(self, shape):
        centroid = self._getCentroid(shape)
        offset = self._centerOfMass - centroid
        for i in range(self._numberOfSides):
            self._vertexes.append(Vector(shape[i])+ offset)
        
    def _initSidesLength(self):
        for i in range(self._numberOfSides):
            direction: Vector = self.vertexes[(i+1) % self._numberOfSides] - self.vertexes[i]
            self._sidesLength.append(direction.norm)
    
    def _getCentroid(self, shape):
        if self._area == None:
            self._initArea(shape)
        cx = 0
        cy = 0 
        for i in range(self._numberOfSides):
            cx += (shape[i][0] + shape [(i+1)% self._numberOfSides][0])*(shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0])
            cy += (shape[i][1] + shape [(i+1)% self._numberOfSides][1])*(shape[i][0]*shape[(i+1) % self._numberOfSides][1] - shape[i][1]*shape[(i+1) % self._numberOfSides][0])
        cx /= 6*self._area
        cy /= 6*self._area
        return Vector((cx, cy))
    
class RegularPolygon(Polygon):
    def __init__(self, sideLength, centerOfMass: tuple, rotation, numberOfSides, material: Solid):
        super().__init__(rotation, material)
        self._numberOfSides = numberOfSides
        self._centerOfMass = Vector(centerOfMass)
        
        self._sideLength = sideLength

        self._apothem = self._calculateApothem()
        
        self._initVertexes()
        self._initProperties()
    
    def __repr__(self):
        return f"Regular {super().__repr__()}"  
     
    def __str__(self):
        return f"Regular {super().__str__()}"
    
    def _initVertexes(self):            
        angles = np.linspace(math.radians(self._rotation), 2*np.pi + math.radians(self._rotation), self._numberOfSides, endpoint=False)
        x:list = self._apothem*np.cos(angles)
        y:list = self._apothem*np.sin(angles)
        xOffset:list =x+self._centerOfMass[0]
        yOffset:list =y+self._centerOfMass[1]

        for i in range(self._numberOfSides):
            self._vertexes.append(Vector((xOffset[i], yOffset[i])))    
    
    def _initSidesLength(self):
        for i in range(self._numberOfSides):
            self._sidesLength.append(self._sideLength)

    def _calculateApothem(self):
        return (self._sideLength/2)/Utils.sin(180/self._numberOfSides)