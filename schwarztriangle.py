from tools import normsq
from canvas import Canvas
from h2geometry import *
import math
import numpy

class SchwarzTriangle:
    """This class implements a tessellation of the hyperbolic plane by Schwarz triangles."""

    def __init__(self, p, q, r):
        assert p > 2 and q > 2 and r > 2
        self.angle1 = math.pi/p
        self.angle2 = math.pi/q
        self.angle3 = math.pi/r
        self.lengths = self.__get_lengths()
        self.vertices = self.__get_vertices()

    def __get_lengths(self):
        """Gives a list of the lengths of the sides of the triangle"""
        a = numpy.arccos(math.cos((self.angle1) + math.cos(self.angle2)*math.cos(self.angle3) ) / 
                        (math.sin(self.angle2) * math.sin(self.angle3) ) )  
        b = numpy.arccos(math.cos((self.angle2) + math.cos(self.angle3)*math.cos(self.angle1) ) / 
                        (math.sin(self.angle3) * math.sin(self.angle1) ) )  
        c = numpy.arccos(math.cos((self.angle3) + math.cos(self.angle1)*math.cos(self.angle2) ) / 
                        (math.sin(self.angle1) * math.sin(self.angle2) ) )   
        return [a,b,c]

    def __get_vertices(self):
        """Returns the vertices of a triangle with the given angles."""
        b,c = self.lengths[1], self.lengths[2]
        A = 0
        B = eucl_dist_from_hyp_dist(c)
        p = (math.cos(self.angle1) + math.sin(self.angle1)*1j)
        b2 = eucl_dist_from_hyp_dist(b)
        C = b2 * p
        return [A,B,C]

