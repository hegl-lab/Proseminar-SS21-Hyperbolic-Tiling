import math

class SchwarzTriangle:
    """This class implements a tessellation of the hyperbolic plane by Schwarz triangles."""

    def __init__(self, p, q, r):
        assert p > 2 and q > 2 and r > 2
        self.angle1 = math.pi/p
        self.angle2 = math.pi/q
        self.angle3 = math.pi/r
        self.vertices = self.get_vertices()

    def get_vertices(self):
        """Returns a list of the vertices of a triangle with the given angles."""

        