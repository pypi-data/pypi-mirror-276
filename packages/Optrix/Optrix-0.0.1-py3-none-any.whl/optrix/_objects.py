import numpy as np

class OpticalObject:
    """ Base class for optical objects

    Parameters
    ----------
    name : str
        Name of the optical object
    """

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"
    
    def __mul__(self, obj1):
        return np.dot(self.Matrix, obj1)
    
class ThinLens(OpticalObject):
    """ Thin Lens object

    Parameters
    ----------
    focal_length : float
        Focal length of the thin lens
    """

    def __init__(self, focal_length=None, n=None, radius1=None, radius2=None, name="thin lens"):
        
        self._n = n
        self._R1 = radius1
        self._R2 = radius2
        self.name = name

        if focal_length is None and (self._n or self._R1 or self._R2) is None:
            raise ValueError("If focal length is not specified, n and R1 and R2 must be.")
        if focal_length is None and (self._n and self._R1 and self._R2) is not None:
            self._focal_length = (n-1)*(1/self._R1 - 1/self._R2)**-1
        elif focal_length is not None:
            self.focal_length = focal_length

        self._Matrix = np.array([[1, 0], [-1 / self._focal_length, 1]])

    
    @property
    def focal_length(self):
        if self._focal_length is None and (self._n or self._R1 or self._R2) is None:
            raise ValueError("If focal length is not specified, n and radius must be.")
        if self._focal_length is None and (self._n and self._R1 and self._R2) is not None:
            self._focal_length = (self._n-1)*(1/self._R1 - 1/self._R2)**-1
        return self._focal_length
    
    @focal_length.setter
    def focal_length(self, value):
        self._focal_length = value

    @property
    def n(self):
        return self._n
    
    @n.setter
    def n(self, value):
        self._n = value
    
    @property
    def R1(self):
        return self._R1
    
    @R1.setter
    def R1(self, value):
        self._R1 = value

    @property
    def R2(self):
        return self._R2
    
    @R2.setter
    def R2(self, value):
        self._R2 = value

    @property
    def Matrix(self):
        return np.array([[1, 0], [-1 / self._focal_length, 1]])

class Mirror(OpticalObject):
    """ Mirror object

    Parameters
    ----------
    radius : float
        Radius of curvature of the mirror. Default is None, which means the mirror is flat.
    """

    def __init__(self, radius=None, name = "mirror"):
        self.name = name
        self._radius = radius
        if radius is not None:
            self._Matrix = np.array([[1, 0], [2 / self._radius, 1]])
        else:
            self._Matrix = np.array([[1, 0], [0, 1]])
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def Matrix(self):
        if self._radius is not None:
            return np.array([[1, 0], [2 / self._radius, 1]])
        else:
            return np.array([[1, 0], [0, 1]])
    
class FreeSpace(OpticalObject):
    """ Free space propagation object

    Parameters
    ----------
    length : float
        Length of the free space propagation
    """

    def __init__(self, length, name = "free space propagation"):
        self.name = name
        self._length = length
        self._Matrix = np.array([[1, self._length], [0, 1]])
    
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        self._length = value

    @property
    def Matrix(self):
        return np.array([[1, self._length], [0, 1]])

class Boundary(OpticalObject):
    """ Boundary object

    Parameters
    ----------
    n1 : float
        Refractive index of the first medium
    n2 : float
        Refractive index of the second medium
    radius : float
        Radius of curvature of the boundary. Default is None, which means the boundary is flat.
    """

    def __init__(self, n1, n2, radius=None, name = "boundary"):
        self._n1 = n1
        self._n2 = n2
        self.name = name
        self._radius = radius
        if radius is not None:
            self._Matrix = np.array([[1, 0], [- (self._n2 - self._n1) / (self._n2 * self._radius), self._n1 / self._n2]])
        else:
            self._Matrix = np.array([[1, 0], [0, self._n1 / self._n2]])

    @property
    def n1(self):
        return self._n1
    
    @n1.setter
    def n1(self, value):
        self._n1 = value
    
    @property
    def n2(self):
        return self._n2
    
    @n2.setter
    def n2(self, value):
        self._n2 = value
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def Matrix(self):
        if self._radius is not None:
            return np.array([[1, 0], [- (self._n2 - self._n1) / (self._n2 * self._radius), self._n1 / self._n2]])
        else:
            return np.array([[1, 0], [0, self._n1 / self._n2]])   
            
class System(OpticalObject):
    """ System object

    Parameters
    ----------
    objects : Array
        Array of optical objects that compose the system. In order from the image to the object.
    """

    def __init__(self, objects, name = "system"):
        self.name = name
        self.objects = objects    
        self.object_matrices = np.array([object.Matrix for object in self.objects])
        self._Matrix = np.linalg.multi_dot(self.object_matrices)

    @property
    def Matrix(self):
        return self._Matrix
    
    @Matrix.setter
    def Matrix(self, value):
        self._Matrix = value
    
    def __mul__(self, obj1):
        return np.dot(self.Matrix, obj1)
    
class Object(OpticalObject):
    """ General Object

    Parameters
    ----------
    Matrix : Array
        Matrix of the object.
    
    focal_length : float
        Focal length of the object, if applicable. Default is none.
    
    distance : float
        Distance from the object to the next optical element, if applicable. Default is none.
    """

    def __init__(self, Matrix, focal_length=None, distance=None, name = "object"):
        self._Matrix = Matrix
        self._focal_length = focal_length
        self._distance = distance
        self.name = name
    
    @property
    def Matrix(self):
        return self._Matrix
    
    @Matrix.setter
    def Matrix(self, value):
        self._Matrix = value

    @property
    def focal_length(self):
        return self._focal_length
    
    @focal_length.setter
    def focal_length(self, value):
        self._focal_length = value

    @property
    def distance(self):
        return self._distance
    
    @distance.setter
    def distance(self, value):
        self._distance = value

class GaussianBeam:
    def __init__(self, wavelength, w0, A0):
        self.wavelength = wavelength
        self.w0 = w0
        self.A0 = A0

    def z0(self):
        return np.pi*self.w0**2/self.wavelength

    def w(self, z):   
        return self.w0*np.sqrt(1+(z/self.z0())**2)
        
    def R(self, z):
        return z*(1+(self.z0()/(z + 1e-15))**2)
        
    def zeta(self, z):
        return np.arctan(z/self.z0())

    def wavefunction(self, x, y, z):
        rho = np.sqrt(x**2 + y**2)
        A0 = self.A0
        w0 = self.w0
        w = self.w(z)
        k = 2*np.pi/self.wavelength
        R = self.R(z)
        zeta = self.zeta(z)
        return A0*(w0/w)*np.exp(-rho**2/(w**2 + 1e-15))*np.exp(-1j*k*(rho**2)/(2*R + 1e-15))*np.exp(1j*zeta)

    def wavefunction_in_0(self, x, y):
        A0 = self.A0
        w0 = self.w0
        return A0*np.exp(-(x**2+y**2)/w0**2 + 1e-15)

    def intensity(self, x, y, z):
        return np.abs(self.wavefunction(x, y, z))**2