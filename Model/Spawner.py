from .Campo import Campo
from .Materials import SolidGroup
from .Entities.Ball import Ball
from .Entities.Polygons import RegularPolygon, IrregularPolygon

class Spawner:
    def __init__(self, campo: Campo):
        self._campo = campo
    
    def spawnEntities(self):
        solidGroup = SolidGroup()

        q1 = RegularPolygon(50, (200,200), 45, 4, solidGroup.wood)
        q1.setVelocity((50,0))
        self._campo.addEntity(q1)

        q2 = RegularPolygon(40, (400,220), 54, 4, solidGroup.wood)
        q2.setVelocity((-40,0))
        self._campo.addEntity(q2)

        """ for row in range(10):  # Numero di righe della piramide
                    num_poligoni = 10 - row  # Numero di poligoni per riga, decrescente
                    y_pos = self._campo.size[1] - row * 40  # Altezza dei poligoni, aumenta con le righe

                    for col in range(num_poligoni):
                        # Centriamo la riga rispetto alla base
                        x_pos = self._campo.size[0] / 2 - (num_poligoni / 2 * 40) + col * 40
                        pol = RegularPolygon(10, (x_pos, y_pos), 2, 3, solidGroup.wood)
                        pol.setAcceleration((1, 1))
                        pol.setVelocity((20, -2))
                        self._campo.addEntity(pol)"""