
class Utils():
    def sumVec(v1:tuple, v2:tuple) -> tuple:
        return tuple(a + b for a, b in zip(v1, v2))