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
        # complete
        # return c, r
        midx = (self.z1.real + self.z2.real) / 2
        midy = (self.z1.imag + self.z2.imag) / 2
        if normsq(self.z1)<=1 and normsq(self.z2)<=1:
            if self.z2.imag != self.z1.imag:
                slope = (self.z1.real - self.z2.real) / (self.z2.imag - self.z1.imag)
                #the condition midy!=slope*midx alone was causing trouble for z1.real==z2.real
                if midy != slope * midx or self.z1.real==self.z2.real:
                    delta = -4 * (midy - midx * slope) ** 2 + 4 * (1 + slope ** 2)
                    x1=(-2 * slope * (midy - slope * midx) + math.sqrt(delta)) / (2 * (1 + slope ** 2))
                    y1=midy + slope * (x1 - midx)
                    x2=(-2 * slope * (midy - slope * midx) - math.sqrt(delta)) / (2 * (1 + slope ** 2))
                    y2=midy + slope * (x2 - midx)
                    if math.sqrt(((x1 - midx) ** 2) + ((y1 - midy) ** 2)) < math.sqrt(((x2 - midx) ** 2) + ((y2 - midy) ** 2)):
                        c=x1+y1*1j
                    else:
                        c=x2+y2*1j
                    r=math.sqrt(((c.real-self.z1.real)**2)+((c.imag-self.z1.imag))**2)  
                else:
                    r=-1
                    c=0+0*1j
            else:
                if self.z1.imag == 0:
                    r=-1
                    c=0+0*1j
                else:
                    x=midx
                    y=math.sqrt(1-x**2)
                    if y*self.z1.imag<0:
                        y=-y
                    c=x+y*1j
                    r=math.sqrt(((c.real-self.z1.real)**2)+((c.imag-self.z1.imag))**2)
        return r,c
                    
                                                  
    def get_ideal_endpoints(self):
        ''' returns the ideal endpoints of the geodesic extending the segment '''
        # complete
        r,c = self.get_circle()
        if r==-1 and c==0+0*1j:
            z1=self.z1
            z2=self.z2
            if z1.real!=z2.real:
                delta=4*(z2.real-z1.real)**2*((z2.real-z1.real)**2+(z2.imag-z1.imag)**2-(z1.real*z2.imag-z1.imag*z2.real)**2)
                x1=(2*(z2.imag-z1.imag)*(z1.real*z2.imag-z1.imag*z2.real)+math.sqrt(delta))/(2*(z2.real-z1.real)**2+2*(z2.imag-z1.imag)**2)
                x2=(2*(z2.imag-z1.imag)*(z1.real*z2.imag-z1.imag*z2.real)-math.sqrt(delta))/(2*(z2.real-z1.real)**2+2*(z2.imag-z1.imag)**2)
                y1=z1.imag+(x1-z1.real)*(z2.imag-z1.imag)/(z2.real-z1.real)
                y2=z1.imag+(x2-z1.real)*(z2.imag-z1.imag)/(z2.real-z1.real)

        else:
            a=c.real
            b=c.imag
            y1=(b*(2-r**2)+a*r*math.sqrt(4-r**2))/2
            y2=(b*(2-r**2)-a*r*math.sqrt(4-r**2))/2
            x1=(a*(2-r**2)-b*r*math.sqrt(4-r**2))/2
            x2=(a*(2-r**2)+b*r*math.sqrt(4-r**2))/2
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
    # Something is wrong here and I don't know what.
    fz2 = H2_midpoint_help_function(z1, z2)
    r1 = math.sqrt(normsq(z1))
    hyp_dist = H2_distance_on_diameter(r1)
    half_hyp_dist = hyp_dist / 2
    r2 = eucl_dist_from_hyp_dist(half_hyp_dist)
    m2 = r2 / r1 * fz2

    return H2_midpoint_inverse_help_function(z1, m2)

def H2_midpoint_help_function(z1, z):
    """Sends z1 to 0 and z somewhere else. This is an isometry"""
    return (z - z1) / (1 - math.sqrt(normsq(z1)) * z)

def H2_midpoint_inverse_help_function(z1, z):
    """Sends 0 to z1. This is an isometry and the inverse of the other help function."""
    return (z + z1) / (1 + math.sqrt(normsq(z1))*z)

def H2_distance_on_diameter(r):
    """Returns the hyperbolic distance between 0 and some point with euclidean distance r."""
    return math.log((1 + r) / (1 - r))

def eucl_dist_from_hyp_dist(h):
    """Returns the euclidean distance on euclidean straight line that gives the given hyperbolic distance.
    THis explanation is bad, redo it."""
    return (-1 + math.e**h) / (1 + math.e**h) 