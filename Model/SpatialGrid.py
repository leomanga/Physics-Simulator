from Model.Entities.EntityGroup import EntityGroup, Entity
from Model.Utils import Utils
from icecream import ic
import time
class SpatialGrid():
    def __init__(self, size: tuple, nCellsAxis: tuple, entityGroup: EntityGroup):
        self._size = size

        self._gridColLength = self._size[0] / nCellsAxis[0] + 1 # +1 to avoid error to the borders
        self._gridRowLength = self._size[1] / nCellsAxis[1] + 1 # +1 to avoid error to the borders

        self._nCellsAxis = nCellsAxis

        self._totalGrids = nCellsAxis[0] * nCellsAxis[1]
        self._grids: list[set[Entity]] = None
        self._entityToGrids: list[list] = None
        self._entityGroup: EntityGroup = entityGroup
        self.resetGrids()
        
    def getNeighbourEntities(self, entityIndex: int) -> list[Entity]:
        entity = self._entityGroup[entityIndex]
        occupiedGrids = self._entityToGrids[entityIndex]
        neighbour: list[Entity] = []

        for gridIndex in occupiedGrids:
            grid: list[Entity] = self._grids[gridIndex]
            for possibleNeighbour in grid:
                if possibleNeighbour.id != entity.id:
                    neighbour.append(possibleNeighbour)

        return neighbour
    
    def clearEntity(self, entityIndex):
        entity = self._entityGroup[entityIndex]
        occupiedGrids = self._entityToGrids[entityIndex]
        for gridIndex in occupiedGrids:
            grid: set[Entity] = self._grids[gridIndex]
            grid.discard(entity)

    def resetGrids(self):
        self._grids = [set() for _ in range(self._totalGrids)]
        self._entityToGrids = [[] for _ in range(len(self._entityGroup))]

    def populateGrids(self):
        for entityIndex, entity in enumerate(self._entityGroup):
            colLeft = Utils.clampIndex(int(entity.boundingBox.topLeft[0] / self._gridColLength), 0, self._nCellsAxis[0] - 1)
            colRight =  Utils.clampIndex(int(entity.boundingBox.bottomRight[0] / self._gridColLength), 0, self._nCellsAxis[0] - 1)

            rowTop = Utils.clampIndex(int(entity.boundingBox.topLeft[1] / self._gridRowLength), 0, self._nCellsAxis[1] - 1)
            rowBottom = Utils.clampIndex(int(entity.boundingBox.bottomRight[1] / self._gridRowLength), 0, self._nCellsAxis[1] - 1)

            for i in range(colLeft, colRight + 1):
                indexTop = rowTop * self._nCellsAxis[0] + i
                indexBottom = rowBottom * self._nCellsAxis[0] + i

                self._grids[indexTop].add(entity)
                self._entityToGrids[entityIndex].append(indexTop)
                if indexTop != indexBottom:
                    self._grids[indexBottom].add(entity)
                    self._entityToGrids[entityIndex].append(indexBottom)
            
            for j in range(rowTop + 1, rowBottom): # evito di fare gli angoli dato che li ho fatti sopra
                indexRow = j * self._nCellsAxis[0]

                indexLeft = indexRow + colLeft
                indexRight = indexRow + colRight

                self._grids[indexLeft].add(entity)
                self._grids[indexRight].add(entity) 

                self._entityToGrids[entityIndex].append(indexLeft)
                self._entityToGrids[entityIndex].append(indexRight)

            """for i in range(colLeft, colRight + 1):
                for j in range(rowTop, rowBottom + 1):
                    gridIndex = j * self._nCellsAxis[0] + i
                    self._grids[gridIndex].add(entity)
                    self._entityToGrids[entityIndex].append(gridIndex)"""

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
    
    @property
    def entityToGrids(self) -> list[list]:
        return self._entityToGrids
        
