from tools import normsq
import numpy as np
import math


class H2_segment:
    ''' This class implements a hyperbolic segment or geodesic in the Poincaré disk model '''

    def __init__(self, z1, z2):
        self.z1=z1
        self.z2=z2
        # complete

    def get_circle(self):
        ''' returns the Euclidean circle that the hyperbolic segment is an arc of '''
        x1=self.z1.real
        y1=self.z1.imag
        x2=self.z2.real
        y2=self.z2.imag
        if x1 * y2 != x2 * y1:
            x = (x1**2 * y2 - x2**2 * y1 + y1**2 * y2 - y1 * y2**2 + y2 - y1) / (2 * (x1 * y2 - x2 * y1))
            y = (x1**2 * x2 - x1 * x2**2 + y1**2 * x2 - x1 * y2**2 + x2 - x1) / (2 * (x2 * y1 - x1 * y2))
            c = x + y * 1j
            r = math.sqrt(normsq(self.z1-c))
            return r, c
        else:
            return -1, 0+0*1j
                                                  
    def get_ideal_endpoints(self):
        ''' returns the ideal endpoints of the geodesic extending the segment '''
        # complete
        r,c = self.get_circle()
        if r==-1 and c==0+0*1j:
            z1=self.z1
            z2=self.z2
            x1 = z1.real / math.sqrt(normsq(z1))
            x2 = -x1
            y1 = z1.imag / math.sqrt(normsq(z1))
            y2 = -y1
        else:
            a=c.real
            b=c.imag
            if a != 0:
                y1 = (b + a * r) / (r**2 + 1)
                y2 = (b - a * r) / (r**2 + 1)
                x1 = (1 - b * y1) / a
                x2 = (1 - b * y2) / a
            else:
                y1 = y2 = 1 / b
                x1 = math.sqrt(1 - 1 / b**2)
                x2 = -x1
        e1=x1+y1*1j
        e2=x2+y2*1j
        return e1, e2


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