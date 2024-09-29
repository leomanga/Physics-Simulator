from Model.Entities.EntityGroup import EntityGroup

from icecream import ic

ic.disable()
class SpatialGrid():
    pass
    def __init__(self, size: tuple, nCellsAxis: tuple, entityGroup: EntityGroup):
        self._size = size

        self._gridColLength = self._size[0] / nCellsAxis[0]
        self._gridRowLength = self._size[1] / nCellsAxis[1]

        self._nCellsAxis = nCellsAxis

        self._totalGrids = nCellsAxis[0] * nCellsAxis[1]
        self._grids: list[list] = None
        self._resetGrids()
        self._entityGroup: EntityGroup = entityGroup

    def _resetGrids(self):
        self._grids = []
        for i in range(self._totalGrids):
            self._grids.append([])
        ic("SPATIAL GRID ->", self._totalGrids, len(self._grids))
        ic("SPATIAL GRID -> ", self._grids)

    def _populateGrids(self):
        for entity in self._entityGroup:
            colLeft = int(entity.boundingBox.topLeft[0] / self._gridColLength)
            colRight = int(entity.boundingBox.bottomRight[0] / self._gridColLength)

            rowTop = int(entity.boundingBox.topLeft[1] / self._gridRowLength)
            rowBottom = int(entity.boundingBox.bottomRight[1] / self._gridRowLength)
            for i in range(colLeft, colRight + 1):
                indexTop = rowTop * self._nCellsAxis[0] + i
                indexBottom = rowBottom * self._nCellsAxis[0] + i

                self._grids[indexTop].append(entity)
                if indexTop != indexBottom:
                    self._grids[indexBottom].append(entity)
                ic(self._grids)

                #ic("SPATIAL GRID ->", i, entity, indexTop, indexBottom ,self._grids[indexTop], self._grids[indexBottom])
            
            for j in range(rowTop + 1, rowBottom): # evito di fare gli angoli dato che li ho fatti sopra
                indexRow = j * self._nCellsAxis[0]

                coordLeft = indexRow + colLeft
                coordRight = indexRow + colRight

                self._grids[coordLeft].append(entity)
                self._grids[coordRight].append(entity) 

                #ic("SPATIAL GRID ->",j, coordLeft, coordRight ,entity, self._grids[coordLeft], self._grids[coordRight])
            ic(colLeft, colRight, entity)
            ic("SPATIAL GRID ->", self._grids)

    @property
    def gridRowLength(self) -> float:
        return self._gridRowLength
    
    @property
    def gridColLength(self) -> float:
        return self._gridColLength
    
    @property
    def nCellsAxis(self) -> tuple[int, int]:
        return self._nCellsAxis
    
    @property
    def grids(self) -> list[list]:
        return self._grids
        
