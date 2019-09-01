import numpy as np
from math import sqrt

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def cross(self, other):
        return Vector((self.y * other.z) - (self.z * other.y), (self.z * other.x) - (self.x * other.z), (self.x * other.y) - (self.y * other.x))

    def length(self):
        return sqrt((self.x * self.x) + (self.y*self.y) + (self.z * self.z))

    def normalize(self):
        l = self.length()
        return(Vector(self.x / l, self.y / l, self.z / l))

class Triangle:
    def __init__(self, v1, v2, v3, n1, n2, n3, col, intensity):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.col = col
        self.intensity = intensity

    def get_data(self):
        return np.asarray([self.v1.x, self.v1.y, self.v1.z, 0,
                         self.v2.x, self.v2.y, self.v2.z, 0,
                         self.v3.x, self.v3.y, self.v3.z, 0,
                         self.n1.x, self.n1.y, self.n1.z, 0,
                         self.n2.x, self.n2.y, self.n2.z, 0,
                         self.n3.x, self.n3.y, self.n3.z, 0,
                         self.col.x, self.col.y, self.col.z,
                         self.intensity]).astype('f4')
