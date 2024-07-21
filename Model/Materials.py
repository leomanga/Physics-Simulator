
class FluidGroup():
    def __init__(self):
        self._void = Fluid(0)
        self._air = Fluid(1.70*10**(-4))
        self._water = Fluid(1*10**(-2))
    
    @property
    def air(self):
        return self._air

    @property
    def void(self):
        return self._void
    
    @property
    def water(self):
        return self._water

class Fluid():
    def __init__(self, viscosity):
        self._viscosity = viscosity
        
    def setViscosity(self, viscosity):
        self._viscosity = viscosity
    
    @property
    def viscosity(self):
        return self._viscosity
          
class SolidGroup():
    def __init__(self):
        self._wood = Solid(0.3, 0.5)
    
    @property
    def wood(self):
        return self._wood

class Solid():
    def __init__(self, friction, restituitionCoeff, density):
        self._friction = friction
        self._restituitionCoeff = restituitionCoeff
        self._density = density
    
    def setFriction(self, friction):
        self._friction = friction

    def setRestituitionCoeff(self, coeff):
        self._restituitionCoeff = coeff

    def setDensity(self, density):
        self._density = density

    @property
    def friction(self):
        return self._friction
    
    @property
    def restituitionCoeff(self):
        return self._restituitionCoeff
    
    @property
    def density(self):
        return self._density



