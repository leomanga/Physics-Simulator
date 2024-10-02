import numpy as np

from typing import Sequence, Union

class Vector():
    def __init__(self, elements:Sequence[int | float]):
        self._dimension = len(elements)
        
        self._vector = np.array(elements)

        self._norm = np.linalg.norm(self._vector)
    
        self._normalized = None

#-------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"Vector({self._vector})"
    
    def __str__(self) -> str:
        return f"{(round(self._vector[0],0), round(self._vector[1],0))}"
    
    def __getitem__(self, index:int) -> int | float:
        """
        . vector[index]
        """
        return self._vector[index]

    def __setitem__(self, index:int, value:float | int):
        """
        . vector[index] = value
        """
        self._vector[index] = value
        
    def __len__(self) -> int:
        """
        . len(vector)
        """
        return self._dimension

    def __add__(self, other:"Vector") -> "Vector":
        """
        . result = vector1 + vector2
        """
        self._validate_same_dimension(other)
        return Vector(self._vector + other._vector)

    def __sub__(self, other:"Vector") -> "Vector":
        """
        . result = vector1 - vector2
        """
        self._validate_same_dimension(other)
        return Vector(self._vector - other._vector)
    
    def __mul__(self, other:Union["Vector", int, float]) -> Union[int, float, "Vector"]:
        """
        . Scalar product or scalar multiplication
            -----------------------------------------
            . result(int or float) = vector1 * vector2
            . result(Vector) = vector1 * scalar
        """
        if isinstance(other, Vector):
            return self._scalarProduct(other)
        
        return Vector(self._vector * other)
    
    def __matmul__(self, other: "Vector") -> "Vector":
            return self.cross(other)

    def __truediv__(self, other:int | float) -> "Vector":
        """
        . result = vector1 / scalar
        """
        if other == 0:
            raise ValueError("Cannot divide by zero")
        return Vector(self._vector / other)
            
    def __neg__(self) -> "Vector":
        """
        . result = -vector
        """
        return Vector(self._vector * -1)
    
    def __iadd__(self, other:"Vector"):
        """
        . vector1 += vector2
        """
        self._vector = self._vector + other._vector
        self._norm = np.linalg.norm(self._vector)
        return self

    def __isub__(self, other:"Vector"):
        """
        . vector1 -= vector2
        """
        self._vector = self._vector - other._vector
        self._norm = np.linalg.norm(self._vector)
        return self

    def __imul__(self, other:int | float):
        """
        . vector *= scalar
        """
        self._vector = self._vector * other
        self._norm = np.linalg.norm(self._vector)
        return self
    
    def __itruediv__(self, other:int | float):
        """
        . vector /= scalar
        """
        self._vector = self._vector / other
        self._norm = np.linalg.norm(self._vector)
        return self
    
    def __iter__(self):
        return iter(self._vector)

#-------------------------------------------------------------------
    def _scalarProduct(self, other: "Vector") -> Union[int, float]:
        """
        . You can simply use vector1 * vector2 
        """
        self._validate_same_dimension(other)
        return np.dot(self._vector, other._vector)
    
    def projectTo(self, other: "Vector") -> "Vector":
        self._validate_same_dimension(other)
        if other.norm == 0:
            raise ValueError("Cannot project onto a zero vector")
        return (self.scalarProduct(other) / other.scalarProduct(other)) * other
    
    def _validate_same_dimension(self, other: "Vector"):
        if self._dimension != other._dimension:
            raise ValueError("Vectors must have the same dimension")
        
    def cross(self, other: "Vector"):
        self._validate_same_dimension(other)
        return Vector(np.cross(self._vector, other._vector))
    
    @property
    def normalized(self) -> "Vector":
        if self._norm == 0:
                raise ValueError("Cannot normalize a zero vector")
        
        if self._normalized is None:
            self._normalized = Vector(self._vector / self._norm)

        return self._normalized

    @property
    def dimension(self) -> int:
        return self._dimension
    
    @property
    def norm(self) -> float:
        try:
            return self._norm
        except RuntimeWarning:
            return 0
    
class VectorZero(Vector):
    def __init__(self):
        super().__init__((0,0))