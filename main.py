#!/usr/bin/env python
# -*- coding: utf-8 -*-

from schwarztriangle import SchwarzTriangle
from canvas import Canvas
import tkinter
from h2geometry import *

def run_tessellation_program():
    first_window = tkinter.Tk()
    first_window.title("Schwarz triangle tessellation")
    
    #Make boxes for writing p, q and r.
    p = enter_pqr(first_window, "p")
    q = enter_pqr(first_window, "q")
    r = enter_pqr(first_window, "r")

    def f():
        p2 = p.get()
        q2 = q.get()
        r2 = r.get()

        if (float(p2) > 2 and float(q2) > 2 and float(r2) > 2):
            run_main_window_tessellation(float(p2), float(q2), float(r2))
        else:
            if not float(p2) > 2:
                show_not_greater_than_two_error(first_window, "p")
            if not float(q2) > 2:
                show_not_greater_than_two_error(first_window, "q")
            if not float(r2) > 2:
                show_not_greater_than_two_error(first_window, "r")   
        
    printButton = tkinter.Button(first_window,text = "Enter", command = f)
    printButton.pack()

    first_window.mainloop()

def run_main_window_tessellation(p,q,r):
    main_window = Window()

    # Just a test to see if stuff works. p,q and r shouldn't be greater than 10.
    # z1 = - p * 0.1 + p * 0.1j
    # z2 = q * 0.1 - q * 0.1j
    # z3 = r * 0.1 + r * 0.1j
    # main_window.canvas.make_tessellation(z1, z2, z3)

    schwarz = SchwarzTriangle(p,q,r)
    vertices = schwarz.vertices
    z1,z2,z3 = vertices[0],vertices[1],vertices[2]
    #schwarz.make_tessellation()

    main_window.run()

def enter_pqr(window, name):
    frame = tkinter.Frame(window)
    frame.pack()
    label = tkinter.Label(frame, text="Please write " + name + ": ")
    label.pack(side="left")
    var = tkinter.StringVar()
    pqr = tkinter.Entry(frame, textvariable=var, exportselection=0)
    pqr.pack(side="left")
    return pqr
    
def show_not_greater_than_two_error(window, name):
    label = tkinter.Label(window,text= name + " must be > 2.", fg = "red")
    label.pack(side="left")

def test_H2_reflection(window):
    z1=0.5+0.5j
    z2=-0.3-0.3j
    window.canvas.draw_H2_segment(z1, z2, "cyan")
    s=H2_segment(z1, z2)
    z3=0.2+0.3j
    s_ref=H2_reflection(s)
    z3_ref=s_ref.reflect(z3)
    print("z3_ref={}".format(z3_ref))
    window.canvas.draw_H2_segment(z3, z3_ref, "green", complete=False)

def test_reflect_triangle(window):
    z1=0.2+0.7j
    z2=-0.5-0.2j
    s=H2_segment(z1, z2)
    window.canvas.draw_H2_segment(z1, z2)
    s_ref=H2_reflection(s)
    z11 = 0.1 + 0.9j
    z12 = -0.5 + 0.1j 
    z13 = -0.9 + 0.1j
    a, b, c = reflect_triangle(s_ref, z11, z12, z13)
    window.canvas.draw_H2_triangle(a, b, c, "green")


def test_draw_triangle_and_polygon(window):
        # Test for draw_H2_triangle
    z11 = 0.5 + 0.5j
    z12 = -0.5 + 0.5j 
    z13 = -0.2 - 0.7j
    window.canvas.draw_H2_triangle(z11, z12, z13, "hotpink")
    #window.canvas.draw_point(get_barycenter(z11,z12,z13), "green")
    #print(get_barycenter(z11,z12,z13))
    # Test for draw_H2_polygon
    z21 = 0.2 + 0.2j
    z22 = -0.2 + 0.2j 
    z23 = -0.2 - 0.2j
    z24 = 0.2 - 0.2j
    z = [z21,z22,z23,z24]
    window.canvas.draw_H2_polygon(z, "magenta")

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
    run_tessellation_program()
#main_window = Window()

    # Test for H2_reflection
    # ------------------------uncomment the next line for testing
    #test_H2_reflection(main_window)

    #Test for reflecting a triangle
    #------------------------uncomment the next line for testing
    #test_reflect_triangle(main_window)
    
    #test_draw_triangle_and_polygon(main_window)

    #main_window.run()

#test for barycenter
#test_draw_triangle_and_polygon(main_window)
