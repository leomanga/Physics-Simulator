          
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
    