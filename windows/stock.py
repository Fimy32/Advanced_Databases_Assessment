from tkinter import *
import tkinter as tk
from .register import register
from ecommerceDBHandler import *
import hashlib
import matplotlib.pyplot as plt




class Stock(tk.Tk):
      def __init__(self, system):
            super().__init__()
            self.ecommerceSystem = system
            self.title("Stock")
            # days = returnStock()[0]

            # steps_walked = returnStock()[1]

            # plt.plot(days, steps_walked)

            # plt.show()







            self.canvas = Canvas(self, width=550, height=820)
            self.canvas.pack()

            # self.canvas.create_rectangle(50, 20, 150, 80, fill="#476042")
            # self.canvas.create_rectangle(65, 35, 135, 65, fill="yellow")
            # self.canvas.create_line(0, 0, 50, 20, fill="#476042", width=3)
            # self.canvas.create_line(0, 100, 50, 80, fill="#476042", width=3)
            # self.canvas.create_line(150,20, 200, 0, fill="#476042", width=3)
            # self.canvas.create_line(150, 80, 200, 100, fill="#476042", width=3)


            #Data visualisation bar chart
            start_point_text_x=30
            start_point_text_y=110

            start_point_rect_x=60
            start_point_rect_y=100

            step=30
            count =0
            print(returnStock())
            for row in returnStock():
                  self.canvas.create_text(start_point_text_x, start_point_text_y+(step*count), text=row[1])
                  a = self.canvas.create_rectangle(start_point_rect_x, start_point_rect_y+(step*count), 60+int(row[2]), 120+(step*count), fill='red')
                  self.canvas.create_text(80+int(row[2]), 110+(step*count),text=str(row[2])+str("%"))
                  count = count+1 
