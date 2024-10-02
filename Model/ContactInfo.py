from Model.Vector import Vector      
class ContactInfo():
    def __init__(self, penetrationPoint: Vector, penetrationNormal: Vector, penetrationDepth: float):
        self._penetrationPoint = penetrationPoint
        self._penetrationNormal = penetrationNormal
        self._penetrationDepth = penetrationDepth
    
    def __repr__(self):
        return f"Penetration Point:{self._penetrationPoint}, Penetration Normal:{self._penetrationNormal}, Penetration Depth:{self._penetrationDepth}"

    def swapNormal(self):
        self._penetrationNormal *= -1

    @property
    def penetrationPoint(self) -> Vector:
        return self._penetrationPoint

    @property
    def penetrationNormal(self) -> Vector:
        return self._penetrationNormal
    
    @property
    def penetrationDepth(self) -> float:
        return self._penetrationDepth
    