import numpy as np
import math
class Utils(): 
    def traslateVector(v1:np.ndarray, v2:np.ndarray) -> np.ndarray:
        return v1 + v2
    
    def sin(x:float) -> float:
        #in degrees
        return math.sin(math.radians(x))
    
    def cos(x:float) -> float:
        #in degrees
        return math.cos(math.radians(x))