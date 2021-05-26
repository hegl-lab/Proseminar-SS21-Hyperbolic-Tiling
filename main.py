#!/usr/bin/env python
# -*- coding: utf-8 -*-

from canvas import Canvas
import tkinter

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
    main_window.run()