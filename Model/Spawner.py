from .Campo import Campo
from .Materials import SolidGroup
from .Entities.Ball import Ball
from .Entities.Polygons import RegularPolygon, IrregularPolygon

class Spawner:
    def __init__(self, campo: Campo):
        self._campo = campo
    
    def spawnEntities(self):
        solidGroup = SolidGroup()
        #testing
        """shape = [(68, 80),(32, 67) , (29, 17), (55, 33)]
        irregolare = IrregularPolygon(shape, (400, 400), 0, solidGroup.wood)
        irregolare.setVelocity((12, 12))

        self._campo.addEntity(irregolare)

        palla = Ball((300,300), 50, solidGroup.wood)

        palla.setVelocity((30,30))
        palla.setAcceleration((0, 0))
        palla.setAngularVelocity(3)
        palla.setAngularAcceleration(-0.4)

        self._campo.addEntity(palla)

        quadrato = RegularPolygon(123, (110,110), 45, 5, solidGroup.wood)
        quadrato.setVelocity((10, 10))
        quadrato.setAcceleration((10, 10))
        quadrato.setAngularVelocity(5)
        
        quadrato3 = RegularPolygon(70, (30,30), 0, 5,solidGroup.wood)
        quadrato3.setVelocity((10,0))
        quadrato4 = RegularPolygon(59, (400,90), 0, 4, solidGroup.wood)
        quadrato4.setVelocity((-10,0))
        
        #self._campo.addEntity(quadrato3)
        self._campo.addEntity(quadrato4)
        
        

        self._campo.addEntity(quadrato)

        quadrato2 = RegularPolygon(40, (650,200), 45, 4, solidGroup.wood)
        quadrato2.setVelocity((-20,0))
        quadrato2.setAcceleration((-0.05, 0))
        


        self._campo.addEntity(quadrato2)

        quadrato3 = RegularPolygon(40, (700,200), 36, 4, solidGroup.wood)
        quadrato3.setVelocity((-20,0))
        quadrato3.setAcceleration((-0.6, 0))

        self._campo.addEntity(quadrato3)


        palla2 = Ball((60, 600), 40, solidGroup.wood)
        palla2.setVelocity((65,-40))
        palla2.setAcceleration((0,+9.81))

        self._campo.addEntity(palla2)"""
        
        quadrato = quadrato = RegularPolygon(123, (110,110), 45, 5, solidGroup.wood)
        quadrato.setVelocity((10, 0))
        quadrato.setAcceleration((10, 0))
        quadrato.setAngularVelocity(5)
        
        quadrato3 = RegularPolygon(70, (300,110), 0, 5,solidGroup.wood)
        quadrato3.setVelocity((-10,0))
        
        self._campo.addEntity(quadrato)
        self._campo.addEntity(quadrato3)
        