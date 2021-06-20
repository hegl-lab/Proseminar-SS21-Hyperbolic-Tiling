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
        norm_M_z1 = normsq(self.z1)
        length_A_S = math.sqrt(1 - (norm_M_z1) ** 2)
        senk_A = -self.z1.imag + self.z1.real * j
        senk_A.real = senk_A.real / (normsq(senk_A) * length_A_S)
        senk_A.imag = senk_A.imag / (normsq(senk_A) * length_A_S)
        S = self.z1 + senk_A
        s = -S.real +S.imag * j
        x = S / (self.z1 - (s))
        A = S + (x * (s))
        K1 = self.z1 + 0.5 * normsq(A-self.z1)
        K2 = self.z1 + 0.5 * normsq(self.z2 - self.z1)
        x = (K1-K2) / ((self.z2-self.z1)-(A-self.z1))
        c = K1 + x * (A-self.z1)
        r = normsq (c - self.z1)
        return(c, r)

                                                  
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
    # complete