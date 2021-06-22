#!/usr/bin/env python
# -*- coding: utf-8 -*-

from canvas import Canvas
import tkinter
from h2geometry import H2_segment, H2_reflection

def test_H2_reflection(window):
    #Strange behaviour when z3 is on the geodesic between z1 and z2
    z1=0.5-0.4j
    z2=-0.9-0.1j
    window.canvas.draw_H2_segment(z1, z2, "cyan")
    s=H2_segment(z1, z2)
    z3=0.2+0.2j
    s_ref=H2_reflection(s)
    z3_ref=s_ref.reflect(z3)
    window.canvas.draw_H2_segment(z3, z3_ref, "green", complete=False)

def reflect_triangle(window, s, z1, z2, z3):
    window.canvas.draw_H2_triangle(z1, z2, z3, "orange")
    z1_ref=s.reflect(z1)
    z2_ref=s.reflect(z2)
    z3_ref=s.reflect(z3)
    window.canvas.draw_H2_triangle(z1_ref, z2_ref, z3_ref, "purple")

def test_reflect_triangle(window):
    z1=0.2+0.2j
    z2=-0.5-0.2j
    s=H2_segment(z1, z2)
    window.canvas.draw_H2_segment(z1, z2)
    s_ref=H2_reflection(s)
    z11 = -0.3 + 0.5j
    z12 = -0.5 + 0.1j 
    z13 = -0.9 + 0.1j
    reflect_triangle(window, s_ref, z11, z12, z13)


class Window:
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.title("Hyperbolic tilings")
        self.canvas = Canvas(self.top)
        self.top.bind("<Button-1>", self.mouse_click)
    
    def mouse_click(self, event):
        self.canvas.mouse_click(event)
        
    def run(self):
        self.top.mainloop()

if __name__ == "__main__":
    main_window = Window()

    #Test for H2_reflection
    #------------------------uncomment the next line for testing
    #test_H2_reflection(main_window)

    #Test for reflecting a triangle
    #------------------------uncomment the next line for testing
    #test_reflect_triangle(main_window)
    
    # Test for draw_H2_triangle
    z11 = 0.5 + 0.5j
    z12 = -0.5 + 0.5j 
    z13 = -0.2 - 0.7j
    main_window.canvas.draw_H2_triangle(z11, z12, z13, "hotpink")

    # Test for draw_H2_polygon
    z21 = 0.2 + 0.2j
    z22 = -0.2 + 0.2j 
    z23 = -0.2 - 0.2j
    z24 = 0.2 - 0.2j
    z = [z21,z22,z23,z24]
    main_window.canvas.draw_H2_polygon(z, "magenta")
    main_window.run()