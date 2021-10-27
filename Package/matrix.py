import numpy as np

class Matrix:
    rows = 0
    columns = 0

    matrix = []

    def __init__(self, columns: int=1, rows: int=1, filler: float=0):
        self.rows = rows
        self.columns = columns
        self.matrix = np.array([[filler for __ in range(rows)] for _ in range(columns)], dtype=np.float64)

    @staticmethod
    def GetXRotationMatrix(angle: float=0):
        matrix = Matrix(3, 3)

        matrix.setElement(0, 0, 1)
        angle = np.deg2rad(angle)

        sin = np.sin(angle)
        cos = np.cos(angle)

        matrix.setElement(1, 1,  cos)
        matrix.setElement(1, 2, -sin)

        matrix.setElement(2, 1,  sin)
        matrix.setElement(2, 2,  cos)

        return matrix

    @staticmethod
    def GetYRotationMatrix(angle: float):
        matrix = Matrix(3, 3)

        matrix.setElement(1, 1, 1)
        angle = np.deg2rad(angle)

        sin = np.sin(angle)
        cos = np.cos(angle)

        matrix.setElement(0, 0,  cos)
        matrix.setElement(0, 2, -sin)

        matrix.setElement(2, 0,  sin)
        matrix.setElement(2, 2,  cos)

        return matrix

    @staticmethod
    def GetZRotationMatrix(angle: float):
        matrix = Matrix(3, 3)

        matrix.setElement(2, 2, 1)
        angle = np.deg2rad(angle)

        sin = np.sin(angle)
        cos = np.cos(angle)

        matrix.setElement(0, 0,  cos)
        matrix.setElement(0, 1, -sin)

        matrix.setElement(1, 0,  sin)
        matrix.setElement(1, 1,  cos)

        return matrix

    @staticmethod
    def RotateVector(vector, rotation):
        from .vector import Vector3
        
        vector = vector.matrix

        vector = Matrix.dot(vector, Matrix.GetXRotationMatrix(rotation.x))
        vector = Matrix.dot(vector, Matrix.GetYRotationMatrix(rotation.y))
        vector = Matrix.dot(vector, Matrix.GetZRotationMatrix(rotation.z))

        return Vector3.fromMatrix(vector).normalized

    def setElement(self, x, y, value):
        self.matrix[x][y] = value

    def getElement(self, x, y):
        return self.matrix[x][y]

    @staticmethod
    def dot(a, b):       
        if b.columns != a.rows:
            raise ValueError("Columns of first matrix should match the number of rows of the second")

        a = a.matrix
        b = b.matrix

        mat = np.dot(a, b)
        m = Matrix(mat.shape[0], mat.shape[1])

        for x in range(mat.shape[0]):
            for y in range(mat.shape[1]):
                m.setElement(x, y, mat[x][y])

        return m

    def scale(self, scaler):
        for x in range(self.columns):
            for y in range(self.rows):
                self.matrix[x][y] *= scaler

    def __repr__(self):
        return "<Matrix at {}>\n".format(hex(id(self))) + str(self.matrix)
