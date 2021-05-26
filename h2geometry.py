from tools import normsq
import numpy as np


class H2_segment:
    ''' This class implements a hyperbolic segment or geodesic in the Poincaré disk model '''

    def __init__(self, z1, z2):
        self.z1=z1
        self.z2=z2
        # complete
            
            
    def get_circle(self):
        ''' returns the Euclidean circle that the hyperbolic segment is an arc of '''
        # complete
        # return c, r
                                                  
    def get_ideal_endpoints(self):
        ''' returns the ideal endpoints of the geodesic extending the segment '''
        # complete


class H2_reflection:
    def __init__(self, s : H2_segment):
        ''' Initialization '''
        self.s = s
        # complete

    def reflect(self, z):
        ''' Computes the reflection of a point '''
        # complete


def H2_midpoint(z1, z2):
    ''' Computes the hyperbolic midpoint of two points in the Poincaré disk model '''
    # complete