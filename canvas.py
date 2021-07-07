import tkinter
import math
from h2geometry import *
from tools import mod2pi

class Canvas:
    def __init__(self, top):
        self.size_math = 2*1.2
        self.size_px = 0.8*min(top.winfo_screenwidth(), top.winfo_screenheight())
        self.origin_X = self.size_px/2
        self.origin_Y = self.size_px/2
        self.scale = self.size_px/self.size_math
        self.next = "red"
        
        self.cv = tkinter.Canvas(top, width=self.size_px, height=self.size_px, bg="white")
        self.cv.focus_set()
        self.cv.pack()
        self.draw_circle(0, 1, "purple")
        self.sides={}

    
    def mouse_click(self, event):
        X, Y = event.x, event.y
        x, y = self.px_to_math(X, Y)
        z = x + y*1j
        if normsq(z)<1:
            self.draw_point(z, color="blue")
        else:
            self.draw_point(z, color="red")
        
    def px_to_math(self, X, Y):
        x = (X - self.origin_X)/self.scale
        y = -(Y - self.origin_Y)/self.scale
        return x, y
        
    def math_to_px(self, x, y):
        X = np.rint(x*self.scale + self.origin_X)
        Y = np.rint(-(y*self.scale) + self.origin_Y)
        return X, Y

    def draw_point(self, z, color="black"):
        ''' Here z is a point in the plane given by a complex coordinate '''
        X, Y = self.math_to_px(z.real, z.imag)
        self.cv.create_oval(X-1, Y-1, X+2, Y+2, fill=color, outline=color, width=3)
        
    def draw_segment(self, z1, z2, color):
        self.draw_broken_line([z1, z2], color)

    def draw_broken_line(self, z, color):
        ''' Here z is a list of points given by their complex coordinates '''
        X, Y = self.math_to_px(np.real(z), np.imag(z))
        points = [[X[i], Y[i]] for i in range(len(X))]
        self.cv.create_line(points, fill=color, width=2)
        
    def draw_circle(self, c, r, color):
        X, Y = self.math_to_px(c.real, c.imag)
        R = np.rint(self.scale*r)
        self.cv.create_oval(X-R, Y-R, X+R+1, Y+R+1, outline=color, width=2)
        
    def draw_circle_arc(self, c, r, z1, z2, color):
        angle1 = mod2pi(np.angle(z1 - c))
        angle2 = mod2pi(np.angle(z2 - c))
        if ((z2-c)*((z1-c).conjugate())).imag < 0:
            angle1, angle2 = angle2, angle1
        X, Y = self.math_to_px(c.real,c.imag)
        R = self.scale*r
        self.cv.create_arc(X-R, Y-R, X+R+1, Y+R+1, start=angle1*180/np.pi, extent=mod2pi(angle2-angle1)*180/np.pi, outline=color, style=tkinter.ARC, width=1)


    def draw_H2_segment(self, z1, z2, color="blue", complete=True):
        ''' Draws the hyperbolic segment between two points '''
        #define an H2_segment object
        segment=H2_segment(z1, z2)
        #self.draw_point(z1,"red")
        #self.draw_point(z2,"red")
        #find the Euclidean circle that includes z1 and z2 and is centered on the boundary of the disk
        if z1!=z2:
            r, c=segment.get_circle()
            #get the corresponding ideal endpoints if complete == True
            if complete == True:
                e1, e2=segment.get_ideal_endpoints()
                self.draw_point(e1,"blue")
                self.draw_point(e2,"blue")
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r==-1 and c==0+0*1j:
                    self.draw_segment(e1, e2, color)
                else:
                    self.draw_circle_arc(c, r, e1, e2, color)
            else:
                #draw only the arc circle between z1 and z2
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r==-1 and c==0+0*1j:
                    self.draw_segment(z1, z2, color)
                else:
                    self.draw_circle_arc(c, r, z1, z2, color)

    def draw_H2_triangle(self, z1, z2, z3, color, fill=False):
        ''' Draws a hyperbolic triangle given by its vertices '''
        self.draw_H2_segment(z1, z2, color, False)
        self.draw_H2_segment(z2, z3, color, False)
        self.draw_H2_segment(z3, z1, color, False)

    def draw_H2_triangle_by_sides(self, sides):
        self.draw_H2_segment(sides[0].s.z1, sides[0].s.z2, complete=False)
        self.draw_H2_segment(sides[1].s.z1, sides[1].s.z2, complete=False)
        self.draw_H2_segment(sides[2].s.z1, sides[2].s.z2, complete=False)

    def draw_H2_polygon(self, z, color, fill=False):
        ''' Draws a hyperbolic polygon given by its list of vertices (z is a list)'''
        i = 0
        for vertex in z:
            self.draw_H2_segment(z[i-1],z[i], color)
            i += 1

    def H2_triangle_sides(self, z1, z2, z3):
        s12 = H2_segment(z1, z2)
        s23 = H2_segment(z2, z3)
        s13 = H2_segment(z1, z3)
        return s12, s23, s13
    
    def initiate_sides(self, s12, s23, s13):
        self.sides[s12]=1
        self.sides[s23]=1
        self.sides[s13]=1

    def triangle_already_here(self, s12, s23, s13):
        if s12 in self.sides and s23 in self.sides and s13 in self.sides:
            return True
        return False
    
    def add_missing_sides(self, s12, s23, s13):
        if not(s12 in self.sides):
            self.sides[s12]=1
        if not(s23 in self.sides):
            self.sides[s23]=1
        if not(s13 in self.sides):
            self.sides[s13]=1

    def make_tessellation(self, z1, z2, z3, startTriangle, limit=11, counter=11):
        """Makes a tessellation by reflecting the triangle."""
        if counter==limit:
            #startTriangle contains the hyperbolic segments of the starting triangle
            self.draw_H2_triangle_by_sides(startTriangle)
            counter=counter-1
        if counter!=0 and counter<limit:
            z1_ref, z2_ref, z3_ref = reflect_triangle(z1, z2, z3, startTriangle[0])
            s12, s23, s13 = self.H2_triangle_sides(z1_ref, z2_ref, z3_ref)
            if not self.triangle_already_here(s12, s23, s13):
                self.draw_H2_triangle(z1_ref, z2_ref, z3_ref, "purple")
                self.add_missing_sides(s12, s23, s13)
                self.make_tessellation(z1_ref, z2_ref, z3_ref,startTriangle, limit, counter-1)
            z1_ref, z2_ref, z3_ref = reflect_triangle(z1, z2, z3, startTriangle[1])
            s12, s23, s13 = self.H2_triangle_sides(z1_ref, z2_ref, z3_ref)
            if not self.triangle_already_here(s12, s23, s13):
                self.draw_H2_triangle(z1_ref, z2_ref, z3_ref, "purple")
                self.add_missing_sides(s12, s23, s13)
                self.make_tessellation(z1_ref, z2_ref, z3_ref,startTriangle, limit, counter-1)
            z1_ref, z2_ref, z3_ref = reflect_triangle(z1, z2, z3, startTriangle[2])
            s12, s23, s13 = self.H2_triangle_sides(z1_ref, z2_ref, z3_ref)
            if not self.triangle_already_here(s12, s23, s13):
                self.draw_H2_triangle(z1_ref, z2_ref, z3_ref, "purple")
                self.add_missing_sides(s12, s23, s13)
                self.make_tessellation(z1_ref, z2_ref, z3_ref,startTriangle, limit, counter-1)




