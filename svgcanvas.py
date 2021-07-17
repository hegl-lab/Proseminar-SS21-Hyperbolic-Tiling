import tkinter
import math
from h2geometry import *
from tools import mod2pi

from schwarztriangle import SchwarzTriangle

import drawSvg
from PIL import Image, ImageTk

from time import sleep

class Canvas:
    def __init__(self, top):
        self.size_px = 0.8*min(top.winfo_screenwidth(), top.winfo_screenheight())
        
        self.svg = drawSvg.Drawing(2.4, 2.4, origin = 'center')
        self.svg.append(drawSvg.Rectangle(-1.2,-1.2,2.4,2.4, fill="#FFF"))
        
        self.svg.append(drawSvg.Circle(0,0,1, fill="#FFF", stroke="#000", stroke_width=0.005))
        
        self.cv = tkinter.Canvas(top, width=self.size_px, height=self.size_px, bg="white")
        self.cv.focus_set()
        self.cv.pack()
        
        self.__refresh()
        
        self.sides = {}

    def __refresh(self):
        self.svg.setRenderSize(self.size_px, self.size_px)
        self.svg.savePng("tmp.png")
        self.tkimg = ImageTk.PhotoImage(Image.open("tmp.png"))
        
        self.cv.create_image(0, 0, anchor = "nw", image=self.tkimg)

    def exportSvg(self, filename):
        self.svg.saveSvg(filename)

    def exportPng(self, filename, width, height):
        self.svg.setRenderSize(width, height)
        self.svg.savePng(filename)
    
    def px_to_math(self, x, y):
        X = -1.2 + 2.4 * x/self.size_px
        Y =  1.2 - 2.4 * y/self.size_px
        return X, Y
        
    def mouse_click(self, event):
        x, y = self.px_to_math(event.x, event.y)
        z = x + y*1j
        if normsq(z)<1:
            self.draw_point(z, color = "#00F")
        else:
            self.draw_point(z, color = "#F00")

    def draw_point(self, z, color = "#000", refresh = True):
        ''' Here z is a point in the plane given by a complex coordinate '''
        self.svg.append(drawSvg.Circle(z.real, z.imag, 0.01, fill = color))
        if refresh:
            self.__refresh()

    def draw_segment(self, z1, z2, color = "#000", width = 0.005, refresh = True):
        self.draw_broken_line([z1, z2], color, width, False)
        if refresh:
            self.__refresh()

    def draw_broken_line(self, z, color = "#000", width = 0.005, refresh = True):
        ''' Here z is a list of points given by their complex coordinates '''
        for i in range(1,len(z)):
            self.svg.append(drawSvg.Line(z[i-1].real, z[i-1].imag, z[i].real, z[i].imag, stroke = color, stroke_width = width))
        if refresh:
            self.__refresh()

    def draw_circle(self, c, r, color = "#000", width = 0.005, fill = 'none', refresh = True):
        self.svg.append(drawSvg.Circle(c.real, c.imag, r, stroke = color, stroke_width = width, fill = fill))
        if refresh:
            self.__refresh()
            
    def draw_circle_arc(self, c, r, z1, z2, color = "#000", width = 0.005, refresh = True):
        angle1 = mod2pi(np.angle(z1 - c)) / (2 * np.pi) * 360
        angle2 = mod2pi(np.angle(z2 - c)) / (2 * np.pi) * 360
        if ((z2-c)*((z1-c).conjugate())).imag < 0:
            angle1, angle2 = angle2, angle1
        
        self.svg.append(drawSvg.Arc(c.real, c.imag, r, angle1, angle2, stroke = color, stroke_width = width, fill = 'none'))
        
        if refresh:
            self.__refresh()
          
    def draw_H2_segment(self, z1, z2, color = "#000", width = 0.005, complete = False, drawpoints = False, refresh = True):
        ''' Draws the hyperbolic segment between two points '''
        #define an H2_segment object
        segment=H2_segment(z1, z2)
        #self.draw_point(z1,"red")
        #self.draw_point(z2,"red")
        #find the Euclidean circle that includes z1 and z2 and is centered on the boundary of the disk
        if z1 != z2:
            r, c = segment.get_circle()
            #get the corresponding ideal endpoints if complete == True
            if complete == True:
                e1, e2 = segment.get_ideal_endpoints()
                if drawpoints:
                    self.draw_point(e1, color)
                    self.draw_point(e2, color)
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if r == -1 and c == 0+0*1j:
                    self.draw_segment(e1, e2, color, width, False)
                else:
                    self.draw_circle_arc(c, r, e1, e2, color, width, False)
            else:
                #draw only the arc circle between z1 and z2
                #2 cases
                # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
                # case 2: the euclidean line connecting z1 and z2 is not a diameter
                if drawpoints:
                    self.draw_point(z1, color)
                    self.draw_point(z2, color)
                
                if r == -1 and c == 0+0*1j:
                    self.draw_segment(z1, z2, color, width, False)
                else:
                    self.draw_circle_arc(c, r, z1, z2, color, width, False)
                    
        if refresh:
            self.__refresh()
                
    def __create_H2_segment_str(self, z1, z2, complete = False, move_to_first_point = False):
        ''' Generates the path command for drawing an hyperbolic segment from z1 to z2 '''
        #define an H2_segment object
        segment=H2_segment(z1, z2)
        
        cmd = ""
        if z1 != z2:            
            r, c = segment.get_circle()
        
            #get the corresponding ideal endpoints if complete == True
            if complete == True:
                u1, u2 = segment.get_ideal_endpoints()
            else:
                u1, u2 = z1, z2
                
            #2 cases
            # case 1: the euclidean line connecting z1 and z2 is a diameter-->r==-1 and c=0
            # case 2: the euclidean line connecting z1 and z2 is not a diameter
            if r == -1 and c == 0+0*1j:
                if move_to_first_point:
                    cmd += "M " + str(u1.real) + " " + str(-u1.imag) + " "
                cmd += "L " + str(u2.real) + " " + str(-u2.imag)
            else:
                v1 = u1 - c
                v2 = u2 - c
                v1 = (v1/abs(v1) * r) + c
                v2 = (v2/abs(v2) * r) + c
            
                angle1 = mod2pi(np.angle(v1 - c))
                angle2 = mod2pi(np.angle(v2 - c))
                
                swap = 0
                if angle1 > angle2:
                    swap = 1
            
                if abs(angle2 - angle1) > np.pi:
                    swap = 1 - swap
            
                if move_to_first_point:
                    cmd += "M " + str(v1.real) + " " + str(-v1.imag) + " "
                    
                cmd += "A " + str(r) + " " + str(r) + " 0 0 " + str(swap) + " " + str(v2.real) + " " + str(-v2.imag)
                
        return cmd

    def draw_H2_triangle(self, z1, z2, z3, color = "#000", width = 0.005, fill = 'none', refresh = True):
        ''' Draws a hyperbolic triangle given by its vertices '''
        if fill == 'none':
            self.draw_H2_segment(z1, z2, color, width, refresh = False)
            self.draw_H2_segment(z2, z3, color, width, refresh = False)
            self.draw_H2_segment(z3, z1, color, width, refresh = False)
        else:
            cmd = " " + self.__create_H2_segment_str(z1, z2, move_to_first_point = True)
            cmd += " " + self.__create_H2_segment_str(z2, z3)
            cmd += " " + self.__create_H2_segment_str(z3, z1)
            self.svg.append(drawSvg.Path(cmd, stroke = color, stroke_width = width, fill = fill))
            
        if refresh:
            self.__refresh()
            
    def draw_H2_polygon(self, z, color = "#000", width = 0.005, fill = 'none', refresh = True):
        ''' Draws a hyperbolic polygon given by its list of vertices (z is a list)'''
        if len(z) >= 3:
            if fill == 'none':        
                for i in range(0,len(z)):
                    self.draw_H2_segment(z[i-1],z[i], color, width, refresh = False)
            else:
                cmd = self.__create_H2_segment_str(z[-1], z[0], move_to_first_point = True)
                for i in range(1,len(z)):
                    cmd += " " + self.__create_H2_segment_str(z[i-1], z[i])
                self.svg.append(drawSvg.Path(cmd, stroke = color, stroke_width = width, fill = fill))
            
            if refresh:
                self.__refresh()

    def __make_tessellation2(self, p, q, r, startTriangle, vertices_str, vertices_list, pos_list, steps, step, color1, color2):

        # sets x to 0.0 if x is close to 0.0
        def zero(x):
            if abs(x) < 1e-15:
                x = 0.0
            return x

        # sets real- and imaginary part of complex numbers (c list of complex numerbs) which are close to 0 to 0
        def rc(c):
            return[ zero(n.real) + zero(n.imag) * 1j for n in c]
        
        # returns the color of the current triangle
        def color(i):
            if i % 2 == 0:
                return color1
            else:
                return color2
        
        # magic
        def calculate_next_vertices(p, q, r, prev = "p", prev_pos = []):
        
            def get_number(s):
                if s == 'p':
                        return p
                if s == 'q':
                        return q
                if s == 'r':
                        return r

            def find_third(s):
                if s == "pr" or s == "rp":
                        return "q"
                if s == "pq" or s == "qp":
                        return "r"
                if s == "qr" or s == "rq":
                        return "p"
        
            def find_doubles(s):
                positions = []
                num = 0
                for i in range(len(s)):
                    if s[i-1] == s[i]:
                        if i > 0:
                            positions.append(i-1-num)
                            num += 1
                        else:
                            positions.append(0)
                res_string = s
                res_string = res_string.replace('pp', 'p')
                res_string = res_string.replace('qq', 'q')
                res_string = res_string.replace('rr', 'r')
                if res_string[0] == res_string[-1]:
                        res_string = res_string[:-1]
                return res_string, positions
        
            if prev == "p":
                res_string = ("qr" * p)
                res_list = []
                for i in range(len(res_string)):
                    res_list.append(2*get_number(res_string[i])-2)
                
                return res_string, res_list, [0]*(2*p)
                
            elif len(prev) > 1:           
                
                res_string = ""
                
                for i in range(len(prev)):
                    prev_vertex = prev[i-1]
                    current_vertex = prev[i]
                    
                    num = 2 * get_number(current_vertex) - 3 + prev_pos[i]
                        
                    while num > 0:
                        next_vertex = find_third(prev_vertex + current_vertex)
                        res_string += next_vertex
                        prev_vertex = next_vertex
                        num -= 1
                
                res_string, positions = find_doubles(res_string)
                res_list = [0] * len(res_string)
                for pos in positions:
                    res_list[pos] -= 1
                    
                pos_list = res_list.copy()
                    
                for i in range(len(res_string)):
                    res_list[i] += (2*get_number(res_string[i]) - 2)      
                
                return res_string, res_list, pos_list
        
        if steps < 1:
            return
            
        if step == 1:
            
            print("step ", step)
            
            i = 0
            z1, z2, z3 = startTriangle[0], startTriangle[1], startTriangle[2]
            self.draw_H2_triangle(z1,z2,z3, "#000", 0.002, color(i), False)
            i += 1
            vertices_list[0] -= 1

            for v in vertices_list:
                while v != 0:
                    s = H2_segment(z1,z3)
                    z1, z3, z2 = rc(reflect_triangle(z1,z2,z3, H2_reflection(s)))
                    self.draw_H2_triangle(z1,z2,z3, "#000", 0.002, color(i), False)
                    i += 1
                    v -= 1
                z1, z2, z3 = z3, z1, z2
                            
            z1, z2, z3 = z2, z3, z1
            s = H2_segment(z2,z3)
            z3, z2, z1 = rc(reflect_triangle(z1,z2,z3,H2_reflection(s)))

            new_vertices_str, new_vertices_list, new_pos_list = calculate_next_vertices(p, q, r, vertices_str, pos_list)

            self.__make_tessellation2(p, q, r, [z1,z2,z3], new_vertices_str, new_vertices_list, new_pos_list, steps, step + 1, color1, color2)
            
        elif step != 1 and step <= steps:
            
            print("step ", step)
            
            i = 0            
            z1, z2, z3 = startTriangle[0], startTriangle[1], startTriangle[2]
            self.draw_H2_triangle(z1,z2,z3, "#000", 0.002, color(i), False)
            i += 1
            vertices_list[-1] -= 1
            
            for v in vertices_list:
                v -= 1 
                while v > 0:
                    s = H2_segment(z1,z3)
                    z1, z3, z2 = rc(reflect_triangle(z1,z2,z3,H2_reflection(s)))
                    self.draw_H2_triangle(z1,z2,z3, "#000", 0.002, color(i), False)
                    i += 1
                    v -= 1
                z1, z2, z3 = z3, z1, z2

            s = H2_segment(z1,z3)
            z1, z3, z2 = rc(reflect_triangle(z1,z2,z3,H2_reflection(s)))

            new_vertices_str, new_vertices_list, new_pos_list = calculate_next_vertices(p,q,r, vertices_str, pos_list)
            
            self.__make_tessellation2(p,q,r, [z1,z2,z3], new_vertices_str, new_vertices_list, new_pos_list, steps, step + 1, color1, color2)        

    def make_tessellation2(self, p, q, r, steps = 1, color1 = "#F00", color2 = "#00F"):
        p = int(p)
        q = int(q)
        r = int(r)

        schwarz = SchwarzTriangle(p, q, r)
        z = schwarz.vertices
        z1, z2, z3 = z[0], z[1], z[2]
        startTriangle = [z1,z2,z3]
        self.__make_tessellation2(p, q, r, startTriangle, "p", [2*p], [0], steps, 1, color1, color2)

        self.__refresh() 
