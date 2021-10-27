from typing import Literal
import numpy as np
from ctypes import Structure, c_float


FAST_PRINT: bool = False


class Vector3:
    x = 0
    y = 0
    z = 0

    # Unit Vectors
    once = None
    zero = None
    xUnit = None
    yUnit = None
    zUnit = None

    Axis = None

    def __init__(self, x: float=0, y: float=0, z: float=0):
        self.x = x
        self.y = y
        self.z = z

    # Properties
    @property
    def array(self):
        return np.array([self.x, self.y, self.z])
    
    @property
    def magnitude(self):
        return np.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    @property
    def magnitudeSqr(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    @property
    def normalized(self):
        v = Vector3(self.x, self.y, self.z)
        v.normalize()
        return v

    @property
    def structure(self):
        return Vector3Structure(self)

    # Dot and Cross products
    @staticmethod
    def dot(v1, v2):
        return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

    @staticmethod
    def cross(v1, v2):
        v = Vector3()

        v.x = v1.y*v2.z - v1.z*v2.y
        v.y = v1.z*v2.y - v1.x*v2.z
        v.z = v1.x*v2.y - v1.y*v2.x

        return v

    # Matrix
    @property
    def matrix(self):
        from .matrix import Matrix
        
        m = Matrix(1, 3, 0)

        m.matrix[0][0] = self.x
        m.matrix[0][1] = self.y
        m.matrix[0][2] = self.z

        return m

    # Math
    def scale(self, scaler):
        self.x *= scaler
        self.y *= scaler
        self.z *= scaler
    
    def normalize(self):
        self *= 1 / self.magnitude

    def distance(self, other):
        xdist = (other.x-self.x)*(other.x-self.x)
        ydist = (other.y-self.y)*(other.y-self.y)
        zdist = (other.z-self.z)*(other.z-self.z)

        return np.sqrt(xdist + ydist + zdist)

    def distanceSqr(self, other):
        xdist = (other.x-self.x)*(other.x-self.x)
        ydist = (other.y-self.y)*(other.y-self.y)
        zdist = (other.z-self.z)*(other.z-self.z)

        return xdist + ydist + zdist

    def setMegnitude(self, meg):
        self.normalize()
        self *= meg

    def __add__(self, other):
        v = Vector3()

        v.x = self.x + other.x
        v.y = self.y + other.y
        v.z = self.z + other.z
        
        return v

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

        return self

    def __sub__(self, other):
        v = Vector3()

        v.x = self.x - other.x
        v.y = self.y - other.y
        v.z = self.z - other.z
        
        return v

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

        return self

    def __mul__(self, other):
        v = Vector3()

        if type(other) in [float, int, np.float64]:
            v.x = self.x
            v.y = self.y
            v.z = self.z

            v.scale(other)

        elif type(other) in [tuple, list, np.ndarray] and np.array(other).shape == (3,):
            _v = Vector3(other[0], other[1], other[2])
            v = Vector3.dot(self, _v)

        elif type(other) == Vector3:
            v = Vector3.dot(self, other)

        else:
            raise NotImplementedError("This type of Vector multiplication is not implimented yet.")

        return v

    def __imul__(self, other):
        if type(other) in [float, int, np.float64]:
            self.scale(other)
        
        elif type(other) in [tuple, list, np.ndarray] and np.array(other).shape == (3,):
            v = Vector3(other[0], other[1], other[2])
            self = Vector3.dot(self, v)

        elif type(other) == Vector3:
            self = Vector3.dot(self, other)

        else:
            raise NotImplementedError("This type of Vector multiplication is not implimented yet.")
            
        return self

    # Conversion        
    def __repr__(self):
        if not FAST_PRINT:
            _id = hex(id(self))
            s: str = "<Vector3 at {}>:".format(_id)

            if self.x < 0: s += " - "
            else: s += " "

            s += str(abs(np.float16(self.x))) + "i"
            
            if self.y < 0: s += " - "
            else: s += " + "

            s += str(abs(np.float16(self.y))) + "j"
            
            if self.z < 0: s += " - "
            else: s += " + "

            s += str(abs(np.float16(self.z))) + "k"

            return s

        else:
            return "<Vector3 at {}>: {}i + {}j + {}k".format(hex(id(self)), self.x, self.y, self.z)

    @staticmethod
    def fromMatrix(matrix):
        return Vector3(matrix.matrix[0][0], matrix.matrix[0][1], matrix.matrix[0][2])

Vector3.once = Vector3(1, 1, 1)
Vector3.zero = Vector3(0, 0, 0)

Vector3.xUnit = Vector3(1, 0, 0)
Vector3.yUnit = Vector3(0, 1, 0)
Vector3.zUnit = Vector3(0, 0, 1)

Vector3.Axis = {
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A
}

class Vector3Structure(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float)
    ]

    def __init__(self, v: Vector3):
        self.x = v.x
        self.y = v.y
        self.z = v.z
